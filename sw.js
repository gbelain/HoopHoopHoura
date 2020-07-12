const staticAssets = ["./", "./styles.css", "./app.js"]; // sert à mettre dans le cache les composants statiques de l'app

self.addEventListener("install", async (event) => {
  const cache = await caches.open("hoop-static");
  cache.addAll(staticAssets);
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  event.respondWith(cacheFirst(req));
});

async function cacheFirst(req) {
  const cachedResponse = await caches.match(req); // match retourne ce qui correspond à la requête dans le cache ou undefined
  return cachedResponse || fetch(req);
}
