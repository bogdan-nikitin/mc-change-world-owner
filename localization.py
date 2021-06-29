import locale
import os
import platform


LOCALE_PATH = './lang'
LOCALE_ENVIRON_VARIABLE = 'LANG'
LANGUAGES = ['en', 'ru']


def set_lang_in_environ(lang=None):
    if platform.system() == 'Windows':
        if os.getenv('LANG') is None:
            if lang is None:
                lang, _ = locale.getdefaultlocale()
            os.environ[LOCALE_ENVIRON_VARIABLE] = lang
