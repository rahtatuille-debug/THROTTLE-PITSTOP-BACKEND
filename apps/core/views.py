from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """Simple endpoint so the frontend can confirm it's talking to the API."""
    return Response({"status": "ok", "service": "throttle-pitstop-backend"})
