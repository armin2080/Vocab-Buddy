import json

from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse


def manifest(request):
    payload = {
        'name': 'Vocab Buddy',
        'short_name': 'Vocab Buddy',
        'id': reverse('home'),
        'start_url': reverse('home'),
        'scope': '/',
        'display': 'standalone',
        'background_color': '#FAFAF9',
        'theme_color': '#5B7FFF',
        'description': 'Learn German vocabulary with spaced repetition and flashcards.',
        'icons': [
            {
                'src': static('icons/icon-192.png'),
                'sizes': '192x192',
                'type': 'image/png',
                'purpose': 'any',
            },
            {
                'src': static('icons/icon-512.png'),
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'any',
            },
            {
                'src': static('icons/icon-maskable-512.png'),
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'maskable any',
            },
        ],
    }
    return HttpResponse(json.dumps(payload), content_type='application/manifest+json')


def service_worker(request):
    assets_to_cache = [
        static('css/fonts.css'),
        f"{static('css/theme.css')}?v=4",
        f"{static('js/ui.js')}?v=9",
        f"{static('js/verb-panel.js')}?v=1",
        static('icons/icon-192.png'),
        static('icons/icon-512.png'),
        static('icons/apple-touch-icon.png'),
    ]

    script = f"""
const CACHE_NAME = 'vocab-buddy-pwa-v10';
const ASSETS = {json.dumps(assets_to_cache)};

self.addEventListener('install', (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
}});

self.addEventListener('activate', (event) => {{
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
    ))
  );
  self.clients.claim();
}});

self.addEventListener('fetch', (event) => {{
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  if (!url.pathname.startsWith('/static/')) return;

  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => {{
      const cloned = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
      return response;
    }}))
  );
}});
"""

    response = HttpResponse(script, content_type='application/javascript')
    response['Cache-Control'] = 'no-store'
    response['Service-Worker-Allowed'] = '/'
    return response
