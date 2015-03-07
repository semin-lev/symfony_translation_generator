from lib import TranslateCollections, find_files, TranslatePhrase, TranslationTemplate, File

translates = TranslateCollections()
files = find_files("/Users/levsemin/projects/web/new_beontop/DarvinCMS/src/",
                   "messages.*.yml|validators.*.yml")
for file in files:
    for text in file.get_all_cyrillic():
        translates.translations_list.append(TranslatePhrase(text, file))

templates = [
    TranslationTemplate("<?=$view['translator']->trans('%s')?>"),
    TranslationTemplate("$view['translator']->trans('%s')"),
    TranslationTemplate("$this->container->get('translator')->trans('%s')"),
]

for trans in translates.translations_list:
    if trans.replace_to_key is not None:
        continue
    print(trans)
    key = input("Заменить на ключ: ")
    if len(key) == 0:
        continue
    temp_key = input("Шаблон (0 - view, 1 view without php tags, 2 - code, blank - nothing): ")
    template = templates[int(temp_key)] if temp_key == '0' or temp_key == '1' else None
    trans.set_replace_to(key, template)
    if key:
        print("Похожие")
        for same in translates.find_same(trans):
            flag = input(trans)
            if len(flag) == 0:
                same.set_replace_to(key, template)

    print("__________________")

translates.flush()
# for file in files:
#    file.flush()