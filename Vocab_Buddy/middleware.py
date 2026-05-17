from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """Middleware that requires a user to be authenticated to view any page.

    Exemptions are paths under `/auth/`, `/static/`, `/admin/`, and common public files.
    Redirects unauthenticated users to the login page with `next` parameter.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If user is authenticated, proceed
        if getattr(request, 'user', None) and request.user.is_authenticated:
            return self.get_response(request)

        path = request.path_info or request.path

        # Allow listed public paths
        public_prefixes = [
            settings.STATIC_URL,
            '/static/',
            '/auth/',
            '/admin/',
            '/media/',
            '/favicon.ico',
            '/robots.txt',
            '/manifest.webmanifest',
            '/service-worker.js',
        ]

        for prefix in public_prefixes:
            if path.startswith(prefix):
                return self.get_response(request)

        # Resolve login URL (handles both URL names and paths)
        try:
            login_url = reverse(settings.LOGIN_URL)
        except:
            login_url = settings.LOGIN_URL if hasattr(settings, 'LOGIN_URL') else '/auth/login/'

        # Allow login page itself
        if path.startswith(login_url):
            return self.get_response(request)

        # Otherwise redirect to login with next param
        return redirect(f"{login_url}?next={request.path}")
