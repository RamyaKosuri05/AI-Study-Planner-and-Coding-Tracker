"""
Study4u
A dynamic, full-stack Flask web application with a professional SaaS aesthetic.
"""

from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import random
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'study4u-professional-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# ─────────────────────────────────────────────
#  Database Models (Strict Schema)
# ─────────────────────────────────────────────

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id       = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password      = db.Column(db.String(256), nullable=False)

    def get_id(self):
        return str(self.user_id)
        
    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)


class StudyTasks(db.Model):
    __tablename__ = 'StudyTasks'
    task_id       = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    task_name     = db.Column(db.String(200), nullable=False)
    priority      = db.Column(db.String(20), default='Medium')
    deadline      = db.Column(db.Date, nullable=True)
    status        = db.Column(db.String(20), default='Pending')


class CodingProblems(db.Model):
    __tablename__ = 'CodingProblems'
    problem_id    = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    problem_name  = db.Column(db.String(200), nullable=False)
    platform      = db.Column(db.String(50), nullable=False)
    difficulty    = db.Column(db.String(20), nullable=False)
    date_solved   = db.Column(db.Date, default=date.today)


class StudySessions(db.Model):
    __tablename__ = 'StudySessions'
    session_id    = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    hours_studied = db.Column(db.Float, nullable=False)
    date          = db.Column(db.Date, default=date.today)


class StreakData(db.Model):
    __tablename__ = 'StreakData'
    user_id        = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date, nullable=True)


@login_manager.user_loader
def load_user(uid):
    return Users.query.get(int(uid))

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def get_quote():
    quotes = [
        "Your only limit is your mind.",
        "Small steps every day.",
        "Grind now, shine later.",
        "Debug your mind, compile your dreams.",
        "Stay curious, stay foolish."
    ]
    return random.choice(quotes)

def update_streak(user_id):
    """Update streak dynamically based on activity."""
    sd = StreakData.query.get(user_id)
    today = date.today()
    if not sd:
        sd = StreakData(user_id=user_id, current_streak=1, longest_streak=1, last_activity_date=today)
        db.session.add(sd)
    else:
        if sd.last_activity_date != today:
            if sd.last_activity_date == today - timedelta(days=1):
                # Consecutive day
                sd.current_streak += 1
            else:
                # Missed a day
                sd.current_streak = 1
            
            sd.last_activity_date = today
            if sd.current_streak > sd.longest_streak:
                sd.longest_streak = sd.current_streak
    db.session.commit()

# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        u = data.get('username')
        e = data.get('email')
        p = data.get('password')
        
        if Users.query.filter_by(username=u).first() or Users.query.filter_by(email=e).first():
            return jsonify({'success': False, 'error': 'User exists'}), 400
            
        user = Users(username=u, email=e)
        user.set_password(p)
        db.session.add(user)
        db.session.commit()
        
        # Init streak
        db.session.add(StreakData(user_id=user.user_id))
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        u = Users.query.filter_by(email=data.get('email')).first()
        if u and u.check_password(data.get('password')):
            login_user(u)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    uid = current_user.user_id
    total_hours = db.session.query(db.func.sum(StudySessions.hours_studied)).filter_by(user_id=uid).scalar() or 0.0
    total_problems = CodingProblems.query.filter_by(user_id=uid).count()
    
    streak = StreakData.query.get(uid)
    curr_streak = streak.current_streak if streak else 0
    
    all_tasks = StudyTasks.query.filter_by(user_id=uid).count()
    done_tasks = StudyTasks.query.filter_by(user_id=uid, status='Completed').count()
    progress_pct = round((done_tasks / all_tasks * 100) if all_tasks else 0)
    
    upcoming = StudyTasks.query.filter(StudyTasks.user_id==uid, StudyTasks.status!='Completed').limit(5).all()
    
    return render_template('dashboard.html',
        total_hours=round(total_hours, 1),
        total_problems=total_problems,
        current_streak=curr_streak,
        progress_pct=progress_pct,
        upcoming=upcoming,
        quote=get_quote()
    )

# Tasks
@app.route('/planner')
@login_required
def planner():
    tasks = StudyTasks.query.filter_by(user_id=current_user.user_id).all()
    return render_template('planner.html', tasks=tasks)

@app.route('/planner/add', methods=['POST'])
@login_required
def add_task():
    d = request.json
    dl = datetime.strptime(d['deadline'], '%Y-%m-%d').date() if d.get('deadline') else None
    t = StudyTasks(user_id=current_user.user_id, task_name=d['task_name'], priority=d['priority'], deadline=dl)
    db.session.add(t)
    update_streak(current_user.user_id)
    return jsonify({'success': True})

@app.route('/planner/update/<int:tid>', methods=['PUT'])
@login_required
def update_task(tid):
    t = StudyTasks.query.get(tid)
    if t and t.user_id == current_user.user_id:
        if 'status' in request.json: t.status = request.json['status']
        db.session.commit()
    return jsonify({'success': True})

