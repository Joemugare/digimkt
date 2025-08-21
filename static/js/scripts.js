// Enhanced Scripts for DigitalHub
// This file contains non-critical JavaScript functionality

(function() {
    'use strict';
    
    // Wait for main app to be ready
    const waitForApp = () => {
        return new Promise((resolve) => {
            if (window.app) {
                resolve(window.app);
            } else {
                document.addEventListener('DOMContentLoaded', () => {
                    const checkApp = () => {
                        if (window.app) {
                            resolve(window.app);
                        } else {
                            setTimeout(checkApp, 50);
                        }
                    };
                    checkApp();
                });
            }
        });
    };

    // Enhanced features
    class EnhancedFeatures {
        constructor(app) {
            this.app = app;
            this.init();
        }

        init() {
            this.setupAnalytics();
            this.setupSocialSharing();
            this.setupImageLazyLoading();
            this.setupFormEnhancements();
            this.setupAccessibility();
            this.setupPerformanceMonitoring();
        }

        setupAnalytics() {
            // Enhanced analytics tracking
            this.trackPageView();
            this.trackUserEngagement();
            this.trackPerformance();
        }

        trackPageView() {
            if (typeof gtag !== 'undefined') {
                gtag('config', 'G-GHEQ6TQTFY', {
                    page_title: document.title,
                    page_location: window.location.href,
                    custom_map: {
                        'dimension1': 'user_type',
                        'dimension2': 'content_category'
                    }
                });
            }
        }

        trackUserEngagement() {
            let engagementStartTime = Date.now();
            let isEngaged = false;

            // Track scroll depth
            let maxScrollDepth = 0;
            const trackScroll = () => {
                const scrollDepth = Math.round(
                    (window.pageYOffset / (document.body.scrollHeight - window.innerHeight)) * 100
                );
                
                if (scrollDepth > maxScrollDepth) {
                    maxScrollDepth = scrollDepth;
                    
                    // Track milestone scroll depths
                    if (scrollDepth >= 25 && scrollDepth < 50 && maxScrollDepth < 25) {
                        this.trackEvent('scroll', 'depth', '25%');
                    } else if (scrollDepth >= 50 && scrollDepth < 75 && maxScrollDepth < 50) {
                        this.trackEvent('scroll', 'depth', '50%');
                    } else if (scrollDepth >= 75 && scrollDepth < 90 && maxScrollDepth < 75) {
                        this.trackEvent('scroll', 'depth', '75%');
                    } else if (scrollDepth >= 90 && maxScrollDepth < 90) {
                        this.trackEvent('scroll', 'depth', '90%');
                    }
                }
            };

            // Track time on page
            const trackEngagement = () => {
                const timeSpent = Date.now() - engagementStartTime;
                
                if (!isEngaged && timeSpent > 30000) { // 30 seconds
                    isEngaged = true;
                    this.trackEvent('engagement', 'time_on_page', '30_seconds');
                }
            };

            // Add throttled listeners
            let scrollTimeout;
            window.addEventListener('scroll', () => {
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(trackScroll, 100);
            }, { passive: true });

            setInterval(trackEngagement, 10000); // Check every 10 seconds

            // Track clicks on important elements
            document.addEventListener('click', (e) => {
                const target = e.target.closest('a, button, .card, .btn');
                if (target) {
                    this.trackEvent('click', target.tagName.toLowerCase(), target.textContent?.substring(0, 50) || 'unknown');
                }
            });
        }

        trackPerformance() {
            // Track Core Web Vitals
            if ('PerformanceObserver' in window) {
                // Largest Contentful Paint
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.startTime < performance.now()) {
                            this.trackEvent('performance', 'LCP', Math.round(entry.startTime));
                        }
                    }
                }).observe({ entryTypes: ['largest-contentful-paint'] });

                // First Input Delay
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        this.trackEvent('performance', 'FID', Math.round(entry.processingStart - entry.startTime));
                    }
                }).observe({ entryTypes: ['first-input'] });

                // Cumulative Layout Shift
                let clsScore = 0;
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            clsScore += entry.value;
                        }
                    }
                    this.trackEvent('performance', 'CLS', Math.round(clsScore * 1000));
                }).observe({ entryTypes: ['layout-shift'] });
            }
        }

        trackEvent(category, action, label, value) {
            if (typeof gtag !== 'undefined') {
                gtag('event', action, {
                    event_category: category,
                    event_label: label,
                    value: value
                });
            }
        }

        setupSocialSharing() {
            // Enhanced social sharing
            window.shareContent = (platform, options = {}) => {
                const defaults = {
                    url: window.location.href,
                    title: document.title,
                    text: document.querySelector('meta[name="description"]')?.content || '',
                    hashtags: ['DigitalMarketing', 'DigitalHub']
                };

                const config = { ...defaults, ...options };
                
                const shareUrls = {
                    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(config.url)}`,
                    twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(config.url)}&text=${encodeURIComponent(config.text)}&hashtags=${config.hashtags.join(',')}`,
                    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(config.url)}`,
                    whatsapp: `https://wa.me/?text=${encodeURIComponent(config.text + ' ' + config.url)}`,
                    telegram: `https://t.me/share/url?url=${encodeURIComponent(config.url)}&text=${encodeURIComponent(config.text)}`,
                    reddit: `https://reddit.com/submit?url=${encodeURIComponent(config.url)}&title=${encodeURIComponent(config.title)}`
                };

                if (shareUrls[platform]) {
                    const popup = window.open(
                        shareUrls[platform], 
                        'share', 
                        'width=600,height=400,scrollbars=yes,resizable=yes'
                    );
                    
                    this.trackEvent('social_share', platform, config.url);
                    
                    // Focus popup
                    if (popup) {
                        popup.focus();
                    }
                } else if (platform === 'native' && navigator.share) {
                    navigator.share({
                        title: config.title,
                        text: config.text,
                        url: config.url
                    }).then(() => {
                        this.trackEvent('social_share', 'native', config.url);
                    }).catch(console.error);
                }
            };

            // Copy to clipboard functionality
            window.copyToClipboard = async (text, successMsg = 'Copied to clipboard!') => {
                try {
                    if (navigator.clipboard) {
                        await navigator.clipboard.writeText(text);
                    } else {
                        // Fallback for older browsers
                        const textArea = document.createElement('textarea');
                        textArea.value = text;
                        textArea.style.position = 'fixed';
                        textArea.style.opacity = '0';
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                    }
                    
                    if (this.app && this.app.showToast) {
                        this.app.showToast(successMsg, 'success');
                    }
                    
                    this.trackEvent('action', 'copy_to_clipboard', text.substring(0, 50));
                } catch (error) {
                    console.error('Failed to copy:', error);
                    if (this.app && this.app.showToast) {
                        this.app.showToast('Failed to copy', 'error');
                    }
                }
            };
        }

        setupImageLazyLoading() {
            // Enhanced image lazy loading with progressive enhancement
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        imageObserver.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px',
                threshold: 0.01
            });

            // Observe all lazy images
            document.querySelectorAll('img[data-src]').forEach(img => {
                img.classList.add('lazy-loading');
                imageObserver.observe(img);
            });

            // Background images
            document.querySelectorAll('[data-bg]').forEach(el => {
                imageObserver.observe(el);
            });
        }

        loadImage(img) {
            return new Promise((resolve, reject) => {
                const src = img.dataset.src || img.dataset.bg;
                if (!src) {
                    resolve();
                    return;
                }

                if (img.tagName === 'IMG') {
                    img.onload = () => {
                        img.classList.remove('lazy-loading');
                        img.classList.add('lazy-loaded');
                        resolve();
                    };
                    img.onerror = reject;
                    img.src = src;
                    img.removeAttribute('data-src');
                } else {
                    // Background image
                    const testImg = new Image();
                    testImg.onload = () => {
                        img.style.backgroundImage = `url(${src})`;
                        img.classList.remove('lazy-loading');
                        img.classList.add('lazy-loaded');
                        img.removeAttribute('data-bg');
                        resolve();
                    };
                    testImg.onerror = reject;
                    testImg.src = src;
                }
            });
        }

        setupFormEnhancements() {
            // Enhanced form handling
            document.querySelectorAll('form').forEach(form => {
                this.enhanceForm(form);
            });
        }

        enhanceForm(form) {
            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearFieldError(input));
            });

            // Submit handling
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    return false;
                }
                
                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    const originalText = submitBtn.textContent;
                    submitBtn.textContent = 'Submitting...';
                    
                    // Reset after timeout (in case of network issues)
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.textContent = originalText;
                    }, 30000);
            }
        }
    }

    // Utility functions
    const Utils = {
        // Debounce function
        debounce(func, wait, immediate) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    timeout = null;
                    if (!immediate) func(...args);
                };
                const callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func(...args);
            };
        },

        // Throttle function
        throttle(func, limit) {
            let lastFunc;
            let lastRan;
            return function(...args) {
                if (!lastRan) {
                    func(...args);
                    lastRan = Date.now();
                } else {
                    clearTimeout(lastFunc);
                    lastFunc = setTimeout(() => {
                        if ((Date.now() - lastRan) >= limit) {
                            func(...args);
                            lastRan = Date.now();
                        }
                    }, limit - (Date.now() - lastRan));
                }
            };
        },

        // Animation frame throttle
        rafThrottle(func) {
            let ticking = false;
            return function(...args) {
                if (!ticking) {
                    requestAnimationFrame(() => {
                        func(...args);
                        ticking = false;
                    });
                    ticking = true;
                }
            };
        },

        // Format numbers
        formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        },

        // Format dates
        formatDate(date, options = {}) {
            const defaults = { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            };
            return new Intl.DateTimeFormat('en-US', { ...defaults, ...options }).format(date);
        },

        // Sanitize HTML
        sanitizeHTML(str) {
            const temp = document.createElement('div');
            temp.textContent = str;
            return temp.innerHTML;
        },

        // Generate unique ID
        generateId(prefix = 'id') {
            return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        },

        // Check if element is in viewport
        isInViewport(element, threshold = 0) {
            const rect = element.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;
            const windowWidth = window.innerWidth || document.documentElement.clientWidth;
            
            return (
                rect.top >= -threshold &&
                rect.left >= -threshold &&
                rect.bottom <= windowHeight + threshold &&
                rect.right <= windowWidth + threshold
            );
        },

        // Smooth scroll to element
        scrollToElement(element, options = {}) {
            const defaults = {
                behavior: 'smooth',
                block: 'start',
                inline: 'nearest'
            };
            
            if (typeof element === 'string') {
                element = document.querySelector(element);
            }
            
            if (element) {
                element.scrollIntoView({ ...defaults, ...options });
            }
        },

        // Local storage with fallback
        storage: {
            get(key, defaultValue = null) {
                try {
                    const item = localStorage.getItem(key);
                    return item ? JSON.parse(item) : defaultValue;
                } catch {
                    return defaultValue;
                }
            },

            set(key, value) {
                try {
                    localStorage.setItem(key, JSON.stringify(value));
                    return true;
                } catch {
                    return false;
                }
            },

            remove(key) {
                try {
                    localStorage.removeItem(key);
                    return true;
                } catch {
                    return false;
                }
            }
        }
    };

    // Advanced components
    class AdvancedComponents {
        constructor(app) {
            this.app = app;
            this.components = new Map();
            this.init();
        }

        init() {
            this.setupInfiniteScroll();
            this.setupImageGallery();
            this.setupTooltips();
            this.setupTabs();
            this.setupAccordions();
            this.setupCounters();
        }

        setupInfiniteScroll() {
            const containers = document.querySelectorAll('[data-infinite-scroll]');
            
            containers.forEach(container => {
                const loadMore = container.querySelector('[data-load-more]');
                if (!loadMore) return;

                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            this.loadMoreContent(container);
                        }
                    });
                }, { threshold: 0.1 });

                observer.observe(loadMore);
                this.components.set(`infinite-${container.id}`, observer);
            });
        }

        async loadMoreContent(container) {
            const loadMore = container.querySelector('[data-load-more]');
            const url = container.dataset.infiniteScroll;
            const page = parseInt(container.dataset.page || '1') + 1;

            if (loadMore.classList.contains('loading')) return;

            loadMore.classList.add('loading');
            loadMore.textContent = 'Loading...';

            try {
                const response = await fetch(`${url}?page=${page}`);
                const data = await response.json();

                if (data.html) {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = data.html;
                    
                    const newItems = tempDiv.children;
                    Array.from(newItems).forEach(item => {
                        container.insertBefore(item, loadMore);
                        item.style.opacity = '0';
                        item.style.transform = 'translateY(20px)';
                        
                        requestAnimationFrame(() => {
                            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0)';
                        });
                    });

                    container.dataset.page = page.toString();

                    if (!data.has_next) {
                        loadMore.style.display = 'none';
                    }
                }
            } catch (error) {
                console.error('Failed to load more content:', error);
                if (this.app.showToast) {
                    this.app.showToast('Failed to load more content', 'error');
                }
            } finally {
                loadMore.classList.remove('loading');
                loadMore.textContent = 'Load More';
            }
        }

        setupImageGallery() {
            const galleries = document.querySelectorAll('[data-gallery]');
            
            galleries.forEach(gallery => {
                const images = gallery.querySelectorAll('img');
                
                images.forEach((img, index) => {
                    img.addEventListener('click', () => {
                        this.openLightbox(images, index);
                    });
                    img.style.cursor = 'pointer';
                });
            });
        }

        openLightbox(images, startIndex = 0) {
            const lightbox = this.createLightbox();
            let currentIndex = startIndex;

            const showImage = (index) => {
                const img = lightbox.querySelector('.lightbox-image');
                const counter = lightbox.querySelector('.lightbox-counter');
                
                img.src = images[index].src;
                img.alt = images[index].alt || '';
                counter.textContent = `${index + 1} / ${images.length}`;
                
                currentIndex = index;
            };

            const nextImage = () => {
                currentIndex = (currentIndex + 1) % images.length;
                showImage(currentIndex);
            };

            const prevImage = () => {
                currentIndex = (currentIndex - 1 + images.length) % images.length;
                showImage(currentIndex);
            };

            // Event listeners
            lightbox.querySelector('.lightbox-next').addEventListener('click', nextImage);
            lightbox.querySelector('.lightbox-prev').addEventListener('click', prevImage);
            lightbox.querySelector('.lightbox-close').addEventListener('click', () => {
                this.closeLightbox(lightbox);
            });

            // Keyboard navigation
            const handleKeydown = (e) => {
                switch (e.key) {
                    case 'ArrowRight':
                        nextImage();
                        break;
                    case 'ArrowLeft':
                        prevImage();
                        break;
                    case 'Escape':
                        this.closeLightbox(lightbox);
                        break;
                }
            };

            document.addEventListener('keydown', handleKeydown);
            lightbox.addEventListener('remove', () => {
                document.removeEventListener('keydown', handleKeydown);
            });

            showImage(startIndex);
            document.body.appendChild(lightbox);
            
            requestAnimationFrame(() => {
                lightbox.classList.add('active');
            });
        }

        createLightbox() {
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = `
                <div class="lightbox-backdrop"></div>
                <div class="lightbox-container">
                    <button class="lightbox-close" aria-label="Close">&times;</button>
                    <button class="lightbox-prev" aria-label="Previous">&larr;</button>
                    <button class="lightbox-next" aria-label="Next">&rarr;</button>
                    <img class="lightbox-image" src="" alt="">
                    <div class="lightbox-counter"></div>
                </div>
            `;
            return lightbox;
        }

        closeLightbox(lightbox) {
            lightbox.classList.remove('active');
            setTimeout(() => {
                lightbox.dispatchEvent(new Event('remove'));
                lightbox.remove();
            }, 300);
        }

        setupTooltips() {
            const tooltipElements = document.querySelectorAll('[data-tooltip]');
            
            tooltipElements.forEach(element => {
                let tooltip;
                
                const showTooltip = (e) => {
                    tooltip = this.createTooltip(element.dataset.tooltip);
                    document.body.appendChild(tooltip);
                    this.positionTooltip(tooltip, element, e);
                    
                    requestAnimationFrame(() => {
                        tooltip.classList.add('show');
                    });
                };

                const hideTooltip = () => {
                    if (tooltip) {
                        tooltip.classList.remove('show');
                        setTimeout(() => tooltip.remove(), 200);
                        tooltip = null;
                    }
                };

                element.addEventListener('mouseenter', showTooltip);
                element.addEventListener('mouseleave', hideTooltip);
                element.addEventListener('focus', showTooltip);
                element.addEventListener('blur', hideTooltip);
            });
        }

        createTooltip(text) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = text;
            tooltip.setAttribute('role', 'tooltip');
            return tooltip;
        }

        positionTooltip(tooltip, element, event) {
            const rect = element.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();
            
            let top = rect.top - tooltipRect.height - 5;
            let left = rect.left + (rect.width - tooltipRect.width) / 2;

            // Adjust if tooltip goes off-screen
            if (top < 0) {
                top = rect.bottom + 5;
                tooltip.classList.add('bottom');
            }

            if (left < 0) {
                left = 5;
            } else if (left + tooltipRect.width > window.innerWidth) {
                left = window.innerWidth - tooltipRect.width - 5;
            }

            tooltip.style.top = `${top + window.pageYOffset}px`;
            tooltip.style.left = `${left}px`;
        }

        setupTabs() {
            const tabContainers = document.querySelectorAll('[data-tabs]');
            
            tabContainers.forEach(container => {
                const tabs = container.querySelectorAll('[data-tab]');
                const panels = container.querySelectorAll('[data-panel]');
                
                tabs.forEach(tab => {
                    tab.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.switchTab(tab, tabs, panels);
                    });
                });

                // Keyboard navigation
                container.addEventListener('keydown', (e) => {
                    if (e.target.matches('[data-tab]')) {
                        let nextTab;
                        const currentIndex = Array.from(tabs).indexOf(e.target);
                        
                        switch (e.key) {
                            case 'ArrowRight':
                                nextTab = tabs[(currentIndex + 1) % tabs.length];
                                break;
                            case 'ArrowLeft':
                                nextTab = tabs[(currentIndex - 1 + tabs.length) % tabs.length];
                                break;
                            case 'Home':
                                nextTab = tabs[0];
                                break;
                            case 'End':
                                nextTab = tabs[tabs.length - 1];
                                break;
                        }
                        
                        if (nextTab) {
                            e.preventDefault();
                            nextTab.focus();
                            this.switchTab(nextTab, tabs, panels);
                        }
                    }
                });
            });
        }

        switchTab(activeTab, allTabs, allPanels) {
            const targetPanel = activeTab.dataset.tab;
            
            // Update tabs
            allTabs.forEach(tab => {
                tab.classList.remove('active');
                tab.setAttribute('aria-selected', 'false');
                tab.setAttribute('tabindex', '-1');
            });
            
            activeTab.classList.add('active');
            activeTab.setAttribute('aria-selected', 'true');
            activeTab.setAttribute('tabindex', '0');
            
            // Update panels
            allPanels.forEach(panel => {
                panel.classList.remove('active');
                panel.setAttribute('aria-hidden', 'true');
            });
            
            const targetPanelEl = document.querySelector(`[data-panel="${targetPanel}"]`);
            if (targetPanelEl) {
                targetPanelEl.classList.add('active');
                targetPanelEl.setAttribute('aria-hidden', 'false');
            }
        }

        setupAccordions() {
            const accordions = document.querySelectorAll('[data-accordion]');
            
            accordions.forEach(accordion => {
                const headers = accordion.querySelectorAll('[data-accordion-header]');
                
                headers.forEach(header => {
                    header.addEventListener('click', () => {
                        this.toggleAccordion(header, accordion);
                    });
                    
                    // Make focusable
                    if (!header.hasAttribute('tabindex')) {
                        header.setAttribute('tabindex', '0');
                    }
                    
                    header.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            this.toggleAccordion(header, accordion);
                        }
                    });
                });
            });
        }

        toggleAccordion(header, accordion) {
            const content = header.nextElementSibling;
            const isExpanded = header.getAttribute('aria-expanded') === 'true';
            const allowMultiple = accordion.dataset.accordion === 'multiple';
            
            if (!allowMultiple) {
                // Close other accordion items
                accordion.querySelectorAll('[data-accordion-header]').forEach(otherHeader => {
                    if (otherHeader !== header) {
                        otherHeader.setAttribute('aria-expanded', 'false');
                        otherHeader.classList.remove('active');
                        const otherContent = otherHeader.nextElementSibling;
                        if (otherContent) {
                            otherContent.style.height = '0';
                            otherContent.classList.remove('active');
                        }
                    }
                });
            }
            
            // Toggle current item
            header.setAttribute('aria-expanded', !isExpanded);
            header.classList.toggle('active');
            
            if (content) {
                if (isExpanded) {
                    content.style.height = '0';
                    content.classList.remove('active');
                } else {
                    content.style.height = content.scrollHeight + 'px';
                    content.classList.add('active');
                }
            }
        }

        setupCounters() {
            const counters = document.querySelectorAll('[data-counter]');
            
            const animateCounter = (counter) => {
                const target = parseInt(counter.dataset.counter);
                const duration = parseInt(counter.dataset.duration || '2000');
                const start = 0;
                const startTime = performance.now();
                
                const updateCounter = (currentTime) => {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    
                    // Easing function
                    const easeOutQuart = 1 - Math.pow(1 - progress, 4);
                    const current = Math.floor(easeOutQuart * target);
                    
                    counter.textContent = Utils.formatNumber(current);
                    
                    if (progress < 1) {
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = Utils.formatNumber(target);
                    }
                };
                
                requestAnimationFrame(updateCounter);
            };
            
            // Use Intersection Observer to trigger when visible
            const counterObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });
            
            counters.forEach(counter => {
                counterObserver.observe(counter);
            });
        }

        destroy() {
            this.components.forEach(component => {
                if (component && component.disconnect) {
                    component.disconnect();
                }
            });
            this.components.clear();
        }
    }

    // Initialize enhanced features when app is ready
    waitForApp().then(app => {
        window.enhancedFeatures = new EnhancedFeatures(app);
        window.advancedComponents = new AdvancedComponents(app);
        window.Utils = Utils;
        
        console.log('Enhanced features loaded successfully');
    });

    // Expose utilities globally
    window.Utils = Utils;

})();
                }
            });
        }

        validateField(field) {
            const value = field.value.trim();
            const type = field.type;
            let isValid = true;
            let message = '';

            // Required validation
            if (field.required && !value) {
                isValid = false;
                message = 'This field is required';
            }
            // Email validation
            else if (type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                isValid = false;
                message = 'Please enter a valid email address';
            }
            // URL validation
            else if (type === 'url' && value && !/^https?:\/\/.+/.test(value)) {
                isValid = false;
                message = 'Please enter a valid URL';
            }
            // Phone validation
            else if (type === 'tel' && value && !/^[\d\s\-\+\(\)]+$/.test(value)) {
                isValid = false;
                message = 'Please enter a valid phone number';
            }

            this.showFieldValidation(field, isValid, message);
            return isValid;
        }

        validateForm(form) {
            const fields = form.querySelectorAll('input, textarea, select');
            let isValid = true;

            fields.forEach(field => {
                if (!this.validateField(field)) {
                    isValid = false;
                }
            });

            return isValid;
        }

        showFieldValidation(field, isValid, message) {
            // Remove existing error
            this.clearFieldError(field);

            if (!isValid) {
                field.classList.add('error');
                
                const errorEl = document.createElement('div');
                errorEl.className = 'field-error';
                errorEl.textContent = message;
                errorEl.setAttribute('role', 'alert');
                
                field.parentNode.appendChild(errorEl);
            } else {
                field.classList.remove('error');
                field.classList.add('valid');
            }
        }

        clearFieldError(field) {
            field.classList.remove('error');
            const error = field.parentNode.querySelector('.field-error');
            if (error) {
                error.remove();
            }
        }

        setupAccessibility() {
            // Enhanced accessibility features
            this.setupKeyboardNavigation();
            this.setupFocusManagement();
            this.setupARIA();
        }

        setupKeyboardNavigation() {
            // Better keyboard navigation
            document.addEventListener('keydown', (e) => {
                // Skip navigation with Tab
                if (e.key === 'Tab') {
                    this.highlightFocusedElement();
                }
                
                // Close modals with Escape
                if (e.key === 'Escape') {
                    this.closeAllModals();
                }
                
                // Navigation with arrow keys in grid layouts
                if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                    this.handleArrowNavigation(e);
                }
            });
        }

        highlightFocusedElement() {
            // Add visual focus indicators
            document.body.classList.add('keyboard-navigation');
            
            // Remove class when mouse is used
            document.addEventListener('mousedown', () => {
                document.body.classList.remove('keyboard-navigation');
            }, { once: true });
        }

        closeAllModals() {
            document.querySelectorAll('.modal.active, .search-modal.active').forEach(modal => {
                modal.classList.remove('active');
            });
        }

        handleArrowNavigation(e) {
            // Implement arrow key navigation for card grids
            const focusedElement = document.activeElement;
            const cardGrid = focusedElement.closest('.card-grid');
            
            if (!cardGrid) return;
            
            const cards = Array.from(cardGrid.querySelectorAll('.card, .grid-item'));
            const currentIndex = cards.indexOf(focusedElement.closest('.card, .grid-item'));
            
            if (currentIndex === -1) return;
            
            let nextIndex;
            const cardsPerRow = Math.floor(cardGrid.offsetWidth / cards[0].offsetWidth);
            
            switch (e.key) {
                case 'ArrowLeft':
                    nextIndex = currentIndex - 1;
                    break;
                case 'ArrowRight':
                    nextIndex = currentIndex + 1;
                    break;
                case 'ArrowUp':
                    nextIndex = currentIndex - cardsPerRow;
                    break;
                case 'ArrowDown':
                    nextIndex = currentIndex + cardsPerRow;
                    break;
            }
            
            if (nextIndex >= 0 && nextIndex < cards.length) {
                e.preventDefault();
                const nextCard = cards[nextIndex];
                const focusableEl = nextCard.querySelector('a, button') || nextCard;
                focusableEl.focus();
            }
        }

        setupFocusManagement() {
            // Manage focus for modals and dynamic content
            document.addEventListener('click', (e) => {
                if (e.target.matches('[data-toggle="modal"]')) {
                    setTimeout(() => {
                        const modal = document.querySelector(e.target.getAttribute('data-target'));
                        if (modal) {
                            const firstFocusable = modal.querySelector('input, button, a, [tabindex]:not([tabindex="-1"])');
                            if (firstFocusable) {
                                firstFocusable.focus();
                            }
                        }
                    }, 100);
                }
            });
        }

        setupARIA() {
            // Enhanced ARIA attributes
            document.querySelectorAll('[data-toggle]').forEach(toggle => {
                const target = document.querySelector(toggle.getAttribute('data-target'));
                if (target) {
                    toggle.setAttribute('aria-controls', target.id || `target-${Date.now()}`);
                    toggle.setAttribute('aria-expanded', 'false');
                    
                    toggle.addEventListener('click', () => {
                        const expanded = toggle.getAttribute('aria-expanded') === 'true';
                        toggle.setAttribute('aria-expanded', !expanded);
                    });
                }
            });
        }

        setupPerformanceMonitoring() {
            // Monitor and report performance issues
            if ('PerformanceObserver' in window) {
                // Monitor long tasks
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.duration > 50) {
                            console.warn('Long task detected:', entry);
                            this.trackEvent('performance', 'long_task', entry.name, entry.duration);
                        }
                    }
                }).observe({ entryTypes: ['longtask'] });

                // Monitor resource loading
                new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.duration > 1000) {
                            console.warn('Slow resource:', entry.name, entry.duration);
                            this.trackEvent('performance', 'slow_resource', entry.name, entry.duration);
                        }
                    }
                }).observe({ entryTypes: ['resource'] });
            }

            // Memory usage monitoring
            if ('memory' in performance) {
                setInterval(() => {
                    const memory = performance.memory;
                    if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.9) {
                        console.warn('High memory usage detected');
                        this.trackEvent('performance', 'high_memory_usage', 'warning', memory.usedJSHeapSize);
                    }
                }, 30000);