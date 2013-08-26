Извлечение данных из текстов законов о бюджете Санкт-Петербурга
===============================================================

Результаты находятся [здесь](http://antonkhorev.github.io/BudgetSpb/).

Зачем?
------

Законы о бюджете публикуются в виде pdf-файлов, основную часть которых составляют таблицы с данными, занимающие сотни страниц.
Есть ещё вариант — весь текст закона из системы «Кодекс» на одной очень большой странице html или в одном doc-файле.
Таблицы оттуда для удобства работы с ними можно было бы извлечь, что данная программа и делает.
На данный момент обрабатывается *Ведомственная структура расходов*, которая обычно находится в приложениях 3 и 4 к закону.

Как запустить?
--------------

Для работы программы нужно установить:

- [python 3](http://www.python.org/) (проверено с версией 3.3);
- [xlwt3](https://bitbucket.org/luensdorf/xlwt3) — так как `xlwt` под python 3 не портирована, нужен `xlwt3`,
  но `xlwt3` не поддерживается автором и не заработает под python 3.3, поэтому нужен её указанный форк;
- [PyYAML](http://pyyaml.org/wiki/PyYAML) (проверено с версией 3.10);
- скачать [pdfbox-app-1.8.2.jar](http://pdfbox.apache.org/downloads.html), положить в каталог `bin`,
  но стандартная сборка не даст извлекать текст из файлов, у которых это действие «запрещено», а такие есть, см. ниже.

Для извлечения данных нужно запустить `src/main.py`, который скачает файлы с текстами законов, создаст csv и xls с таблицами и `index.html` со ссылками на созданные файлы.

- *Если нужно скачать законы вручную:*
  ссылки на них есть в [таблице с документами](http://antonkhorev.github.io/BudgetSpb/), столбец «исходные документы в pdf», ссылка «архив»,
  Некоторых архивов нет на сайте Комитета финансов, соответственно, нет и ссылок на них.
  В этом случае нужно перейти по ссылке «страница» и скачать все файлы закона по отдельности.
- *Если нужно найти их на сайте Комитета финансов:*
  ссылки на них находятся на странице [«Законы о бюджете»](http://www.fincom.spb.ru/comfin/budjet/laws.htm).
  Нужен файл, где весь закон с приложениями — он называется обычно «Скачать Закон с приложениями», «Текст проекта Закона с приложениями» или «Скачать все».
  Если его нет, нужно скачать все файлы закона по отдельности.
- *Вручную скачиваемые файлы* нужно класть в подкаталог каталога `zip`, соответствующий ссылке.
  Например, файл `http://www.fincom.spb.ru/files/cf/npd/budget/2013/full/bd2013-15.zip` должен находиться в каталоге `zip/2013/full`.
- Можно не скачивать пояснительные записки и комментарии.

Для публикации файлов в интернете нужно:

1. Закачать каталоги `csv` и `xls` на хостинг файлов (проверено на *dropbox*).
2. Средствами хостинга сделать их общедоступными.
3. Сохранить html-страницы с ссылками на файлы в каталог `htm`.
4. Запустить `src/linker.py`, который сделает новый `index.html` со ссылками на файлы на хостинге.
5. Закачать `index.html` на веб-хостинг (проверено на *github pages*, на *dropbox* не сработает).

«Запрещенные» pdf-файлы и что с ними делать
-------------------------------------------

Документы сохранены в pdf с «запретом» на извлечение текста:

- в законе 1-го изменения бюджета 2007 г.

Чтобы извлечь текст, нужно собрать pdfbox так, чтобы он игнорировал «запреты»:

1. Скачать исходный код `pdfbox`.
2. В файл `pdfbox/src/main/java/org/apache/pdfbox/pdmodel/encryption/AccessPermission.java` внести изменение:

		private boolean isPermissionBitOn( int bit )
		{
			//return (bytes & (1 << (bit-1))) != 0;
			return true;
		}

3. Собрать jar-файл с помощью `maven`:

		mvn clean package

4. Заменить pdfbox на получившийся файл `app/target/pdfbox-app-x.y.z.jar`.
