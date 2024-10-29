# AHeroOfOurTime_Corpus
## Краулинг
`Project_corpus_crawler.ipynb` — код для парсинга произведения "Герой нашего времени" с сайта rvb.ru. 

`crawler_text.csv` — CSV файл, где хранится спарсенный текст по главам.

## Морфологическая разметка
- Список наших тегов
- NOUN: существительное;
- VERB: глагол;
- ADJ: прилагательное;
- ADV: наречие;
- AUX: вспомогательный;
- CCONJ: сочинительный союз;
- NUM: цифра;
- PART: частица;
- PRON: местоимение;
- PROPN: имя собственное;
- SCONJ: подчинительный союз;
- X: слово, написанное не кириллицей.

## Параметр устаревшести
В качестве одной из фишек проекта мы решили выделить устаревшие слова в нашем датасете. На сайте они будут обозначены подчеркиванием. Список устаревших слов мы брали с помощью парсинга с сайта https://azbyka.ru/otechnik/Spravochniki/slovar-ustarevshih-slov/
## Поиск
Функция поиска у нас написана в файле search.py. В ней прописаны все возможные запросы пользователя (и с токенами, и с частями речи)

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
