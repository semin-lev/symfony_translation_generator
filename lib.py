__author__ = 'levsemin'
import re
import os


class File:
    def __init__(self, filename):
        self.__filename = filename
        self.__content = None
        self.__mime_type = None

    @property
    def filename(self):
        return self.__filename

    @property
    def content(self):
        if self.__content is None:
            with open(self.filename, 'r') as f:
                self.__content = f.read()
        return self.__content

    @property
    def is_text_file(self):
        try:
            return re.search(r'.*', self.content) is not None
        except UnicodeDecodeError:
            return False

    def get_all_cyrillic(self):
        if not self.is_text_file:
            return []
        results = re.findall("[а-яА-Я][а-яА-Я \-,.]+[а-яА-Я]", self.content)
        return list(set(results))

    def replace(self, old, new):
        self.__content = self.content.replace(old, new)

    def flush(self):
        with open(self.filename, 'w') as f:
            f.write(self.content)


class TranslatePhrase:
    def __init__(self, phrase, file_obj):
        self.__phrase = phrase
        self.__file = file_obj
        self.__replace_to_key = None
        self.__replace_to_template = None

    @property
    def phrase(self):
        return self.__phrase

    @property
    def file(self):
        """
        :rtype: File
        """
        return self.__file

    @property
    def replace_to_key(self):
        return self.__replace_to_key

    @property
    def replace_to_template(self):
        """
        :rtype: TranslationTemplate
        """
        return self.__replace_to_template

    def set_replace_to(self, key, template=None):
        self.__replace_to_key = key
        self.__replace_to_template = template

    def flush(self):
        if not self.replace_to_key:
            return
        self.file.replace(self.phrase,
                          self.replace_to_template.template % self.replace_to_key if self.replace_to_template else
                          self.replace_to_key)

    def __str__(self, *args, **kwargs):
        return "%s - %s" % (self.phrase, self.file.filename)

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)


class TranslateCollections:
    def __init__(self):
        self.__list = []

    @property
    def translations_list(self):
        """
        :rtype: TranslatePhrase[]
        """
        return self.__list

    def find_same(self, translate_phrase):
        result = []
        for item in self.translations_list:
            if item.phrase == translate_phrase.phrase and item.file != translate_phrase.file \
                    and item.replace_to_key is None:
                result.append(item)
        return result

    def key_dictionary(self):
        return

    def flush(self):
        for item in self.translations_list:
            item.flush()


class TranslationTemplate:
    def __init__(self, template):
        self.__template = template

    @property
    def template(self):
        return self.__template


def find_files(catalog, excluded=None):
    result = []
    for root, dirs, files in os.walk(catalog):
        for item in files:
            if not excluded or not re.search(excluded, item):
                result.append(File(os.path.join(root, item)))
    return result