self.addEventListener('install', function(event) {
    console.log('Service Worker installing.');
    // Perform install steps if necessary
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker activating.');
    // Perform activate steps if necessary
});

self.addEventListener('fetch', function(event) {
    console.log('Fetching:', event.request.url);
    event.respondWith(
        caches.match(event.request).then(function(response) {
            // Cache hit - return response
            if (response) {
                return response;
            }

            // IMPORTANT: Clone the request. A request is a stream and can only be consumed once.
            // Since we are consuming this once by cache and once by the browser for fetch, we need to clone the response.
            var fetchRequest = event.request.clone();

            return fetch(fetchRequest).then(
                function(response) {
                    // Check if we received a valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    // IMPORTANT: Clone the response. A response is a stream and because we want the browser to consume the response as well as the cache consuming the response, we need to clone it so we have two streams.
                    var responseToCache = response.clone();

                    caches.open('my-site-cache-v1')
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                }
            );
        })
    );
});
