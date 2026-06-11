# 🎓 StudyFlow — AI Study Planner & Coding Tracker

A **modern, full-stack web application** built with Python (Flask) and SQLite to help students organize their study schedules, track coding practice, maintain learning streaks, and generate weekly progress reports.

> 🎨 **Design Philosophy**: OxygenOS-inspired UI — ultra-fluid animations, glassmorphism, spring physics, dark/light mode, and premium micro-interactions.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Auth** | Secure registration & login with hashed passwords |
| 📊 **Dashboard** | Stats, streak heatmap, AI suggestions, mini chart |
| 📋 **Study Planner** | CRUD tasks with priority, deadline & hours tracking |
| 💻 **Coding Tracker** | Log solved problems with platform, difficulty & topic filters |
| 🔥 **Streak System** | Automatic daily streak calculation with milestone badges |
| 📈 **Analytics** | 6 interactive Chart.js charts (doughnut, bar, line) |
| 📄 **Reports** | Weekly progress snapshots with productivity scores |
| 🤖 **AI Suggestions** | Rule-based intelligent insights (no API key needed!) |
| 👤 **Profile** | Score ring, color picker, streak stats, recommendations |
| 🌙 **Dark/Light Mode** | Persistent theme toggle across sessions |

---

## 🚀 Quick Start

### 1. Clone / Download the project

```
cd "c:\Users\Ramya\Videos\New pro"
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

> 🎉 Register a new account — sample data is automatically seeded!

---

## 📁 Project Structure

```
New pro/
├── app.py                  # Flask backend (routes, models, helpers)
├── database.db             # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── templates/
│   ├── base.html           # Shared layout (sidebar, topbar, theme)
│   ├── login.html          # Login page with particles
│   ├── register.html       # Registration with password strength meter
│   ├── dashboard.html      # Main dashboard with all stats
│   ├── planner.html        # Study task manager
│   ├── coding_tracker.html # Coding problem logger
│   ├── analytics.html      # Chart.js analytics
│   ├── reports.html        # Weekly progress reports
│   └── profile.html        # User profile & settings
│
└── static/
    ├── css/
    │   └── style.css       # OxygenOS-inspired design system (~900 lines)
    └── js/
        └── main.js         # Interactions, charts, animations (~350 lines)
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0 |
| Database | SQLite via Flask-SQLAlchemy |
| Auth | Flask-Login + Werkzeug password hashing |
| Frontend | HTML5, Vanilla CSS, JavaScript (ES6+) |
| Charts | Chart.js 4.4 (CDN) |
| Fonts | Inter + JetBrains Mono (Google Fonts) |

---

## 🤖 AI Features (No API Key Required)

The AI engine is powered by intelligent rule-based logic:

- **Streak encouragement** — Messages at 3, 7, 14, 30-day milestones
- **Difficulty coaching** — Suggests harder problems when too many Easies
- **Productivity insights** — Compares activity to weekly targets
- **Topic recommendations** — Suggests missing DSA topics
- **Daily motivational quotes** — Deterministic by day-of-year

---

## 📊 Database Schema

```sql
users          (id, username, email, password_hash, avatar_color, created_at)
study_tasks    (id, user_id, title, description, priority, status, hours, deadline, created_at, completed_at)
coding_problems(id, user_id, name, platform, difficulty, topic, notes, date_solved)
streak_data    (id, user_id, activity_date, activity_type, count)
weekly_reports (id, user_id, week_start, tasks_done, problems_solved, study_hours, score)
```

---

## 🎨 Design Highlights

- **OxygenOS-inspired** fluid animations with spring physics (`cubic-bezier(0.34, 1.56, 0.64, 1)`)
- **Custom scrollbar**, animated gradient background orbs
- **Glassmorphism** cards with `backdrop-filter: blur()`
- **Staggered entry animations** for all list items
- **Animated counters** using IntersectionObserver
- **Toast notifications** with slide-in/out
- **Responsive** — works on mobile, tablet, and desktop

---

## 🎯 Productivity Score Formula

```
Score = (tasks_completed/10 × 40%) + (problems_solved/10 × 40%) + (streak_days/7 × 20%)
Max = 100 points
```

---

*Built for software developer fresher portfolios — resume-worthy, full-stack, and production-quality.*
