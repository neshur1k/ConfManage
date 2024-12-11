<b>Домашнее задание 2. Вариант 2</b><br>
<i>Ангаткин Александр Денисович, ИКБО-60-23</i><br>
Программа представляет собой инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Зависимости определяются по имени пакета языка JavaScript (npm). Для
описания графа зависимостей используется представление Graphviz.
Визуализатор выводит результат на экран в виде кода.
<br><br>
Для запуска используется команда:<br>
python main.py <Путь к программе для визуализации графов> <Имя анализируемого пакета> <Путь к файлу-результату в виде кода> <Максимальная глубина анализа зависимостей> <URL-адрес репозитория>
<br>Пример использования (пакет express, максимальная глубина 3):<br>
![image](https://github.com/user-attachments/assets/124f8e55-8b81-4999-b444-9b6fa24b9d3a)
![image](https://github.com/user-attachments/assets/ceb93d07-7e3a-4d85-8a5d-b4575eb04d38)
<br><br>Визуализация графа:
![image](https://github.com/user-attachments/assets/a5d8f99b-cdce-4017-bdc8-33b7ed6c2eae)
<br><br>Граф:
<code>
digraph G {
  "express" -> "qs";
  "express" -> "depd";
  "express" -> "etag";
  "express" -> "send";
  "express" -> "vary";
  "express" -> "debug";
  "express" -> "fresh";
  "express" -> "cookie";
  "express" -> "accepts";
  "express" -> "methods";
  "express" -> "type-is";
  "express" -> "parseurl";
  "express" -> "statuses";
  "express" -> "encodeurl";
  "express" -> "proxy-addr";
  "express" -> "body-parser";
  "express" -> "escape-html";
  "express" -> "http-errors";
  "express" -> "on-finished";
  "express" -> "safe-buffer";
  "express" -> "utils-merge";
  "express" -> "content-type";
  "express" -> "finalhandler";
  "express" -> "range-parser";
  "express" -> "serve-static";
  "express" -> "array-flatten";
  "express" -> "path-to-regexp";
  "express" -> "setprototypeof";
  "express" -> "cookie-signature";
  "express" -> "merge-descriptors";
  "express" -> "content-disposition";
  "qs" -> "side-channel";
  "side-channel" -> "call-bind";
  "side-channel" -> "es-errors";
  "side-channel" -> "get-intrinsic";
  "side-channel" -> "object-inspect";
  "call-bind" -> "call-bind-apply-helpers";
  "call-bind" -> "es-define-property";
  "call-bind" -> "get-intrinsic";
  "call-bind" -> "set-function-length";
  "get-intrinsic" -> "call-bind-apply-helpers";
  "get-intrinsic" -> "dunder-proto";
  "get-intrinsic" -> "es-define-property";
  "get-intrinsic" -> "es-errors";
  "get-intrinsic" -> "function-bind";
  "get-intrinsic" -> "gopd";
  "get-intrinsic" -> "has-symbols";
  "get-intrinsic" -> "hasown";
  "send" -> "ms";
  "send" -> "etag";
  "send" -> "debug";
  "send" -> "fresh";
  "send" -> "destroy";
  "send" -> "statuses";
  "send" -> "encodeurl";
  "send" -> "mime-types";
  "send" -> "escape-html";
  "send" -> "http-errors";
  "send" -> "on-finished";
  "send" -> "range-parser";
  "debug" -> "ms";
  "mime-types" -> "mime-db";
  "http-errors" -> "depd";
  "http-errors" -> "inherits";
  "http-errors" -> "setprototypeof";
  "http-errors" -> "statuses";
  "http-errors" -> "toidentifier";
  "on-finished" -> "ee-first";
  "accepts" -> "mime-types";
  "accepts" -> "negotiator";
  "type-is" -> "mime-types";
  "type-is" -> "media-typer";
  "proxy-addr" -> "forwarded";
  "proxy-addr" -> "ipaddr.js";
  "body-parser" -> "qs";
  "body-parser" -> "depd";
  "body-parser" -> "bytes";
  "body-parser" -> "debug";
  "body-parser" -> "unpipe";
  "body-parser" -> "destroy";
  "body-parser" -> "type-is";
  "body-parser" -> "raw-body";
  "body-parser" -> "iconv-lite";
  "body-parser" -> "http-errors";
  "body-parser" -> "on-finished";
  "body-parser" -> "content-type";
  "raw-body" -> "bytes";
  "raw-body" -> "http-errors";
  "raw-body" -> "iconv-lite";
  "raw-body" -> "unpipe";
  "iconv-lite" -> "safer-buffer";
  "finalhandler" -> "debug";
  "finalhandler" -> "encodeurl";
  "finalhandler" -> "escape-html";
  "finalhandler" -> "on-finished";
  "finalhandler" -> "parseurl";
  "finalhandler" -> "statuses";
  "finalhandler" -> "unpipe";
  "serve-static" -> "encodeurl";
  "serve-static" -> "escape-html";
  "serve-static" -> "parseurl";
  "serve-static" -> "send";
  "content-disposition" -> "safe-buffer";
}
</code>
<br>Тесты написаны с помощью библиотеки unittest. Они покрывают функции fetch_package_json, fetch_dependencies, generate_dot_code.
<br>Результаты прогона тестов:<br>
![image](https://github.com/user-attachments/assets/b3d8bbdd-a595-4793-a560-7f61a1d2d19b)
<br>Код тестов:<br>
![image](https://github.com/user-attachments/assets/2cd44dca-a1c9-4dca-920d-766a16a85a4d)
![image](https://github.com/user-attachments/assets/1d20019f-f2dd-43b0-be20-44f5d01de914)
![image](https://github.com/user-attachments/assets/1c012f21-0d8b-4e4a-af74-4fd23452b10d)
