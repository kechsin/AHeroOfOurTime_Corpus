# AHeroOfOurTime_Corpus
## Инструкция по сайту

[Сайт 1](https://anastasiaklenowa.pythonanywhere.com/search) (без часотности, с выделением жирным фрифтом искомых слов и подчеркиванием слов с устаревшим значением).

[Сайт 2](https://nastya1219.pythonanywhere.com/) (с частотностью).

На сайте есть четыре основные кнопки.

Кнопка `Главная страница` — переносит на главную страничку.

Кнопка `Поиск по корпусу` — переносит на страничку с поиском.

Кнопка `Частотность` — переносит на страничку с поиском частотностей.

Кнопка `Наш GitHub` — переносит на нашу страничку проекта в GitHub.

На главной странице описаны правила ввода в поисковик, особенности разметки корпуса и части речи. В самом низу есть еще одна кнопка `Поиск по корпусу`. 

На странице поиска находиться стандартная поисковая строка, которая обрабатывает запросы.

## Запуск сайта

Для локального запуска сайта в терминале создайте виртуальную среду `python -m venv venv`. 

Активируйте виртуальную среду: для Mac `source venv/bin/activate`, а для Windows `venv\Scripts\activate`. 

Загрузите нужные библиотеки с помощью команды`pip install -r requirements.txt`.

В папке `flaskProject` находятся все необходимые файлы для запуска сайта локально. В папке `static` находится css-файл `style_project.css`, в котором находится стиль нашего сайта. В папке `templates` находятся html файлы `head.html` (главная страница) и `search.html` (поиск по корпусу). 

Запусите файл `app.py`, а потом перейти по ссылке http://127.0.0.1:50000.

## Корпус
Наш корпус основан на произведении М. Ю. Лермонтова «Герой нашего времени». Это главное прозаическое произведение М.Ю. Лермонтова. По такому корпусу можно исследовать прозаический язык Лермонтова, как, кстати, это делала Е.В. Рахилина.

**Чем еще корпус полезен?**
- Изучать исторические изменения в лексике.
- Через язык поэзии, которая сохраняет старую норму, можно прослеживать следы устаревших языковых оборотов.
- Возможность протестировать морфологический теггер Stanza на тексте XIX века. 


## Краулинг

Произведение было взято с сайта rvb.ru.

`Project_corpus_crawler.ipynb` — код для парсинга произведения "Герой нашего времени" с сайта rvb.ru. 

`crawler_text.csv` — CSV файл, где хранится спарсенный текст по главам.

## Морфологическая разметка

Мы использовали стандартный тегсет [Universal POS tags](https://universaldependencies.org/u/pos/all.html#al-u-pos/INTJ). Для разметки мы взяли библиотеку [stanza](https://github.com/stanfordnlp/stanza). Stanza опирается на контекст и разрешает морфологическую неоднозначность достаточно хорошо. 

`corpus_data.csv` — CSV файл, где хранится информация о каждом предложении (токены, леммы, теги, из какой части взято предложение).

`morph_hero.ipynb` — код, с морфологической обработкой предложений и сохранением данных в CSV-файл `corpus_data.csv`.

**Теги используемые в нашем проекте:**

1. `NOUN` — существительное;

2. `VERB` — глагол;

3. `ADJ` — прилагательное;

4. `ADV` — наречие;

5. `AUX` — вспомогательный глагол;

6. `CCONJ` — сочинительный союз;

7. `NUM` — числительное;

8. `PART` — частица;

9. `PRON` — местоимение;

10. `PROPN` — имя собственное;

11. `SCONJ` — подчинительный союз;

12. `DET` — определитель;

13. `ADP` — общий термин для предлогов и послелогов;

14. `INTJ` — междометие;

15. `X` — заимствованное слово латиницей.

## Анализ рынка

Функция разметки устаревшести подобна проекту Е. В. Рахилиной с пометами об устаревшести слов. 
![скриншот базы данных Рахилиной](https://i.imgur.com/KXLwfKY.png)
Наша разметка распространяется только на лексический уровень и здесь нет распознания омонимии (например, слово "право" в значении вводного слова устаревшее, но есть и неустаревшие значения — и все они у нас будут помечены устаревшими, потому что разрешать неоднозначность было бы значительно сложнее).

**Мы посмотрели различные корпусы и пришли к решению:**
- Добавление кнопки копирования целого предложения (как в НКРЯ, Tatoeba, Linguee и т. д.) является очень полезной фичей. 
- Добавление частотности тоже очень полезно для исследований словосочетаний и диахронии.
- Добавление выделения искомых слов в предложении как в НКРЯ тоже полезно. Сразу видно, где искомая часть находится в предложении.
- Добавление параметра устаревшести. Может быть полезно для прослеживания исторических изменений в лексике. Данная фича придумана нами.

## Параметр устаревшести

В качестве одной из фишек проекта мы решили выделить устаревшие слова в нашем датасете. На сайте они будут обозначены подчеркиванием. Список устаревших слов мы брали с помощью парсинга с сайта [Словаря устаревших слов](https://azbyka.ru/otechnik/Spravochniki/slovar-ustarevshih-slov/).

`corpus_data_with_labels.csv` — CSV файл, где хранится та же информация, что и в `corpus_data.csv`, только добавилась 6 колонка с пометкой устаревшести слова (бинарная разметка).

`is_obsolete_hero.ipynb` — код, размечающий устаревшие слова взятые из [Словаря устаревших слов](https://azbyka.ru/otechnik/Spravochniki/slovar-ustarevshih-slov/) и сохраняющий данные в CSV-файл `corpus_data_with_labels.csv`.

## Поиск
Функция поиска создана для того, чтобы пользователь мог смотреть по нашему корпусу разные сочетания (от одного слова до трех) слов или частей речи. Части речи мы выписали в отдельный список. Запрос пользователя далее мы сравниваем со словами и с тегами к этим словам в корпусе.  
 
У нас есть отдельные функции для просмотра совпадения слов и предложений. В них написаны условия для проверки разных конфигураций запросов 
 
Далее общем файле для поиска (search_engine.py) идет функция для подсчета частотности слов, а также функция для выделения искомых и устаревших слов

`Search.ipynb` - функция поиска. В этом файле прописаны все возможные запросы пользователя.

В поисковом запросе `знать+NOUN` мы решили, что будем искать лемму слова, потому что полезнее узнать общее количество употреблений слова _знать_ в значении существительного, чем искать определенную словоформу.

## Частотность
В качестве еще одной из фишек мы решили вывести частотность слов и сочетаний. Если пользователь вводит запрос, у которого есть больше одного варианта, как он может быть выражен в тексте (то есть, лемма может быть в разных формах, а если в поиске часть речи, то там могут быть разные слова), то эта функция выведет, какие из конкретных реализаций запроса в каком количестве встречаются:
Пример: по запросу *конь* частотности будут такие: ('коня', 10), ('конь', 4), ('конях', 1), ('коне', 1), ('кони', 1).
Не учитываются: регистр, знаки препинания (все варианта типа "дом, стоял", "дом стоял", "Дом - стоял" будут засчитаны как один вариант реализации "дом стоял").
Частотность рассчитывается функцией frequency класса SearchEngineCSV (в файле `Search.ipynb`).

## Сайт
Сайт был создан с помощью html, css, flask. На нашем сайте три страницы: на первом есть рассказ о проекте и все инструкции, на второй странице представлен сам поиск по корпусу, на третьей - поиск частотности.
В инструкции по пунктам в отдельных блоках расписаны все варианты подачи запроса пользователем, отмечено, что устаревшие и искомые слова будут выделены цветом. Еще на странице с инструкцией выведен список возможных POS. В верне части обеих страниц сайта есть навигационная панель, где есть кнопки, благодаря которым можно перемещаться по страницам сайта и попасть на наш гитхаб.


## Тестирование
**При тестировании мы проверили все основные вариации запросов. Нами были выделены несколько сложных случаев:
- POS, размеченные как 'X'. Так размечались слова, написанные не на русском языке (например, charmant, délicieux)
- При проверке выдачи результатов мы заметили, что теггер в некоторых случаях выделил лемму "Печорина" (как женская фамилия), из-за этого при запросе леммы без кавычек "Печорин" случаи "с женской фамилией" не были учтены
- Мы предположили, что также проблемы могут возникнуть при вводе запросов с разным регистром букв. Сначала мы думали сделать проверку isupper для случаев запросов с POS, но потом решили создать отдельных список POS и сравнивать запрос уже с ним. Также мы привели все запросы и выдачу к одному регистру, так что теперь при запросах "Печорин", "ПЕЧОРИН", "печорин" будут выданы одинаковые результаты, что удобно для поиска.
- Ошибки могли бы возникнуть при запросе, состоящем из трех слов, окруженных кавычками, потому что в таком случае кавычки будут рядом с первым и третьим словом. В итоге мы учли этот момент и теперь при запросе точной формы из 3 слов (то есть три словах в кавычках) поиск действительно выдает верный результат
- Возникла ошибка: при запросе "ведь есть" не находятся результаты, хотя при запросе "'ведь есть'" - находятся. Причина: pymporphy анализирует запросы с леммами, и он у слова *есть* определяет лемму *есть* (думает, что это *есть* = *кушать*), а во всех вхождениях *ведь есть* в тексте у слова *есть* лемма *быть*.

## Скорость поиска
Сейчас у нас не очень быстро работает функция поиска, и функция частотности тоже (она использует поиск). У нас есть две идеи, как это улучшить, но мы не успели их реализовать.
1. У нас сейчас приведение слова запроса к нормальной форме происходит в функции match_token, которая вызывается для каждого слова в тексте, причём при неоднословных запросах больше одного раза. Было бы значительно быстрее, если бы это происходило один раз сразу после получения запроса. Это кажется более серьёзным улучшением, потому что сейчас мы непосредственно делаем одну работу дважды.
2. Если же этого не хватит, можно применить какие-то алгоритмы для ускорения поиска, например, [алгоритм Кнута-Морриса-Пратта](https://ru.wikipedia.org/wiki/Алгоритм_Кнута_—_Морриса_—_Пратта) позволит более эффективно искать подпоследовательность токенов (или лемм, частей речи) в последовательности.

## Участники команды и их обязаности

Алсу Хабирзянова — краулинг корпус, дизайн сайта, разработка сайта, функция поиска.

Анастасия Кленова — добавление фичи параметра устаревшести, разработка сайта, функция поиска, тестирование.

Евгения Лепихина — разработка база данных (морфологическая разметка), добавление фичи частотности, тестирование.

