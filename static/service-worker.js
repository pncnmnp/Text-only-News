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
// https://serviceworke.rs/strategy-cache-update-and-refresh_service-worker_doc.html

self.addEventListener('fetch', function(event) {
	console.log('Fetch intercepted for:', event.request.url);
	event.respondWith(fromCache(event.request));
	event.waitUntil(update(event.request).then(refresh));
});

function fromCache(request) {
	return caches.open(cacheName).then(function (cache) {
		return cache.match(request);
	});
}

function update(request) {
	return caches.open(cacheName).then(function (cache) {
		return fetch(request).then(function (response) {
			return cache.put(request, response.clone()).then(function () {
				return response;
			});
		});
	});
}

function refresh(response) {
	return self.clients.matchAll().then(function (clients) {
		clients.forEach(function (client) {
			var message = {
				type: 'refresh',
				url: response.url,
				eTag: response.headers.get('ETag')
			};
			client.postMessage(JSON.stringify(message));
		});
	});
}