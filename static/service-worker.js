const cacheName = 'cache-v1';
const precacheResources = [
	'/english',
	'/hindi',
	'/static/common_styles.css'
];

self.addEventListener('install', event => {
	console.log('Service worker install event!');
	event.waitUntil(
		caches.open(cacheName)
			.then(cache => {
				return cache.addAll(precacheResources);
			})
	);
});

self.addEventListener('activate', event => {
	console.log('Service worker activate event!');
});

// The below event listener is from 
// https://developers.google.com/web/ilt/pwa/caching-files-with-service-worker

self.addEventListener('fetch', function(event) {
	event.respondWith(
		fetch(event.request).catch(function() {
			return caches.match(event.request);
		})
	);
});