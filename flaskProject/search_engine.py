import csv  # Импортируем модуль для работы с CSV-файлами
import pymorphy2  # Импортируем библиотеку для морфологического анализа
import re  # Импортируем модуль для работы с регулярными выражениями

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
            return lemma == query_word and pos == query_pos  # Сравниваем лемму и POS-тег
        if token in POS_TAGS:  # Если токен является частью речи
            return pos.lower() == token  # Сравниваем с POS-тегом
        return lemma == morph.parse(token)[0].normal_form  # Сравниваем с нормальной формой токена

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
        # Функция для поиска предложений, содержащих искомый запрос
        query_tokens = query.lower().split()  # Приводим запрос к нижнему регистру и разбиваем на токены
        matches = []  # Список для хранения найденных предложений
        query_length = len(query_tokens)  # Длина запроса

        # Итерируем по индексам и предложениям
        for idx, sentence in enumerate(self.sentences):
            words = self.tokens[idx]  # Получаем токены текущего предложения
            lemmas = self.lemmas[idx]  # Получаем леммы текущего предложения
            pos_tags = self.pos_tags[idx]  # Получаем POS-теги текущего предложения
            obsolete_flags = self.is_obsolete[idx]  # Получаем индикаторы устаревших слов

            # Проверяем, что количество токенов, лемм и POS-тегов совпадает
            if len(words) != len(lemmas) or len(words) != len(pos_tags):
                continue  # Если не совпадает, переходим к следующему предложению

            i = 0  # Инициализация индекса для поиска
            # Цикл для поиска совпадений в предложении
            while i <= len(words) - query_length:
                # Если найдено совпадение
                if self.match_sequence(query_tokens, words[i:i + query_length], lemmas[i:i + query_length],
                                       pos_tags[i:i + query_length]):
                    match_indices = list(range(i, i + query_length))  # Индексы совпадающих токенов
                    # Индексы устаревших слов
                    obsolete_indices = [j for j, flag in enumerate(obsolete_flags) if flag == 1]
                    # Выделяем слова и формируем предложение с источником
                    highlighted_sentence = self.highlight_word(sentence, words, match_indices, obsolete_indices)
                    source_info = f"[{self.chapters[idx]}]"  # Информация о главе
                    formatted_sentence = f"{highlighted_sentence} {source_info}"  # Форматируем итоговое предложение
                    matches.append(formatted_sentence)  # Добавляем в список найденных
                    i += 1  # Двигаем индекс на один элемент вперед для поиска следующих совпадений
                else:
                    i += 1  # Если совпадение не найдено, просто двигаем индекс
        return matches  # Возвращаем список найденных предложений

    def match_sequence(self, query_tokens, words, lemmas, pos_tags):
        # Функция для проверки последовательности токенов
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
