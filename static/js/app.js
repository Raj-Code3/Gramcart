// GramKart storefront script
const PLACEHOLDER = '/static/images/product-placeholder.svg';
const INR = (v) => '\u20B9' + Number(v).toLocaleString('en-IN', { maximumFractionDigits: 2 });

// Replace any broken image with the branded placeholder
window.addEventListener('error', (e) => {
    const el = e.target;
    if (el && el.tagName === 'IMG' && !el.dataset.fallback) {
        el.dataset.fallback = '1';
        el.src = PLACEHOLDER;
    }
}, true);

document.addEventListener('DOMContentLoaded', () => {
    initLiveSearch();
    initWishlistToggles();
});

function getCookie(name) {
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m[2]) : '';
}

function initLiveSearch() {
    const input = document.getElementById('main-search-input');
    const box = document.getElementById('search-results-dropdown');
    if (!input || !box) return;
    let timer;
    input.addEventListener('input', (e) => {
        clearTimeout(timer);
        const q = e.target.value.trim();
        if (q.length < 2) { box.classList.add('hidden'); box.innerHTML = ''; return; }
        timer = setTimeout(() => {
            fetch('/api/quick-search/?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    if (data.results && data.results.length) {
                        let html = '<div class="p-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">Suggested Products</div>';
                        data.results.forEach(item => {
                            html += '<a href="' + item.url + '" class="flex items-center gap-3 p-2.5 hover:bg-slate-50 rounded-xl transition group">' +
                                '<img src="' + item.image + '" alt="" class="w-11 h-11 object-cover rounded-lg bg-slate-100 flex-shrink-0">' +
                                '<div class="flex-1 min-w-0"><p class="text-sm font-medium text-slate-800 group-hover:text-indigo-600 truncate">' + item.name + '</p>' +
                                '<div class="flex items-center gap-2 mt-0.5"><span class="text-xs text-slate-500">' + item.category + '</span>' +
                                '<span class="text-xs font-bold text-indigo-600">' + INR(item.price) + '</span></div></div></a>';
                        });
                        box.innerHTML = html;
                    } else {
                        box.innerHTML = '<div class="p-4 text-center text-sm text-slate-500">No products found</div>';
                    }
                    box.classList.remove('hidden');
                })
                .catch(err => console.error('Search error:', err));
        }, 250);
    });
    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !box.contains(e.target)) box.classList.add('hidden');
    });
}

function initWishlistToggles() {
    document.querySelectorAll('.wishlist-toggle-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const id = this.getAttribute('data-product-id');
            if (!id) return;
            fetch('/wishlist/toggle/' + id + '/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(res => {
                    if (res.redirected) { window.location.href = res.url; return null; }
                    return res.json();
                })
                .then(data => {
                    if (!data || data.status !== 'success') return;
                    const icon = this.querySelector('i');
                    if (icon) {
                        icon.classList.toggle('bi-heart-fill', data.is_added);
                        icon.classList.toggle('text-rose-500', data.is_added);
                        icon.classList.toggle('bi-heart', !data.is_added);
                    }
                    const badge = document.getElementById('global-wishlist-badge');
                    if (badge) {
                        badge.textContent = data.wishlist_count;
                        badge.style.display = data.wishlist_count > 0 ? 'flex' : 'none';
                    }
                    showToast(data.message, data.is_added ? 'success' : 'info');
                })
                .catch(err => console.error('Wishlist error:', err));
        });
    });
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const bg = type === 'success' ? 'bg-emerald-600' : (type === 'error' ? 'bg-rose-600' : 'bg-indigo-600');
    const icon = type === 'success' ? 'bi-check-circle-fill' : (type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill');
    const toast = document.createElement('div');
    toast.className = bg + ' text-white px-5 py-3.5 rounded-2xl shadow-xl flex items-center gap-3 transition-all duration-300 transform translate-y-4 opacity-0 z-50';
    toast.innerHTML = '<i class="bi ' + icon + ' text-lg"></i><span class="text-sm font-medium"></span>';
    toast.querySelector('span').textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.classList.remove('translate-y-4', 'opacity-0'), 10);
    setTimeout(() => { toast.classList.add('opacity-0', 'translate-y-2'); setTimeout(() => toast.remove(), 300); }, 3500);
}
