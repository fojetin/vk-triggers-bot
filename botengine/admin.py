from django.contrib import admin

from .models import *


class TriggerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'entry')
    
    def get_answer(self, obj):
        return obj.answer.text
    get_answer.admin_order_field  = 'author'  #Allows column order sorting
    get_answer.short_description = 'Author Name'  #Renames column head


class OneTextTriggerInline(admin.StackedInline):
    model = OneTextTrigger
    extra = 1


class TextTriggerAdmin(TriggerAdmin):
    inlines = [OneTextTriggerInline]
    list_display = ('answer', 'get_text', 'entry')

    def get_text(self, obj):
        return [trigger.text for trigger in obj.one_text_trigger.all()]


admin.site.register(Answer)

admin.site.register(TextTrigger, TextTriggerAdmin)

admin.site.register(RegexTrigger, TriggerAdmin)