@app.route('/planner/delete/<int:tid>', methods=['DELETE'])
@login_required
def delete_task(tid):
    t = StudyTasks.query.get(tid)
    if t and t.user_id == current_user.user_id:
        db.session.delete(t)
        db.session.commit()
    return jsonify({'success': True})

# Coding
@app.route('/coding')
@login_required
def coding_tracker():
    problems = CodingProblems.query.filter_by(user_id=current_user.user_id).all()
    return render_template('coding_tracker.html', problems=problems)

@app.route('/coding/add', methods=['POST'])
@login_required
def add_problem():
    d = request.json
    ds = datetime.strptime(d['date_solved'], '%Y-%m-%d').date() if d.get('date_solved') else date.today()
    p = CodingProblems(user_id=current_user.user_id, problem_name=d['problem_name'], 
                       platform=d['platform'], difficulty=d['difficulty'], date_solved=ds)
    db.session.add(p)
    update_streak(current_user.user_id)
    return jsonify({'success': True})

@app.route('/coding/delete/<int:pid>', methods=['DELETE'])
@login_required
def delete_problem(pid):
    p = CodingProblems.query.get(pid)
    if p and p.user_id == current_user.user_id:
        db.session.delete(p)
        db.session.commit()
    return jsonify({'success': True})

# Sessions
@app.route('/sessions/add', methods=['POST'])
@login_required
def add_session():
    d = request.json
    s = StudySessions(user_id=current_user.user_id, hours_studied=float(d['hours_studied']), date=date.today())
    db.session.add(s)
    db.session.commit()
    update_streak(current_user.user_id)
    return jsonify({'success': True})

# Analytics endpoints
@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/api/charts/tasks')
@login_required
def api_tasks():
    uid = current_user.user_id
    done = StudyTasks.query.filter_by(user_id=uid, status='Completed').count()
    pend = StudyTasks.query.filter(StudyTasks.user_id==uid, StudyTasks.status!='Completed').count()
    return jsonify({'labels': ['Completed', 'Pending'], 'data': [done, pend], 'colors': ['#10b981', '#f43f5e']})

@app.route('/api/charts/coding')
@login_required
def api_coding():
    uid = current_user.user_id
    rows = db.session.query(CodingProblems.platform, db.func.count(CodingProblems.problem_id)).filter_by(user_id=uid).group_by(CodingProblems.platform).all()
    return jsonify({'labels': [r[0] for r in rows], 'data': [r[1] for r in rows], 'colors': ['#4f46e5', '#0ea5e9', '#6366f1']})

@app.route('/api/charts/productivity')
@login_required
def api_prod():
    uid = current_user.user_id
    labels, data = [], []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        hrs = db.session.query(db.func.sum(StudySessions.hours_studied)).filter_by(user_id=uid, date=d).scalar() or 0
        labels.append(d.strftime('%a'))
        data.append(hrs)
    return jsonify({'labels': labels, 'data': data})

@app.route('/api/charts/difficulty')
@login_required
def api_diff():
    uid = current_user.user_id
    rows = db.session.query(CodingProblems.difficulty, db.func.count(CodingProblems.problem_id)).filter_by(user_id=uid).group_by(CodingProblems.difficulty).all()
    return jsonify({'labels': [r[0] for r in rows], 'data': [r[1] for r in rows], 'colors': ['#10b981', '#f59e0b', '#ef4444']})

# Reports
@app.route('/reports')
@login_required
def reports():
    uid = current_user.user_id
    # Weekly calc
    w_start = date.today() - timedelta(days=7)
    w_hrs = db.session.query(db.func.sum(StudySessions.hours_studied)).filter(StudySessions.user_id==uid, StudySessions.date>=w_start).scalar() or 0
    w_probs = CodingProblems.query.filter(CodingProblems.user_id==uid, CodingProblems.date_solved>=w_start).count()
    w_score = min(w_hrs * 5 + w_probs * 5, 100)
    
    # Monthly calc
    m_start = date.today() - timedelta(days=30)
    m_hrs = db.session.query(db.func.sum(StudySessions.hours_studied)).filter(StudySessions.user_id==uid, StudySessions.date>=m_start).scalar() or 0
    m_probs = CodingProblems.query.filter(CodingProblems.user_id==uid, CodingProblems.date_solved>=m_start).count()
    m_score = min(m_hrs * 2 + m_probs * 2, 100)
    
    return render_template('reports.html', w_hrs=w_hrs, w_probs=w_probs, w_score=w_score, m_hrs=m_hrs, m_probs=m_probs, m_score=m_score)

# Dev Route for testing Streaks
@app.route('/dev/backdate-streak')
@login_required
def dev_backdate_streak():
    """Artificially sets your last activity date to yesterday so you can test tomorrow's streak logic."""
    sd = StreakData.query.get(current_user.user_id)
    if sd and sd.last_activity_date:
        sd.last_activity_date = date.today() - timedelta(days=1)
        db.session.commit()
        flash('Developer Tool: Your streak last_activity_date was just moved to yesterday! Log a task/problem now to see your streak increase.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("[OK] Study4u DB created.")
    app.run(debug=True, host='0.0.0.0', port=5000)
