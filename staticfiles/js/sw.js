const CACHE_NAME = 'digitalhub-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/styles.css',
    '/static/js/scripts.js',
    '/static/images/Digitalhub.png',
    '/static/images/favicon.ico',
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                return response || fetch(event.request);
            })
    );
});