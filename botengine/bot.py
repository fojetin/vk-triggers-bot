# -*- coding: utf-8 -*-
import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.upload import FilesOpener

from django.conf import settings
from .models import Answer, Trigger, RegexTrigger, \
    TextTrigger, OneTextTrigger


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

    regex_trigger = RegexTrigger.objects.all()
    text_triggers = OneTextTrigger.objects.all()

    # reg exps
    for trigger in [(trigger.reg_exp, trigger.pk) for trigger in regex_trigger]:
        pass
    else:
        # text exps
        for trigger in [(trigger.text.lower(), trigger.text_trigger.id, trigger.text_trigger.entry) for trigger in text_triggers]:
            if trigger[2]:
                # Вхождение
                pass
            else:
                # Совпадение
                if trigger[0] == text:
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


def no_pm(raw_event, vk=vk):
    event = longpoll._parse_event(raw_event)
    vk.messages.send(
        chat_id=event.chat_id,
        peer_id=event.obj.peer_id,
        random_id=get_random_id(),
        message='Я бот для чатов!\nНикаких ЛС!',
    )


# vocabulary = ('КТО МНОГО ПИЗДИТ ТОТ МАЛО ЖИВЁТ', 'ПОДЗАБОРНАЯ БРАНЬ',
#               'ТРЕПЕЗДОНИТ', 'СКОТОЁБИНА', 'СОЧИ', 'ОДНОХУЙСТВЕННО',
#               'БЛЯДЕМУДИННЫЙ ПИЗДОПРОЁБ',)