# AHeroOfOurTime_Corpus
## Корпус

Наш корпус основан на произведении М. Ю. Лермонтова «Герой нашего времени». Произведение было взято с сайта rvb.ru.

`Project_corpus_crawler.ipynb` — код для парсинга произведения "Герой нашего времени" с сайта rvb.ru. 

`crawler_text.csv` — CSV файл, где хранится спарсенный текст по главам.

`corpus_data.csv` — CSV файл, где хранится информация о каждом предложении (токены, леммы, теги, из какой части взято предложение).

`morph_hero.ipynb` — код, с морфологической обработкой предложений.

`corpus_data_with_labels.csv` — CSV файл, где хранится та же информация, что и в `corpus_data.csv` только добавилась 6 колонка с пометкой устаревшести слова (бинарная разметка).

`is_obsolete_hero.ipynb` — код, размечающий устаревшие слова связые из [Словаря устаревших слов](https://azbyka.ru/otechnik/Spravochniki/slovar-ustarevshih-slov/)

## Морфологическая разметка
NOUN: существительное;

VERB: глагол;

ADJ: прилагательное;

ADV: наречие;

AUX: вспомогательный глагол;

CCONJ: сочинительный союз;

NUM: числительное;

PART: частица;

PRON: местоимение;

PROPN: имя собственное;

SCONJ: подчинительный союз;

DET: определитель;

ADP: общий термин для предлогов и послелогов;

INTJ: междометие;

X: заимствованное слово латиницей.

## Параметр устаревшести
В качестве одной из фишек проекта мы решили выделить устаревшие слова в нашем датасете. На сайте они будут обозначены подчеркиванием. Список устаревших слов мы брали с помощью парсинга с сайта https://azbyka.ru/otechnik/Spravochniki/slovar-ustarevshih-slov/
## Поиск
`Search.ipynb` - функция поиска. В этом файле прописаны все возможные запросы пользователя.

## Частотность
В качестве еще одной из фишек мы решили вывести частотность слов и сочетаний...

## Сайт
Сайт был создан с помощью html, css, flask. На нашем сайте две страницы: на первом есть рассказ о проекте и все инструкции, на второй странице представлен сам поиск по корпусу.
В инструкции по пунктам в отдельных блоках расписаны все варианты подачи запроса пользователем, отмечено, что устаревшие и искомые слова будут выделены цветом. Еще на странице с инструкцией выведен список возможных POS. В верне части обеих страниц сайта есть навигационная панель, где есть кнопки, благодаря которым можно перемещаться по страницам сайта и попасть на наш гитхаб.
## Тестирование
**При тестировании мы проверили все основные вариации запросов. Нами были выделены несколько сложных случаев:
- POS, размеченные как 'X'. Так размечались слова, написанные не на русском языке (например, charmant, délicieux)
- Лемматизатор записал в леммы в некоторых случаях форму "Печорина" (как женская фамилия) вместо формы "Печорин"
- Мы учитывали запросы со словами в разных регистрах, приравнивая их. Запросы "Печорин", "печорин", "ПЕЧОРИН" выдают одинаковые результаты. Запросы со словами мы разграничивали с POS, создав специальный словарь для POS-тегов и сравнивая запросы с этими значениями.
