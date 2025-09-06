// Main JavaScript functionality for The Oasis Hotel & Spa

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeNavbar();
    initializeAnimations();
    initializeForms();
    initializeGallery();
});

// Navbar functionality
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    
    // Add background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
        
        // Close mobile menu when clicking on nav links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }
}

// Animation initialization
function initializeAnimations() {
    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe cards and other elements
    const animateElements = document.querySelectorAll('.card, .amenity-icon');
    animateElements.forEach(element => {
        observer.observe(element);
    });
}

// Form functionality
function initializeForms() {
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Scroll to first error
                const firstError = form.querySelector(':invalid');
                if (firstError) {
                    firstError.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                    firstError.focus();
                }
            } else {
                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
    
    // Date validation for booking form
    const checkInDate = document.getElementById('check_in');
    const checkOutDate = document.getElementById('check_out');
    
    if (checkInDate && checkOutDate) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        checkInDate.min = today;
        checkOutDate.min = today;
        
        checkInDate.addEventListener('change', function() {
            checkOutDate.min = this.value;
            if (checkOutDate.value && checkOutDate.value <= this.value) {
                const nextDay = new Date(this.value);
                nextDay.setDate(nextDay.getDate() + 1);
                checkOutDate.value = nextDay.toISOString().split('T')[0];
            }
        });
        
        checkOutDate.addEventListener('change', function() {
            if (this.value <= checkInDate.value) {
                this.setCustomValidity('Check-out date must be after check-in date');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

// Gallery functionality
function initializeGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const filterButtons = document.querySelectorAll('input[name="gallery-filter"]');
    
    // Gallery filtering
    filterButtons.forEach(button => {
        button.addEventListener('change', function() {
            const filter = this.id.replace('filter-', '');
            let visibleCount = 0;
            
            galleryItems.forEach(item => {
                const category = item.dataset.category;
                const shouldShow = filter === 'all' || category === filter;
                
                if (shouldShow) {
                    item.style.display = 'block';
                    item.classList.add('fade-in');
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                    item.classList.remove('fade-in');
                }
            });
            
            // Show no results message if needed
            const noResults = document.getElementById('no-results');
            if (noResults) {
                noResults.style.display = visibleCount === 0 ? 'block' : 'none';
            }
        });
    });
    
    // Gallery item hover effects
    galleryItems.forEach(item => {
        const container = item.querySelector('.gallery-image-container');
        if (container) {
            container.addEventListener('mouseenter', function() {
                this.classList.add('hovered');
            });
            
            container.addEventListener('mouseleave', function() {
                this.classList.remove('hovered');
            });
        }
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Back to top button
function initializeBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary back-to-top';
    backToTopBtn.setAttribute('aria-label', 'Back to top');
    backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    
    document.body.appendChild(backToTopBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    // Scroll to top when clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Auto-dismiss alerts
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-dismiss success alerts after 5 seconds
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

// Utility functions
const Utils = {
    // Debounce function for performance
    debounce: function(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Show loading state
    showLoading: function(element) {
        element.classList.add('loading');
        element.style.pointerEvents = 'none';
    },
    
    // Hide loading state
    hideLoading: function(element) {
        element.classList.remove('loading');
        element.style.pointerEvents = 'auto';
    },
    
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }
};

// Initialize additional features on load
window.addEventListener('load', function() {
    initializeSmoothScroll();
    initializeBackToTop();
    initializeAlerts();
});

// Export for use in other scripts
window.OasisHotel = {
    Utils: Utils
};
