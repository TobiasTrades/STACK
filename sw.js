/* Lets the browser install Stack as an app. Always fetches fresh data from the network. */
self.addEventListener("install", function(){ self.skipWaiting(); });
self.addEventListener("activate", function(e){ e.waitUntil(self.clients.claim()); });
self.addEventListener("fetch", function(e){ e.respondWith(fetch(e.request)); });
