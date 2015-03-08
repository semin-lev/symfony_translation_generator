from lib import TranslateCollections, find_files, TranslatePhrase, TranslationTemplate, File
from yaml_config import YamlRepresentation

yaml = YamlRepresentation("test.yml")
translates = TranslateCollections()
files = find_files("/Users/levsemin/projects/web/new_beontop/DarvinCMS/app/Resources",
                   "messages.*.yml|validators.*.yml")
for file in files:
    for text in file.get_all_cyrillic():
        translates.translations_list.append(TranslatePhrase(text, file))

templates = [
    TranslationTemplate("<?=$view['translator']->trans('%s')?>"),
    TranslationTemplate("$view['translator']->trans('%s')"),
    TranslationTemplate("$this->container->get('translator')->trans('%s')"),
    TranslationTemplate("%s"),
]

for trans in translates.translations_list:
    if trans.replace_to_key is not None:
        continue
    print(trans)
    exist_key = yaml.find_key_by_value(trans.phrase)
    key = input("Заменить на ключ (%s): " % exist_key)
    if len(key) == 0 and exist_key is None:
        continue
    if len(key) is None:
        key = exist_key
    temp_key = input("Шаблон (0 or nothing - view, 1 view without php tags, 2 - code, 3 - nothing): ")
    template = templates[int(temp_key)] if len(temp_key) > 0 else '0'
    trans.set_replace_to(key, template)
    yaml.set_value(key, trans.phrase)
    if key:
        print("Похожие")
        for same in translates.find_same(trans):
            flag = input(same)
            if len(flag) == 0:
                same.set_replace_to(key, template)

    print("__________________")
    print("")

translates.flush()
for file in files:
    file.flush()