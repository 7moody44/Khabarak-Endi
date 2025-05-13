// Utility functions can be added here
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

// Add event listeners for search and filter
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('news-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(() => {
            // Implement search functionality
        }, 300));
    }

    const sortSelect = document.getElementById('news-sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            // Implement sorting functionality
        });
    }
});
