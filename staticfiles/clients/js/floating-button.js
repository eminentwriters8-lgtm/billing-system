// Floating Add Client Button - Auto-hide on admin pages
document.addEventListener('DOMContentLoaded', function() {
    // Hide button on admin pages
    if (window.location.pathname.startsWith('/admin/')) {
        const btn = document.querySelector('.floating-add-btn');
        if (btn) {
            btn.style.display = 'none';
        }
    }
});
