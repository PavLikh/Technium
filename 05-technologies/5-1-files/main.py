def get_words(filename: str) -> list | None:
    try:
        with open(filename) as f:
            s = f.read().lower()
    except:
        return None

    translation = str.maketrans('!.,()?:\'-', '         ')
    sentence = s.translate(translation)
    l = sentence.split()
    return l


def get_words_dict(l: list) -> dict:
    words = dict()
    for word in l:
        if word not in words:
            words[word] = 1
        else:
            words[word] = words[word] + 1
    return words

def show_res(words: dict) -> None:
    print('Кол-во слов:', sum(words.values()))
    print('Кол-во уникальных слов:', len(words))
    print('Все использованные слова:')
    for key, val in words.items():
        print(key, val)


file = input('Введите название файла: ')
words_l = get_words(file)
if words_l is None:
    print("Ошибка открытия файла")
else:
    words = get_words_dict(words_l)
    show_res(words)
