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



def photo_messages(photos):
        """ Загрузка изображений в сообщения

        :param photos: путь к изображению(ям) или file-like объект(ы)
        :type photos: str or list
        """

        url = vk.photos.getMessagesUploadServer()['upload_url']

        with FilesOpener(photos) as photo_files:
            response = vk._vk.http.post(url, files=photo_files)

        return vk.photos.saveMessagesPhoto(**response.json())

vk_session = vk_api.VkApi(token='f138588eae55d9e9c5de44a4adbf7364e731989b9e74c4003793b1a129a9d6812d175d839698d9736f7f9')
vk = vk_session.get_api()

vocabulary = ('КТО МНОГО ПИЗДИТ ТОТ МАЛО ЖИВЁТ', 'ПОДЗАБОРНАЯ БРАНЬ',
              'ТРЕПЕЗДОНИТ', 'СКОТОЁБИНА', 'СОЧИ', 'ОДНОХУЙСТВЕННО',
              'БЛЯДЕМУДИННЫЙ ПИЗДОПРОЁБ',)

longpoll = VkBotLongPoll(vk_session, '172443585')


def lazy_logg(event):
    print('Новое сообщение:')
    print('От:', event.obj.from_id)
    print('Текст:', event.obj.text)


def id_nah(raw_event, vk=vk):
    event = longpoll._parse_event(raw_event)
    vk.messages.send(
        chat_id=event.chat_id,
        peer_id=event.obj.peer_id,
        random_id=get_random_id(),
        message='Я чат-бот!\nНикаких ЛС, СУКА!',
    )

def main(raw_event, vk=vk):
    event = longpoll._parse_event(raw_event)
    lazy_logg(event)
    if event.obj.text and event.obj.text.lower() in ('да', 'даа', 'дa', 'дaa',
                                                      'да!', 'да?',):
        vk.messages.send(
            chat_id=event.chat_id,
            random_id=get_random_id(),
            message='Пизда',
        )

    elif event.obj.text and event.obj.text.lower() == 'da':
        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='pizda')


    elif event.obj.text and event.obj.text.lower() == 'yes':
        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message='pussy')

    elif event.obj.text and event.obj.text.lower() in ('нет', 'неет', 'нeт',
                                                        'нет!', 'net', 'net!', 'no', 'no!'):
        vk.messages.send(
            chat_id=event.chat_id,
            random_id=get_random_id(),
            message='Пидора ответ',
        )

    elif event.obj.text and event.obj.text.lower() == 'ня':
        vk.messages.send(
            random_id=get_random_id(),
            attachment='photo-172443585_456239018',
            chat_id=event.chat_id,
        )

    elif event.obj.text and  event.obj.text.lower() in ('сочи', ):
        vk.messages.send(
            chat_id=event.chat_id,
            random_id=get_random_id(),
            message='Хуй',
        )

    elif event.obj.text and event.obj.text.lower() in ('хуй', ):
        vk.messages.send(
            chat_id=event.chat_id,
            random_id=get_random_id(),
            message='Сочи',
        )

    elif event.obj.text and event.obj.text.lower().replace('a', 'а').replace('p', 'р') in ('татары', 'татар', 'таяры') and (event.obj.text[0] == 'т'):
        vk.messages.send(
            chat_id=event.chat_id,
            random_id=get_random_id(),
            message='С БАЛЬШОЙ БУКВЫ!!!',
        )

    elif event.obj.text and event.obj.text.lower() == 'анкап':
        vk.messages.send(
            random_id=get_random_id(),
            attachment='photo-172443585_456239023',
            chat_id=event.chat_id,
        )

    elif event.obj.text and event.obj.text.lower() == 'кека':
        vk.messages.send(
            random_id=get_random_id(),
            attachment='photo-172443585_456239024',
            chat_id=event.chat_id,
        )

    elif event.obj.text and event.obj.text.lower() == 'сложна':
        vk.messages.send(
            random_id=get_random_id(),
            attachment='video-172443585_456239017',
            chat_id=event.chat_id,
        )

    else:
        if random.randint(0, 25) == 0:
            vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message=random.choice(vocabulary),
        )


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            pass
