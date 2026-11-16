/* STACK PWA cache: shell available offline; fresh data preferred when online. */
var CACHE = "stack-shell-v2";
var SHELL = ["./","./index.html","./manifest.webmanifest","./icon-192.png","./icon-512.png","./apple-touch-icon.png","./assets/mary-poppins-storybook.webp","./assets/london-storybook-background.webp"];
self.addEventListener("install",function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(SHELL);}).catch(function(){}).then(function(){return self.skipWaiting();}));
});
self.addEventListener("activate",function(e){
  e.waitUntil(caches.keys().then(function(keys){return Promise.all(keys.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));
});
self.addEventListener("fetch",function(e){
  var req=e.request, url=new URL(req.url);
  if(req.method!=="GET" || url.origin!==self.location.origin) return;
  if(req.mode==="navigate" || url.pathname.endsWith(".json") || url.pathname.endsWith(".html")){
    e.respondWith(fetch(req).then(function(res){if(res && res.ok){var copy=res.clone();caches.open(CACHE).then(function(c){c.put(req,copy);});}return res;}).catch(function(){return caches.match(req).then(function(hit){return hit || caches.match("./index.html");});}));
    return;
  }
  e.respondWith(caches.match(req).then(function(hit){if(hit)return hit;return fetch(req).then(function(res){if(res && res.ok){var copy=res.clone();caches.open(CACHE).then(function(c){c.put(req,copy);});}return res;});}));
});