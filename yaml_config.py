__author__ = 'levsemin'
import yaml


class YamlRepresentation:
    def __init__(self, filename):
        self.__filename = filename
        self.__dict = None

    @property
    def dict(self):
        """
        :rtype: dict
        """
        if self.__dict is None:
            with open(self.__filename) as f:
                self.__dict = yaml.load(f)
        return self.__dict

    def flush(self):
        with open(self.__filename, 'w') as f:
            yaml.dump(self.dict, f, default_flow_style=False, allow_unicode=True)

    def _parse_key(self, str_key):
        """
        :type str_key: str
        """
        parsed_keys = str_key.split(".")
        last_key = parsed_keys.pop()
        return parsed_keys, last_key

    def _get_child_dict(self, parsed_keys, create_new_if_not_exist=False):
        """
        :type parsed_keys: list
        """
        item = self.dict
        while len(parsed_keys) > 0 and type(item) is dict:
            key = parsed_keys.pop(0)
            sub = item.get(key)
            if sub is None:
                if not create_new_if_not_exist:
                    return None
                sub = dict()
                item[key] = sub
            if type(sub) is dict:
                item = sub
                continue
            raise KeyError("%s must be a dictionary" % key)
        return item

    def set_value(self, key, value):
        """
        :type key: str
        :param value:
        :return:
        """
        (parsed_keys, last_key) = self._parse_key(key)
        item = self._get_child_dict(parsed_keys, True)
        item[last_key] = value

    def get_value(self, key):
        """
        :type key: str
        :return:
        """
        (parsed_keys, last_key) = self._parse_key(key)
        item = self._get_child_dict(parsed_keys, False)
        return item[last_key] if type(item) is dict else None
