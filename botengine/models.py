from django.db import models


class Answer(models.Model):
    label = models.CharField('Название', max_length=50)
    text = models.TextField('Сообщение', blank=True)
    media_attachment = models.CharField('Медиа', max_length=50, blank=True,
        help_text='Например для https://vk.com/photo-172443585_456239024 сюда надо вставить photo-172443585_456239024, для видео https://vk.com/video-172443585_456239017 вставить video-172443585_456239017. Все видео должны быть загруженны в бота.')

    def __str__(self):
        return "Ответ: " + self.label

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Trigger(models.Model):
    entry = models.BooleanField(default=False,
        help_text='Если установлен то триггер будет срабатывать на вхождение в строку, в противном случае на полное совпадение.')
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, blank=True, null=True, related_name='trigger')


class RegexTrigger(Trigger):
    reg_exp = models.TextField()

    class Meta:
        verbose_name = 'РегВыражение триггер'
        verbose_name_plural = 'РегВыражения триггеры'


class TextTrigger(Trigger):
    pass

    class Meta:
        verbose_name = 'Текстовый триггер'
        verbose_name_plural = 'Текстовые триггеры'


class OneTextTrigger(models.Model):
    text = models.CharField(max_length=100)
    text_trigger = models.ForeignKey(TextTrigger, on_delete=models.CASCADE, related_name='one_text_trigger')
