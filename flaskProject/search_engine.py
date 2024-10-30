import csv  # Импортируем модуль для работы с CSV-файлами
import pymorphy2  # Импортируем библиотеку для морфологического анализа
import re  # Импортируем модуль для работы с регулярными выражениями
from detokenize.detokenizer import detokenize

# Инициализация морфологического анализатора
morph = pymorphy2.MorphAnalyzer()

# Список универсальных частей речи (POS-тегов), используемых в проекте
POS_TAGS = [
    "adj", "adv", "intj", "noun", "propn", "verb",
    "adp", "aux", "cconj", "det", "num", "part",
    "pron", "sconj", "x"
]


class SearchEngineCSV:
    def __init__(self, csv_file):
        # Инициализация атрибутов класса
        self.sentences = []  # Список предложений
        self.tokens = []  # Список токенов (слов) в предложениях
        self.lemmas = []  # Список лемм (основ слов) для токенов
        self.pos_tags = []  # Список POS-тегов для токенов
        self.chapters = []  # Список глав (или источников) предложений
        self.is_obsolete = []  # Список индикаторов устаревших слов

        # Открываем CSV-файл для чтения
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)  # Создаем объект для чтения CSV
            next(reader)  # Пропускаем заголовок
            for row in reader:  # Итерируем по строкам в файле
                # Считываем данные из каждой строки и сохраняем в соответствующие списки
                self.sentences.append(row[0])
                self.tokens.append(row[1].split(';'))  # Разбиваем токены по разделителю ';'
                self.lemmas.append([lemma.lower() for lemma in row[2].split(';')])  # Леммы в нижнем регистре
                self.pos_tags.append(row[3].split(';'))  # Разбиваем POS-теги по разделителю ';'
                self.chapters.append(row[4])  # Сохраняем главу (источник)
                # Преобразуем индикаторы устаревших слов в целые числа
                self.is_obsolete.append([int(obs) for obs in row[5].split(';')])

    def match_token(self, token, word, lemma, pos):
        # Функция для проверки соответствия токена искомому слову
        token = token.lower()  # Приводим токен к нижнему регистру для сравнения
        if '"' in token:  # Если токен заключен в кавычки
            return token.strip('"').lower() == word.lower()  # Сравниваем без кавычек
        if '+' in token:  # Если токен содержит '+', значит, это лемма и POS-тег
            query_word, query_pos = token.split('+')  # Разделяем на слово и POS-тег
            return lemma.lower() == query_word.lower() and pos.lower() == query_pos.lower()  # Сравниваем лемму и POS-тег
        if token in POS_TAGS:  # Если токен является частью речи
            return pos.lower() == token  # Сравниваем с POS-тегом
        return lemma == morph.parse(token)[0].normal_form  # Сравниваем с нормальной формой токена

    def match_sequence(self, query_tokens, words, lemmas, pos_tags):
        # Функция для проверки последовательности токенов
        if len(query_tokens) > 2 and '"' in query_tokens[2]:
            query_tokens[1] = query_tokens[1] + '"'
        for j, query_token in enumerate(query_tokens):
            # Если текущий токен запроса является частью речи
            if query_token in POS_TAGS:
                if pos_tags[j].lower() != query_token:  # Проверка соответствия POS-тега
                    return False  # Если не совпадает, возвращаем False
            else:
                # Проверка соответствия слова, леммы и POS-тега
                if not self.match_token(query_token, words[j], lemmas[j], pos_tags[j]):
                    return False  # Если не совпадает, возвращаем False
        return True  # Если все токены совпадают, возвращаем True

    def highlight_word(self, sentence, words, match_indices, obsolete_indices):
        # Функция для выделения искомых и устаревших слов в предложении
        highlighted_sentence = sentence  # Сохраняем оригинальное предложение
        # Выделяем жирным искомые слова
        for i in match_indices:
            word = words[i]  # Получаем слово по индексу
            # Заменяем слово на его выделенную версию
            highlighted_sentence = re.sub(rf'\b{re.escape(word)}\b', f'<b>{word}</b>',
                                          highlighted_sentence, flags=re.IGNORECASE)
        # Подчеркиваем устаревшие слова
        for i in obsolete_indices:
            word = words[i]  # Получаем устаревшее слово по индексу
            # Заменяем слово на его подчеркнутую версию
            highlighted_sentence = re.sub(rf'\b{re.escape(word)}\b', f'<u>{word}</u>',
                                          highlighted_sentence, flags=re.IGNORECASE)
        return highlighted_sentence  # Возвращаем предложение с выделенными словами

    def search(self, query):
        query_tokens = query.lower().split()  # Приведение запроса к нижнему регистру

        matches = []
        # Итерируем по индексам и предложениям
        for idx, sentence in enumerate(self.sentences):
            words = self.tokens[idx]
            lemmas = self.lemmas[idx]
            pos_tags = self.pos_tags[idx]
            if len(words) != len(lemmas) or len(words) != len(pos_tags):  # проверка, что количество токенов, лемм и тегов частей речи одинаковое
                continue

            # Поиск последовательности токенов в предложении
            for i in range(len(words) - len(query_tokens) + 1):
                formatted_sentence = ""
                matches_in_sent = []
                # Проверка последовательности для n-граммы
                if self.match_sequence(query_tokens, words[i:i+len(query_tokens)], lemmas[i:i+len(query_tokens)], pos_tags[i:i+len(query_tokens)]):
                    # Форматируем предложение с источником
                    source_info = f"[{self.chapters[idx]}]"
                    if formatted_sentence == "":
                        formatted_sentence = f"{sentence} {source_info}"
                    matches_in_sent.append((i, i + len(query_tokens)))  # информация о том, какие слова - ответ на запрос (номер первого слова последовательности и первого слова после неё)
                if formatted_sentence != "":
                    matches.append([formatted_sentence, matches_in_sent, idx])  # строка "текст предложения [номер главы]", список индексов слов, соответствующих запросу, и номер предложения

        return matches

    def frequency(self, query):  # функция, определяющая частотность, принимает результаты поиска
        search_results = self.search(query)
        freq_list = {}  # вариант ответа на запрос : его частотность
        for results_elem in search_results:
            entry_indexes = results_elem[1]  # на каких номерах слова, соответствующие самому запросу (номер первого слова и следующего после последнего слова)
            sent_num = results_elem[2]
            for i in entry_indexes:
                entry_tokens = self.tokens[sent_num][i[0]:i[1]]
                entry = detokenize(entry_tokens).replace('- ', '-')
                freq_list[entry] = freq_list.get(entry, 0) + 1
        freq_list_array = list(freq_list.items())
        freq_list_sorted =  sorted(freq_list_array, key=lambda x: x[1], reverse=True)
        return freq_list_sorted
