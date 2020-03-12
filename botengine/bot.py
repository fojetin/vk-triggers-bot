# -*- coding: utf-8 -*-
import random
import re

from django.conf import settings

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from botengine.models import Answer, OneTextTrigger, RegexTrigger, TextTrigger, Trigger


def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])


def bot_handler(raw_event):
    vk_session = vk_api.VkApi(token=settings.VK_BOT_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, settings.VK_GROUP_ID)

    event = longpoll._parse_event(raw_event)
    lazy_logg(event)

    if not event.obj.text:
        return
    text = event.obj.text.lower()

    regex_triggers = RegexTrigger.objects.all()
    text_triggers = OneTextTrigger.objects.all()

    for trigger in regex_triggers:
        # reg exps
        match = re.match(trigger.reg_exp, text.lower())
        if match:
            answer = trigger.answer
            break
    else:
        # text exps
        for trigger in [(trigger.text.lower(),
                        trigger.text_trigger.id,
                        trigger.text_trigger.entry)
                        for trigger
                        in text_triggers]:
            if trigger[2]:
                # Вхождение
                if trigger[0] in text.lower().split():
                    answer = Answer.objects.get(trigger__pk=trigger[1])
                    break
                pass
            else:
                # Совпадение
                if trigger[0].lower() == text.lower():
                    answer = Answer.objects.get(trigger__pk=trigger[1])
                    break
        else:
            # Ничего не совпало
            return

    print(answer)
    if answer.media_attachment:
        vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                attachment=answer.media_attachment,
        )
    else:
        vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message=answer.text,
        )


def lazy_logg(event):
    print('Новое сообщение:')
    print('От:', event.obj.from_id)
    print('Текст:', event.obj.text)
