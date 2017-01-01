Сказки добавляются сюда.

Имя файла должно быть таким:

```
0042-link-name.md
^^^^ обязательный префикс для сортировки файлов
    ^ дефис-разделитель
     ^^^^^^^^^ имя ссылки, сказка будет по url: /tale/link-name/
              ^^^ обязательно расширение .md — Markdown
```

Сам файл — в формате [Markdown](http://rukeba.com/by-the-way/markdown-sintaksis-po-russki/).

Первый заголовок первого уровня в файле будет текстом ссылки на индексной странице.

```
# Вот этот текст будет на главной странице

А дальше идёт текст сказки...
```

Чтобы вставить пустую строку, придётся написать html entity:

```
Предыдущий абзац

&nbsp;

Следующий абзац. Между абзацами — пустой абзац.
```