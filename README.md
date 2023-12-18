# Матчинг описания вакансий и резюме

Наш проект посвящён созданию поисковой системы, которая по входному резюме находит наиболее подходящие варианты вакансий из сохранённых в базе.

## Постановка бизнес-задачи

**Кому и как это может полезным?**

- улучшение поиска вакансий соискателями,
- более оптимальная рекомендация вакансий на соответствующих платформах.

## ML-решение

### Общий пайплайн

Для вакансий и резюме строятся их векторные представления одинакой размерности на основе наиболее важных текстовых признаков.

Для ускорения процесса поиска сохранённые вакансии предварительно кластеризуются, поэтому далее вместо того, чтобы сравнивать входное резюме со всеми вакансиями, мы будем находить ближайший к эмбеддингу входного резюме кластер с вакансиями и в качестве результатов поиска будем выдавать несколько примеров вакансий из этого кластера.

### Используемые данные

В качестве данных мы использовали:

1. готовый датасет с вакансиями с сайта "Работа России" (датасет №3 по ссылке: [datasets](https://trudvsem.ru/opendata/datasets)): для формирования базы вакансий использовали только те вакансии, в которых заполнены поля с навыками и требованиями по знанию языков. Из этих вакансий в итоге было взято 1000 примеров.
2. собранный нами (с помощью API hh.ru) датасет резюме. Опишем подробнее процесс подготовки датасета: ...

### Проведённые эксперименты

Были реализованы несколько подходов для построения эмбеддингов резюме и вакансий:

1. TF-IDF: ...
2. FastText: ...
3. ruBERT: ...

Для каждого из этих подходов была проведена кластеризация векторов вакансий при помощи метода KMeans.

Для сравнения качества построенных разными подходами эмбеддингов были построены графики метрик качества (при варьировании параметра k -- числа классов) для задачи кластеризации: SSE и Davies-Bouldin Index. Полученные графики представлены ниже:

...

Ноутбуки с проведёнными экспериментами лежат в папке ```notebooks```.

### Итоговый выбор подхода

...

## Характеристики нашего решения

Метрики качества кластеризации на построенных эмбеддингах: ...

Замеры скорости построения эмбеддинга по входному резюме: ...

Замеры скорости поиска подходящих вакансий из сохранённой базы: ...

## Веб-сервис

Для демонстрации работы приложения был реализован веб-сервис на streamlit: ... Его можно запустить локально, загрузить резюме в формате hh.ru и посмотреть, какие вакансии из сохранённой базы подбирает наше решение.

### Демо

Демо с работой веб-сервиса можно посмотреть здесь: ...