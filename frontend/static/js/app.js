/**
 * Car Wash Management System - Mobile-First JavaScript
 * The Spot - Kenya
 */

// =============================================================================
// App State and Configuration
// =============================================================================

const SpotApp = {
    // Configuration
    config: {
        apiBaseUrl: '/api',
        refreshInterval: 30000, // 30 seconds
        offlineThreshold: 5000, // 5 seconds
        maxRetries: 3,
        animationDuration: 300,
        touchTargetSize: 44,
        debounceDelay: 300
    },

    // State
    state: {
        isOnline: navigator.onLine,
        currentUser: null,
        lastUpdate: new Date(),
        activeOrders: [],
        syncQueue: [],
        refreshTimer: null,
        retryCount: 0,
        pageVisibility: 'visible'
    },

    // DOM Elements
    elements: {
        connectionStatus: null,
        offlineBanner: null,
        searchModal: null,
        searchInput: null,
        searchResults: null,
        loadingOverlay: null,
        contentArea: null
    },

    // Event Listeners
    listeners: new Map(),

    // Initialize app
    init() {
        console.log('Initializing The Spot Car Wash Management System');

        // Cache DOM elements
        this.cacheElements();

        // Setup event listeners
        this.setupEventListeners();

        // Initialize features based on current page
        this.initializePageFeatures();

        // Start background processes
        this.startBackgroundProcesses();

        // Check authentication state
        this.checkAuthentication();

        console.log('Spot App initialized successfully');
    },

    // Cache frequently used DOM elements
    cacheElements() {
        this.elements.connectionStatus = document.getElementById('connectionStatus');
        this.elements.offlineBanner = document.getElementById('offlineBanner');
        this.elements.searchModal = document.getElementById('searchModal');
        this.elements.searchInput = document.getElementById('searchInput');
        this.elements.searchResults = document.getElementById('searchResults');
        this.elements.contentArea = document.querySelector('main');
    },

    // Setup global event listeners
    setupEventListeners() {
        // Network connectivity
        window.addEventListener('online', this.handleOnline.bind(this));
        window.addEventListener('offline', this.handleOffline.bind(this));

        // Page visibility changes
        document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));

        // Touch events for mobile gestures
        if ('ontouchstart' in window) {
            this.setupTouchGestures();
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));

        // Search functionality
        if (this.elements.searchInput) {
            this.elements.searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), this.config.debounceDelay));
        }

        // Prevent zoom on double tap for mobile
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);

        // Handle back button for mobile apps
        window.addEventListener('popstate', this.handleBackButton.bind(this));
    },

    // Handle online/offline states
    handleOnline() {
        this.state.isOnline = true;
        this.updateConnectionIndicator(true);
        this.hideOfflineBanner();
        this.syncOfflineActions();
        this.startRealTimeUpdates();

        // Show notification
        this.showToast('Connection restored', 'success');
    },

    handleOffline() {
        this.state.isOnline = false;
        this.updateConnectionIndicator(false);
        this.showOfflineBanner();
        this.stopRealTimeUpdates();

        // Show notification
        this.showToast('You\'re offline. Some features may be limited.', 'warning');
    },

    updateConnectionIndicator(isOnline) {
        if (!this.elements.connectionStatus) return;

        const icon = this.elements.connectionStatus.querySelector('i');
        const text = this.elements.connectionStatus.querySelector('span');

        if (isOnline) {
            icon.className = 'bi bi-wifi';
            text.textContent = 'Online';
            this.elements.connectionStatus.classList.remove('offline');
        } else {
            icon.className = 'bi bi-wifi-off';
            text.textContent = 'Offline';
            this.elements.connectionStatus.classList.add('offline');
        }
    },

    showOfflineBanner() {
        if (this.elements.offlineBanner) {
            this.elements.offlineBanner.classList.remove('d-none');
        }
    },

    hideOfflineBanner() {
        if (this.elements.offlineBanner) {
            this.elements.offlineBanner.classList.add('d-none');
        }
    },

    // Handle page visibility changes
    handleVisibilityChange() {
        this.state.pageVisibility = document.visibilityState;

        if (this.state.pageVisibility === 'visible') {
            // Page became visible, refresh data
            this.refreshCurrentPage();
            this.startRealTimeUpdates();
        } else {
            // Page hidden, reduce update frequency
            this.stopRealTimeUpdates();
        }
    },

    // Setup touch gestures for mobile
    setupTouchGestures() {
        // Add swipe gestures for queue management
        const queueRows = document.querySelectorAll('.queue-row');
        queueRows.forEach(row => {
            let startX = 0;
            let startY = 0;

            row.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            }, { passive: true });

            row.addEventListener('touchend', (e) => {
                if (!startX || !startY) return;

                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;

                const diffX = startX - endX;
                const diffY = startY - endY;

                // Only handle horizontal swipes
                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                    if (diffX > 0) {
                        // Swipe left - complete
                        this.handleSwipeLeft(row);
                    } else {
                        // Swipe right - start
                        this.handleSwipeRight(row);
                    }
                }

                startX = 0;
                startY = 0;
            }, { passive: true });
        });
    },

    handleSwipeLeft(element) {
        const orderId = element.dataset.orderId;
        if (orderId) {
            this.quickCompleteOrder(orderId);
        }
    },

    handleSwipeRight(element) {
        const orderId = element.dataset.orderId;
        if (orderId) {
            this.quickStartOrder(orderId);
        }
    },

    // Handle keyboard shortcuts
    handleKeyboardShortcuts(event) {
        // Focus search with "/" key
        if (event.key === '/' && !event.ctrlKey && !event.metaKey) {
            const activeElement = document.activeElement;
            if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
                event.preventDefault();
                this.openSearchModal();
            }
        }

        // Close modals with Escape
        if (event.key === 'Escape') {
            this.closeAllModals();
        }
    },

    // Open search modal
    openSearchModal() {
        if (this.elements.searchModal) {
            const modal = new bootstrap.Modal(this.elements.searchModal);
            modal.show();
            // Focus input after modal is shown
            setTimeout(() => {
                if (this.elements.searchInput) {
                    this.elements.searchInput.focus();
                }
            }, this.config.animationDuration);
        }
    },

    // Close all modals
    closeAllModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    },

    // Handle search functionality
    async handleSearch(event) {
        const query = event.target.value.trim();

        if (query.length < 2) {
            this.clearSearchResults();
            return;
        }

        try {
            const response = await this.apiCall('/search', 'GET', { q: query });
            if (response.success) {
                this.displaySearchResults(response.data.results);
            }
        } catch (error) {
            console.error('Search error:', error);
            this.displaySearchError(error.message);
        }
    },

    displaySearchResults(results) {
        if (!this.elements.searchResults) return;

        const html = this.generateSearchResultsHTML(results);
        this.elements.searchResults.innerHTML = html;
    },

    generateSearchResultsHTML(results) {
        let html = '';

        // Customers
        if (results.customers && results.customers.length > 0) {
            html += '<div class="search-category"><h6 class="text-muted mb-2">Customers</h6>';
            results.customers.forEach(customer => {
                html += `
                    <div class="search-result-item" onclick="SpotApp.navigateToCustomer(${customer.id})">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${customer.name || customer.phone_number}</strong>
                                <div class="small text-muted">${customer.phone_number}</div>
                            </div>
                            <span class="badge bg-primary">${customer.total_visits} visits</span>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }

        // Vehicles
        if (results.vehicles && results.vehicles.length > 0) {
            html += '<div class="search-category"><h6 class="text-muted mb-2">Vehicles</h6>';
            results.vehicles.forEach(vehicle => {
                html += `
                    <div class="search-result-item" onclick="SpotApp.navigateToVehicle(${vehicle.id})">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${vehicle.registration_number}</strong>
                                <div class="small text-muted">${vehicle.make} ${vehicle.model || ''}</div>
                            </div>
                            <span class="badge bg-secondary">${vehicle.service_count} services</span>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }

        // Orders
        if (results.orders && results.orders.length > 0) {
            html += '<div class="search-category"><h6 class="text-muted mb-2">Orders</h6>';
            results.orders.forEach(order => {
                html += `
                    <div class="search-result-item" onclick="SpotApp.navigateToOrder(${order.id})">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${order.order_number}</strong>
                                <div class="small text-muted">${new Date(order.created_at).toLocaleDateString()}</div>
                            </div>
                            <span class="badge bg-${this.getStatusBadgeClass(order.status)}">${order.status}</span>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }

        return html || '<div class="text-center text-muted py-3">No results found</div>';
    },

    displaySearchError(message) {
        if (this.elements.searchResults) {
            this.elements.searchResults.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    ${message}
                </div>
            `;
        }
    },

    clearSearchResults() {
        if (this.elements.searchResults) {
            this.elements.searchResults.innerHTML = '';
        }
    },

    getStatusBadgeClass(status) {
        const classes = {
            'pending': 'warning',
            'in_progress': 'info',
            'completed': 'success',
            'cancelled': 'danger'
        };
        return classes[status] || 'secondary';
    },

    // Navigation methods
    navigateToCustomer(customerId) {
        window.location.href = `/customers/${customerId}`;
    },

    navigateToVehicle(vehicleId) {
        window.location.href = `/vehicles/${vehicleId}`;
    },

    navigateToOrder(orderId) {
        window.location.href = `/orders/${orderId}`;
    },

    // =============================================================================
    // API and Data Management
    // =============================================================================

    async apiCall(endpoint, method = 'GET', data = null, customHeaders = {}) {
        const url = `${this.config.apiBaseUrl}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...customHeaders
            }
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.state.retryCount = 0;
            return result;

        } catch (error) {
            console.error(`API call failed: ${endpoint}`, error);

            if (this.state.isOnline) {
                // Retry logic for temporary failures
                if (this.state.retryCount < this.config.maxRetries) {
                    this.state.retryCount++;
                    await this.delay(1000 * this.state.retryCount);
                    return this.apiCall(endpoint, method, data, customHeaders);
                }
            }

            throw error;
        }
    },

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    // =============================================================================
    // Order Management
    // =============================================================================

    async quickStartOrder(orderId) {
        if (!confirm('Start this order now?')) return;

        try {
            this.showLoading('Starting order...');

            const response = await this.apiCall(`/orders/${orderId}/start`, 'POST');

            if (response.success) {
                this.showToast('Order started successfully', 'success');
                this.refreshCurrentPage();
            } else {
                this.showToast(response.error?.message || 'Failed to start order', 'error');
            }
        } catch (error) {
            console.error('Start order error:', error);
            this.showToast('Failed to start order. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    },

    async quickCompleteOrder(orderId) {
        if (!confirm('Mark this order as complete?')) return;

        try {
            this.showLoading('Completing order...');

            const response = await this.apiCall(`/orders/${orderId}/finish`, 'POST');

            if (response.success) {
                this.showToast('Order completed successfully', 'success');
                this.refreshCurrentPage();
            } else {
                this.showToast(response.error?.message || 'Failed to complete order', 'error');
            }
        } catch (error) {
            console.error('Complete order error:', error);
            this.showToast('Failed to complete order. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    },

    // =============================================================================
    // Background Processes and Real-time Updates
    // =============================================================================

    startBackgroundProcesses() {
        this.startRealTimeUpdates();
        this.initializeServiceWorker();
        this.setupPeriodicSync();
    },

    startRealTimeUpdates() {
        if (!this.state.isOnline) return;

        // Clear existing timer
        if (this.state.refreshTimer) {
            clearInterval(this.state.refreshTimer);
        }

        // Set new timer
        this.state.refreshTimer = setInterval(() => {
            if (this.state.pageVisibility === 'visible' && this.state.isOnline) {
                this.refreshCurrentPage();
            }
        }, this.config.refreshInterval);
    },

    stopRealTimeUpdates() {
        if (this.state.refreshTimer) {
            clearInterval(this.state.refreshTimer);
            this.state.refreshTimer = null;
        }
    },

    async refreshCurrentPage() {
        try {
            // Only refresh if we're on a page that needs real-time data
            if (this.shouldRefreshCurrentPage()) {
                const response = await this.apiCall('/dashboard-stats');
                if (response.success && response.data) {
                    this.updateDashboardStats(response.data);
                }
            }
        } catch (error) {
            console.error('Refresh error:', error);
        }
    },

    shouldRefreshCurrentPage() {
        // Define which pages need real-time updates
        const refreshablePages = [
            '/dashboard',
            '/queue',
            '/new-order'
        ];

        return refreshablePages.some(path =>
            window.location.pathname.includes(path)
        );
    },

    updateDashboardStats(stats) {
        // Update stat cards with animation
        this.animateNumber('[data-stat="today-orders"]', stats.today_orders);
        this.animateNumber('[data-stat="active-queue"]', stats.active_queue);
        this.animateNumber('[data-stat="today-revenue"]', stats.today_revenue, 'KES ');

        // Update last updated time
        const lastUpdated = document.getElementById('lastUpdated');
        if (lastUpdated) {
            lastUpdated.textContent = new Date(stats.last_updated).toLocaleTimeString();
        }
    },

    animateNumber(selector, value, prefix = '') {
        const element = document.querySelector(selector);
        if (!element) return;

        const current = parseInt(element.textContent.replace(/[^0-9]/g, '')) || 0;
        const increment = (value - current) / 10;
        let step = 0;

        const timer = setInterval(() => {
            step++;
            if (step >= 10) {
                element.textContent = prefix + value.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = prefix + Math.round(current + increment * step).toLocaleString();
            }
        }, 30);
    },

    // =============================================================================
    // Service Worker and Offline Support
    // =============================================================================

    initializeServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('✅ Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('❌ Service Worker registration failed:', error);
                });
        }
    },

    setupPeriodicSync() {
        // Register for periodic sync if supported
        if ('serviceWorker' in navigator && 'periodicSync' in window.ServiceWorkerRegistration.prototype) {
            navigator.serviceWorker.ready.then(registration => {
                return registration.periodicSync.register('sync-data', {
                    minInterval: 24 * 60 * 60 * 1000 // 24 hours
                });
            }).catch(error => {
                console.log('Periodic sync registration failed:', error);
            });
        }
    },

    async syncOfflineActions() {
        if (this.state.syncQueue.length === 0) return;

        console.log(`🔄 Syncing ${this.state.syncQueue.length} offline actions`);

        for (const action of this.state.syncQueue) {
            try {
                await this.apiCall(action.endpoint, action.method, action.data);
                this.state.syncQueue.splice(this.state.syncQueue.indexOf(action), 1);
            } catch (error) {
                console.error('Sync failed for action:', action, error);
                // Keep failed actions for retry
            }
        }

        this.showToast('Offline actions synced successfully', 'success');
    },

    // =============================================================================
    // Authentication
    // =============================================================================

async checkAuthentication() {
    // Skip auth check if we're already on the login page
    if (window.location.pathname.includes('/auth/login')) {
        return;
    }
    
    try {
        const response = await this.apiCall('/auth/profile');
        if (response.success) {
            this.state.currentUser = response.data.user;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        // Only redirect if we get a 401/403, not on network errors
        if (error.message && (error.message.includes('401') || error.message.includes('403'))) {
            window.location.href = '/auth/login';
        }
    }
}

    async logout() {
        try {
            await this.apiCall('/auth/logout', 'POST');
            window.location.href = '/auth/login';
        } catch (error) {
            console.error('Logout error:', error);
            // Force redirect even on error
            window.location.href = '/auth/login';
        }
    },

    // =============================================================================
    // UI Utilities
    // =============================================================================

    showToast(message, type = 'info', duration = 5000) {
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        // Create toast element
        const toastId = 'toast_' + Date.now();
        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHTML);

        // Initialize and show toast
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: duration });
        toast.show();

        // Remove from DOM after hiding
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },

    showLoading(message = 'Loading...') {
        this.hideLoading(); // Remove any existing loading overlay

        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="text-center">
                <div class="loading-spinner mb-3"></div>
                <div class="fw-bold">${message}</div>
            </div>
        `;
        document.body.appendChild(overlay);
    },

    hideLoading() {
        const overlay = document.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    },

    // =============================================================================
    // Page-specific Initialization
    // =============================================================================

    initializePageFeatures() {
        const currentPath = window.location.pathname;

        // Initialize features based on current page
        if (currentPath === '/dashboard') {
            this.initializeDashboard();
        } else if (currentPath === '/queue') {
            this.initializeQueue();
        } else if (currentPath.includes('/new-order')) {
            this.initializeNewOrderForm();
        } else if (currentPath.includes('/orders/')) {
            this.initializeOrderView();
        } else if (currentPath.includes('/payments')) {
            this.initializePaymentsPage();
        }
    },

    initializeDashboard() {
        console.log('📊 Initializing dashboard features');
        // Dashboard-specific initialization already handled by inline scripts
    },

    initializeQueue() {
        console.log('🚗 Initializing queue management');
        // Enhanced queue management features
        this.setupQueueAutoRefresh();
    },

    setupQueueAutoRefresh() {
        // More frequent refresh for queue page
        if (this.state.refreshTimer) {
            clearInterval(this.state.refreshTimer);
        }

        this.state.refreshTimer = setInterval(() => {
            if (this.state.pageVisibility === 'visible' && this.state.isOnline) {
                window.location.reload(); // Simple reload for queue page
            }
        }, 15000); // 15 seconds for queue page
    },

    initializeNewOrderForm() {
        console.log('➕ Initializing new order form');
        this.setupServiceSelection();
        this.setupFormValidation();
    },

    setupServiceSelection() {
        const serviceCheckboxes = document.querySelectorAll('input[name="services"]');
        const totalElement = document.getElementById('totalAmount');

        if (serviceCheckboxes.length > 0 && totalElement) {
            const updateTotal = () => {
                let total = 0;
                serviceCheckboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        total += parseFloat(checkbox.dataset.price) || 0;
                    }
                });
                totalElement.textContent = `KES ${total.toLocaleString()}`;
            };

            serviceCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', updateTotal);
            });

            updateTotal(); // Initial calculation
        }
    },

    setupFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    },

    initializeOrderView() {
        console.log('👁️ Initializing order view');
        this.setupOrderStatusUpdates();
    },

    setupOrderStatusUpdates() {
        // Real-time updates for order status
        const orderId = window.location.pathname.split('/').pop();
        if (orderId && !isNaN(orderId)) {
            this.pollOrderStatus(orderId);
        }
    },

    async pollOrderStatus(orderId) {
        try {
            const response = await this.apiCall(`/orders/${orderId}`);
            if (response.success && response.data.order) {
                const order = response.data.order;
                this.updateOrderStatus(order);
            }
        } catch (error) {
            console.error('Order status poll error:', error);
        }

        // Continue polling if order is active
        setTimeout(() => this.pollOrderStatus(orderId), 10000);
    },

    updateOrderStatus(order) {
        const statusElements = document.querySelectorAll('[data-order-status]');
        statusElements.forEach(element => {
            element.textContent = order.status;
            element.className = `badge bg-${this.getStatusBadgeClass(order.status)}`;
        });
    },

    initializePaymentsPage() {
        console.log('💰 Initializing payments page');
        this.setupPaymentForm();
    },

    setupPaymentForm() {
        const paymentForm = document.getElementById('paymentForm');
        const amountInput = document.getElementById('amount');
        const paymentMethod = document.getElementById('paymentMethod');
        const changeAmount = document.getElementById('changeAmount');

        if (paymentForm && amountInput && paymentMethod && changeAmount) {
            const updateChange = () => {
                const amount = parseFloat(amountInput.value) || 0;
                const orderTotal = parseFloat(paymentForm.dataset.orderTotal) || 0;

                if (paymentMethod.value === 'cash' && amount > orderTotal) {
                    changeAmount.textContent = `KES ${(amount - orderTotal).toLocaleString()}`;
                    changeAmount.parentElement.classList.remove('d-none');
                } else {
                    changeAmount.parentElement.classList.add('d-none');
                }
            };

            amountInput.addEventListener('input', updateChange);
            paymentMethod.addEventListener('change', updateChange);
            updateChange(); // Initial calculation
        }
    },

    // =============================================================================
    // Utility Functions
    // =============================================================================

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-KE', {
            style: 'currency',
            currency: 'KES',
            minimumFractionDigits: 0
        }).format(amount);
    },

    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-KE', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    handleBackButton(event) {
        // Handle custom back button behavior for mobile apps
        const modals = document.querySelectorAll('.modal.show');
        if (modals.length > 0) {
            event.preventDefault();
            this.closeAllModals();
        }
    }
};

// =============================================================================
// Initialize App
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    SpotApp.init();

    // Make app globally accessible
    window.SpotApp = SpotApp;

    console.log('🎉 The Spot is ready to go!');
});

// =============================================================================
// Error Handling
// =============================================================================

window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    SpotApp.showToast('Something went wrong. Please refresh the page.', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    SpotApp.showToast('A network error occurred. Please check your connection.', 'error');
});

// =============================================================================
// Performance Monitoring
// =============================================================================

if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log(`📈 Page load time: ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
            }
        }, 0);
    });
}