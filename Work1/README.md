<b>Домашнее задание 1. Вариант 2</b><br>
<i>Ангаткин Александр Денисович, ИКБО-60-23</i><br>
Программа представляет собой эмулятор для языка оболочки ОС, работа которого похожа на сеанс shell в UNIX-подобной ОС. 
Эмулятор принимает образ виртуальной файловой системы в виде файла формата tar и работает в режиме GUI.<br><br>
Поддерживает команды:
<ul>
  <li>ls - вывод файлов или директорий в текущей либо указанной директории;</li>
  <li>cd - переход в указанную директорию;</li>
  <li>exit - завершение сеанса;</li>
  <li>rev - вывод "перевёрнутых" строк указанного текстового файла;</li>
  <li>history - вывод истории команд.</li>
</ul>
Для запуска используются команды:
<ul>
  <li>python main.py archive.tar - без стартового скрипта;</li>
  <li>python main.py archive.tar --script script.txt - со стартовым скриптом.</li>
</ul>
Примеры использования:<br>
Без стартового скрипта<br>

![image](https://github.com/user-attachments/assets/a01403ae-c803-44b0-88d6-2aa8d03e87f4)
<br>Со стартовым скриптом<br>
![image](https://github.com/user-attachments/assets/d75c10c1-1f4e-4e51-b90d-79cc52631174)
<br><br>Тесты написаны с помощью библиотеки unittest. Они покрывают функции эмулятора load_archive, load_startup_script, execute_command, process_command, display_prompt, get_absolute_path, ls, cd, rev, show_history.
<br>Результаты прогона тестов:<br>
![image](https://github.com/user-attachments/assets/a600aa2a-60e6-4a67-b8b7-8c0c7b503757)
<br>Код тестов:<br>
![image_2024-11-14_21-49-43](https://github.com/user-attachments/assets/e789c834-ce2e-4b62-9513-cbfb55f68c90)
![image_2024-11-14_21-49-43 (2)](https://github.com/user-attachments/assets/c0cfe402-991c-4519-847f-ddc626ecc5ef)
![image_2024-11-14_21-49-43 (3)](https://github.com/user-attachments/assets/0c76bbcc-ba36-402c-ac21-7a5c7fa7dab4)
![image_2024-11-14_21-49-43 (4)](https://github.com/user-attachments/assets/0d67e40b-964f-4d3a-bc0d-f82edbb38e6d)
