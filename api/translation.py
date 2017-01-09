from modeltranslation.translator import translator, TranslationOptions
import models

class AppTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(models.App, AppTranslationOptions)