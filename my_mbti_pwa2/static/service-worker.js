self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('my-cache').then(cache => {
            return cache.addAll([
                '/',
                '/index.html',
                '/styles.css',
                '/main.js',
                '/mbti_data.json',
                '/manifest.json',
                '/images/INTJ.png',
                '/images/INTP.png',
                '/images/ENTJ.png',
                '/images/ENTP.png',
                '/images/INFJ.png',
                '/images/INFP.png',
                '/images/ENFJ.png',
                '/images/ENFP.png',
                '/images/ISTJ.png',
                '/images/ISFJ.png',
                '/images/ESTJ.png',
                '/images/ESFJ.png',
                '/images/ISTP.png',
                '/images/ISFP.png',
                '/images/ESTP.png',
                '/images/ESFP.png'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
