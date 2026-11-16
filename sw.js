/* STACK offline shell v6. Network-first HTML and safe offline image cache. */
const CACHE = "stack-shell-v6-20261116";
const SHELL = ["./","./index.html","./manifest.webmanifest","./icon-192.png","./icon-512.png","./apple-touch-icon.png",
"./home-mary-flying.webp","./list-mary-umbrella.webp","./deals-mary-market.webp","./coupons-mary-carpetbag.webp",
"./eat-mary-london-evening.webp","./family-mary-cherry-lane.webp","./home-rooftops.webp","./list-checking-list.webp",
"./deals-market-stall.webp","./coupons-bargain.webp","./eat-tea-cafe.webp","./date-night-london.webp",
"./rx-mary-first-aid.webp","./stores-flower-shop.webp","./faves-cat-companion.webp","./history-city-sunset.webp",
"./household-banks-family.webp","./family-storytime.webp","./settings-mary-umbrella.webp",
"./about-london-flight.webp","./help-umbrella-stilllife.webp","./cherry-tree-lane.webp"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{
 const req=e.request,url=new URL(req.url);
 if(req.method!=="GET"||url.origin!==self.location.origin)return;
 if(req.mode==="navigate"||url.pathname.endsWith(".html")||url.pathname.endsWith(".json")){
   e.respondWith(fetch(req).then(res=>{if(res.ok){const copy=res.clone();caches.open(CACHE).then(c=>c.put(req,copy));}return res;}).catch(()=>caches.match(req).then(hit=>hit||caches.match("./index.html"))));
   return;
 }
 e.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(res=>{if(res.ok){const copy=res.clone();caches.open(CACHE).then(c=>c.put(req,copy));}return res;})));
});
