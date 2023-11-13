from modeltranslation.translator import register, TranslationOptions

from .models import New, Tag


@register(New)
class NewsTranslation(TranslationOptions):
    fields = ('title', 'content')


@register(Tag)
class TagTranslation(TranslationOptions):
    fields = ('title',)
