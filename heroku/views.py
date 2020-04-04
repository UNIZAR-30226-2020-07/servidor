import json

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def webhook(request):
    try:
        petition = json.loads(request.body)
        data = {
            "content": f"Heroku {petition['action']} at {petition['created_at']}",
            "username": "Heroku",
        }
    except Exception as e:
        data = {
            "content": f"Error on webhook: {e}",
            "username": "Heroku",
        }

    url = "https://discordapp.com/api/webhooks/420245807418310666/PTeD3_vCsV4iLsZKbZWNL2Mf5MOz2JdqSUnZg6IdP-Z-HdVhCWXRZUKSn8OBpgf3yn-z"

    requests.post(url, data=data)

    return HttpResponse(status=204)
