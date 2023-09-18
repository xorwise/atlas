const cacheName = "your-pwa-cache";
const filesToCache = [
  // "/static/ePubViewer/index.html",
  "/static/ePubViewer/style.css",
  "/static/ePubViewer/script.js",
  "/static/ePubViewer/service-worker.js",
  "/static/ePubViewer/sw.js",
  "/static/ePubViewer/libs/epub.js",
  "/static/ePubViewer/libs/epub.js.diff",
  "/static/ePubViewer/libs/epub.orig.js",
  "/static/ePubViewer/libs/jszip.min.js",
  "/static/ePubViewer/libs/normalize.min.css",
  "/static/ePubViewer/libs/sanitize-html.min.js",
  "/static/ePubViewer/polyfills/fetch.js",
  "/static/ePubViewer/polyfills/pep.min.js",
  "/static/ePubViewer/polyfills/babel-polyfill.min.js",
  // Add other assets and pages you want to cache
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(cacheName).then((cache) => {
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
