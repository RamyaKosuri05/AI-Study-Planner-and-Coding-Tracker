// Theme Management
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    
    // Update button icon
    const tBtn = document.getElementById('themeToggleBtn');
    if (tBtn) tBtn.innerText = next === 'dark' ? '☀️' : '🌙';
    
    // If charts exist, re-render them
    if (window.initCharts) window.initCharts();
}

// Modal Management
const Modal = {
    open: (id) => document.getElementById(id).classList.add('open'),
    close: (id) => document.getElementById(id).classList.remove('open')
};

// Generic API Call
async function apiCall(url, method, body) {
    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (data.success) {
        location.reload();
    } else {
        alert(data.error || 'Something went wrong');
    }
}
