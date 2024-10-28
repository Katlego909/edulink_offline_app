const CACHE_NAME = 'static-cache-v1'; // Versioning for cache
const urlsToCache = [
    '/',
    '/static/images/icons/icon-192x192.png',
    '/static/images/icons/icon-512x512.png',
    '/static/manifest.json',
    '/static/css/styles.css',
    '/offline.html', // Add your offline page here// Add your offline page here
];

// Install event to cache resources
self.addEventListener('install', (event) => {
    self.skipWaiting();  // Activate new service worker immediately
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Opened cache and cached resources');
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Only handle GET requests
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) {
                return response; // Serve from cache if available
            }
            return fetch(event.request).then((fetchResponse) => {
                const url = event.request.url;

                // Cache course content
                if (url.includes('/courses/course/') || url.includes('/lessons/') || url.includes('/chapters/')) {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, fetchResponse.clone());
                        return fetchResponse; // Return the fresh response
                    });
                }
                return fetchResponse; // Return the response for other requests
            }).catch(() => {
                // Return offline page if available
                return caches.match('/offline.html');
            });
        })
    );
});

// Activate event to clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim(); // Take control of the page immediately
});
