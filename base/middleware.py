from movieplanet.middleware import AuthMiddlewere
from backend.middleware import DashboardMiddlewere

class ConditionalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth_middleware = AuthMiddlewere(get_response)
        self.dashboard_middleware = DashboardMiddlewere(get_response)

    def __call__(self, request):
        path = request.path

        if path.startswith('/movieplanet/'):
            return self.auth_middleware(request)

        elif path.startswith('/backend/'):
            return self.dashboard_middleware(request)

        # Default path - no custom middleware
        return self.get_response(request)