from modeltranslation.translator import register, TranslationOptions

from .models import Book, BookCategory


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(BookCategory)
class BookCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
