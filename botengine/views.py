import json

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

from django.conf import settings

from .bot import *


def test(request):
    print(dir(request), dir(request.GET.keys()))
    return HttpResponse('<h1>ТЕСТ</h1>')


@csrf_exempt
def vk_hook(request):
    if (request.method == "POST"):
        # confirmation
        print(json.loads(request.body))
        raw_event = json.loads(request.body)
        if raw_event['type'] == 'confirmation':
            if raw_event['secret'] != settings.VK_SECRET:
                return HttpResponse('see you :)')
            else:
                return HttpResponse(settings.VK_SERVER_CONFIRM)
        if (raw_event['secret'] == settings.VK_SECRET):
            print(type(raw_event), raw_event)
            if raw_event['object']['from_id'] == raw_event['object']['peer_id']:
                print('Сообщение в ЛС')
                no_pm(raw_event)
            elif (raw_event['type'] == 'message_new'):
                user_id = raw_event['object']['from_id']
                print(user_id, raw_event)
                bot_handler(raw_event)
            return HttpResponse('ok', content_type="text/plain", status=200)
        else:
            return HttpResponse('see you :)')
