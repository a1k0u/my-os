# Операционные системы

## System info

#### CPU
1. Какими способами можно узнать информацию о CPU? 

- `lshw` `lscpu` `cat /proc/cpuinfo` `sudo dmidecode --type processor`
- [Bash-скрипт](./cpu-info.sh), 
который выводит информацию о процессоре (_название, архитектуру,
число ядер, частоту работы и размер кэш-памяти_) в txt-файл.

#### RAM
2. Что такое RAM и Swap?


- `RAM` - оперативная память, также память с
произвольным доступом. Во время работы компьютера
каждая запущенная программа частично или полностью
загружается в RAM, сохраняя там команды, данные и 
промежуточные результаты для выполнения процессором.
Работа CPU с оперативной памятью <u>быстрее</u>, чем с 
жёстким диском или твердотельным накопителем.


- `Swap` - это процесс выделение виртуальной памяти,
другими словами, часть данных из RAM перемещается
на хранение в HDD или SSD. Использовать этот
механизм можно, например, когда требуется выделить
больше оперативной памяти, чем доступно.


3. Узнать всю информацию о RAM/Swap можно через
команду `free -h`, которая выводит удобочитаемую
сводку с автоматически выставленными единицами измерения.


4. Так как swap поддерживает влияние из вне, был
написан [bash-скрипт](./swap-change.sh), которому на вход подается один
обязательный аргумент с указанием количества выделенного
места. Для работоспособности прописываем 
`chmod u+x swap-change.sh`. Пример запуска:
`./swap-change.sh 1024M`. Скрипт также отлавливает
неверные входные данные (_1023Md, 3293, 
sdd1023.33M, 1g, g, ..._).


5. С помощью `sudo lshw -class memory` и 
`sudo dmidecode -t memory` можно узнать всю информацию
о RAM, в том числе: название (_product_, _Part Number_), 
производителя (_vendor_, _Manufacturer_), серийный номер
(_serial_, _Serial_), формат (_type_), объем (_size_, _Size_)
и частоту работы (_clock_).

#### Disk Usage
6. Очень длинная программа за счет конвейера,
которая выводит **размер свободного места на диске**.
Конечно, никто не мешает сократить её, засунув в 
bashrc с alias.
```bash
 df -h --total 
    | grep "total" 
    | grep -E -o "[0-9]+[BKMGTP]" 
    | echo "Available disk storage $(tail -1)"
 ```

7. Немного видоизмененная команда для вывода
используемого дискового пространства папкой /home.
```shell
df -h /home 
    | grep -E -o "[0-9]+[BKMGTP]" 
    | tail -2 
    | echo "/home used $(head -1) of disk storage"
```

8. Команда `top` предназначена для вывода
списка процессов компьютера.

#### GPU
9. Вывести информацию о GPU можно, например:
утилитой `glxinfo`, предварительно установив её
`sudo apt install mesa-utils`, а затем
`glxinfo -B | grep -A5 "Device:"`.

#### Network
10. [Bash скрипт](./ip-info.sh),
выводящий информацию (**_имя_, _IPv4_, _IPv6_, _MAC_**) для всех
сетевых устройств в human-readable формате. В конце
работы скрипта выводиться внешний IP адрес устройства.


11. В целом MAC-адрес можно получить различными способами, например:
через `ifconfig`, `ip`, но для удобства скрипт, указанный в 
[(9)](./ip-info.sh) пункте
решает поставленную задачу.


12. Подход к решению нахождения IP и MAC адреса PC может быть различен.
Например, информация об IP может быть найдена через `hostname -I`, `ip addr`,
`ifconfig`, `wget -qO- ident.me`.

#### Processes info
13. Список процессов, запущенных на компьютере, можно посмотреть
через `ps -e`, `top` и `htop`.

## System Environment
14. Создание переменных окружения происходит через команду
`export NAME=VALUE`. Вывести существующие переменные можно
через `printenv`, которые возможно изменять и выводить,
обращаясь к ним через `$`, например: `echo $LOGNAME`.

Изменения созданной/отредактированной переменной сохраняются
по-разному.

- Ввод команды `$ export VAR=128` в консоль позволит
переменной сохраниться до перезагрузки терминала.
- Если ввести предыдущую команду в`.bashrc`, то она будет постоянной
для текущего пользователя.
- Однако в `etc/bashrc` эта переменная станет существовать для 
всех пользователей устройства.


15. `PATH` в первую очередь нужен системе, которая
запускает поиск исполняемого файла утилиты, введенную
пользователем в консоли. Написав свой скрипт, мы также
можем дописать к нему путь, обращаясь к нему из любого места.
Выполнить это можно командой `export PATH=$PATH:/home/<some_root>/scripts`, но
эта запись будет существовать вплоть до перезагрузки системы.
Если добавить её в `.bashrc`, то она будет доступна только для
определенного пользователя. Если же требуется дать доступ всей
системе, то модифицируем файл `/etc/environment`. Проверку
манипуляций можно провести через `echo $PATH`, где `$PATH` -
переменная окружения.


16. Для того чтобы обновить наши системные
библиотеки, восстановим ссылки на пакеты до
актуальных. После успешного выполнения
проведем скачиванием обновлений и установку 
их на наше устройство.

```shell
sudo apt update && sudo apt upgrade
```

17.


18. В предыдущих примерах мы убедились, что команды могут быть
чересчур длинными. В bash-скриптах мы могли присвоить значение 
выполнения той или иной утилиты, а можно ли _назначить короткое
имя длинной команде_? `alias` позволяет нам сделать это. Давайте
создадим постоянные команды для выхода из директорий на 1-3 ступени выше.

```shell
> nano ~/.bashrc

# после открытия добавляем строки
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# сохраняем и обновляем bashrc
> . ~/.bashrc
```

19. Перестало нравиться состояние консоли?
Делаем левый клик мышью на свободном месте консоли,
затем переходим в `Preferences`. Откроется окно, в котором
можно сделать различные изменения (_шрифт, цвет, ..._) в консоли.

> ![Preferences in console](./img/18.png)

20. Создадим виртуальное окружение для `Python` в папке
`/home` командой `sudo python3 -m venv /home/upython`.
Теперь добавим в `.bashrc` короткую команду `psv`
(_Python start virtual environment_)
для активации нашего venv.

```shell
alias psv='source /home/upython/bin/activate'
```


## Grep

21. **Grep** - утилита, с помощью которой можно искать паттерны
в текстовых файлах. По большей части под шаблонами (паттернами)
понимается какое-то регулярное выражение. P.S. 
[датасет](https://www.kaggle.com/datasets/kaggle/hillary-clinton-emails?resource=download),
который используется в последующих заданиях.

- Представим, что у нас появился доступ
к электронным письмам Хилари Клинтон.
И нам захотелось узнать о количестве
упоминаний Уганды в её сообщениях.

```shell
grep -w -c "Uganda" Emails.csv
```

- Помимо Уганды интересно узнать о суммарном количестве
упоминаний Таджикистана и Узбекистана в одном вызове.

```shell
grep -E -w -c "Tajikistan|Uzbekistan" Emails.csv
# можно перечислить неограниченное 
# количество паттерном через |
```

- В соответствии с множественным перечислением паттернов
следует то, что количество передаваемых файлов для grep
также не ограничено. 

Найдем все упоминания слова "мир" (_во всех склонениях 
единственного числа_) во всех томах романа-эпопеи 
Льва Толстого "Война и мир".

```shell
grep -E -w -i "мир|мира|миру|миром|мире" \
              Tom1.txt Tom2.txt Tom3.txt Tom4.txt
```

22. Флаг `-i` ~ `--ignore-case` в grep отвечает за то,
что убирает чувствительность к регистру в шаблонах.


23. Флаг `-w` ~ `--word-regexp` выбирает только те строки,
где слово выделяется целиком по шаблону (_не является подстрокой_).


24. Флаг `-v` ~ `--invert-match` выводит все строки, не содержащие
паттерн, например: `grep -w -i -v "love" Shakespeare.txt` выводит
все строки, где нет слова "love".


25. Выведем содержимое файлов, чей суффикс содержит
`info` в папке `/proc`. Воспользуемся синтаксисом
bash прямо в консоли.

```shell
for file in $(ls /proc | grep "info"); do cat /proc/"$file"; done;
```

26. Добавив флаг `-n` в `grep` мы можем выводить в
нумерованном порядке строки, где нашлась шаблонная
подстрока, например `grep -n 'com' Emails.csv`.

> _Разбавим README мини-анектодом._
> 
> У программиста была одна проблема. Он решил эту проблему
> с помощью регулярного выражения. Теперь у программиста
> есть две проблемы!

27. Воспользуемся базовым синтаксисом регулярных выражений.
Найдем все слова, в которые точно выходит одна буква `h`, а после
следует любой `символ`. Любое количество букв `l`, точно больше одной
буквы `о`, какой-то `возможный разделитель` и в конце входящее или
не входящее слово `world`.
```shell
grep -R -w "[h]{1}.l*[o]+[\W]?(world)?" someFile.txt
```

28. Команда `ls -R /lib | grep -E "*\.so"` находит все файлы с расширением
`.so`, рекурсивно обходя все поддиректории `/lib`.


29.


30.


31. Допустим, нам нужно вывести все процессы от действующего
пользователя. Решить поставленную задачу можно так:
`top -n 1 -b | grep -E "${USER:0:7}[+]?"`. 

## Find

32. Чтобы найти определенный файл в какой-то директории,
воспользуемся `find`. Команда будет следующая:

```shell
find ./someDir -type f -name "someFile.txt"
```

33. Найдем все файлы и директории системы,
в которых первый символ названия пропущен,
имеется подстрока 'hi' и какие-то символы,
в папке `/home`.

```shell
find /home -name "?*hi*"
```

34. `-iname` вместо `-name` позволяет в поиске
не учитывать регистр заданной маски.


35. `find` позволяет искать файлы с определенным
набором прав доступа, за это отвечает флаг `-perm`.
Найдем все файлы в системе с полным доступом (_777_).

```shell
find / -perm 777
```

- Каждая цифра отвечает за класс: user, group,
other соответственно.


- Цифра получается из суммы, где 4 - чтение,
3 - запись, а 1 - выполнение.


36. Исходя из информации предыдущего пункта,
найдем все файлы, в которых для текущего
пользователя доступно чтение, а другим - нет.
`find / -perm 400`


37. Поиск пустых директорий можно выполнить так:
`find / -type d -empty`.


38. Все скрытые файлы начинаются с точки в начале,
поэтому поиск всех таких файлов таков:
`find / -type f -name ".*"`


39. Если нужно найти файлы, модифицированные n
дней или часов (минут) назад (за последние),
то пользуемся флагами `-mtime` и `-mmin`.

```shell
# найдем все файлы, измененные за последние
# 3 часа (180 минут)
find / -type f -mmin +0 -mmin -180

# поиск файлов, которые подверглись изменению 3 дня назад
find / -type f -mtime 3

```

40. Аналогично можно узнать о файлах, которые были
открыты за n количество дней, минут назад. `-atime`,
`amin` соответственно.


41. Поиск всех файлов по определенному объему или
диапазону можно сделать так: 
`find / -size +10M -size -15M` (_поиск файлов объемом
от 10 до 15 Мбайт_)


42. Результаты `find` можно перенаправлять в другие
команды. Допустим нам нужно найти все txt-файлы в
текущей директории и переместить их во временную
поддиректорию директории `home`.

```shell
sudo mkdir /home/tmp

sudo find . -type f -name "*.txt" -exec cp {} /home/tmp \;
```

43. Но вот беда, мы скопировали не то что нужно. Давайте с помощью `find` найдем
эти файлы и удалим их.

```shell
sudo find /home/tmp -type f -name "*.txt" -exec rm {} \;

# эквивалентная команда
sudo find /home/tmp -type f -name "*.txt" -delete;
```

## Bash

44. Желательно перед началом написания всех скриптов создать
директорию `mkdir /home/myscripts` и добавить её в `$PATH`,
чтобы иметь доступ к файлам из любого места.

45. Базовый скрипт "hello, world" в первой строке содержит
указание на bash-оболочку, а затем наш сценарий. Перед запуском
нужно убедиться, что действуют права на запуск, а после `./script.sh`.

```shell
#!/bin/bash

echo "hello, world"
```

46. [Скрипт](./check-exist.sh), который проверяет существование
файла или директории относительно какой-то папки. Выводит
тип объекта и абсолютный путь.


47. .


48. .


49. [Python-скрипт](./weather.py), определяющий по IP
адресу местоположение, по которому выводит краткую сводку
текущей погоды.

- Данные о местоположение были вытащены с [Яндекс](yandex.ru/internet),
а погода по API с [OpenWeather](https://openweathermap.org).

- Для получения API ключа требуется регистрация. Но
я гордый рыцарь просто выкладываю ключ, зарегистрированный 
на временную почту.

```shell
export API_OPENWEATHER=27950c473536d6bb06394814058f4575
```

- Вывести stdout (_погоду_) в файл: `python3 weather.py > file.txt`.

50. Сделаем вывод погоды по расписанию через `cron`.

Шпаргалка по `cron`.
```shell
# ┌─────────────────────  Minute   (0..59)
# │ ┌───────────────────  Hour     (0..23)
# │ │ ┌─────────────────  Day      (1..31)
# │ │ │ ┌───────────────  Month    (1..12)
# │ │ │ │ ┌─────────────  Weekday  (0=Sun .. 6=Sat)
# ┴ ┴ ┴ ┴ ┴
# * * * * *
```

- Открываем редактор `cron` через `crontab -e`, где поставим расписание для
обновления погоды каждые 15 минут и вывод в файл.

```shell
*/15 * * * * cd /home/scripts &&
            ./weather.py >> ~/Desktop/weather.txt
```

51. [Python-скрипт](./book.py), реализующий адресную книгу.

> Рассмотрим реализованный функционал.

- Вывод всей контактной книги.

```shell
> python3 book.py -s

---

+----+------+---------+-------+----------------+----------------+
| id | name | surname | phone |     email      |      info      |
+----+------+---------+-------+----------------+----------------+
| 1  | Alex | Kosenko |  +777 |                |       Me       |
| 2  | Vova |  Ivanov |       | vov4ik@mail.ru | My best friend |
| 3  | Ira  |    N    |   +1  |                |                |
| 4  | Vova |  Pupkin |       |                | My best friend |
+----+------+---------+-------+----------------+----------------+
```

- Создание нового контакта с именем Джон, указанным номером и дополнительной информацией.
```shell
> python3 book.py -i -name John -phone +123456 -info "My favorite character"
```

- Удаление всех пользователей с именем Alex и фамилией Kosenko.
```shell
> python3 book.py -d -name Alex -surname Kosenko
```

- Поиск всех контактов по параметрам.
```shell
> python3 book.py -g -name Vova -info "My best friend"

---

+----+------+---------+-------+----------------+----------------+
| id | name | surname | phone |     email      |      info      |
+----+------+---------+-------+----------------+----------------+
| 2  | Vova |  Ivanov |       | vov4ik@mail.ru | My best friend |
| 4  | Vova |  Pupkin |       |                | My best friend |
+----+------+---------+-------+----------------+----------------+
```

- Полный список всех функций программы:

    - -i : вставка (insert) нового контакта с параметрами
    - -s : вывод (show) всей книги
    - -d : удаление (delete) контакта по условию
    - -g : поиск (grep) контакта по условию


- Все поля таблицы:
    - -name, -surname, -phone, -email, -info


- Правила входных данных:
  - Флаги (_поля_) используются перед данными. 
  - Если информация для поля больше одного слова, то требуется заключить её в кавычки.
  - Если основная функция не указана, то выведется книга.

> Стек: Python, SQLite3

52. Осталось сделать **п.51** полноценной утилитой к Linux. Воспользуется
[скриптом](book.sh), который **обязательно** должен находиться рядом с питоновским
файлом. Внесем изменения в `.bashrc`: `alias book='/home/scripts/book.sh'`.


53. Модифицируем наши скрипты, где у администратора будет доступ на чтение и запись,
а у остальных только возможность выполнения. `chmod -R 711  /home/scripts`.


54. Заархивируем все наши скрипты: `tar -cvf scripts.tar /home/scripts`.

> Подтягивайте все зависимости `pip install -r requirements.txt`.

## Administration

55. Создать нового пользователя можно с помощью команды
`sudo useradd -m UserName`. В результате будет создать
user с указанным именем без пароля и с именованной
директорией в `/home/UserName`.

- `sudo passwd UserName` - установить пароль пользователю. 
    
56. Посмотреть список существующих пользователей и групп
можно в файлах `/etc/passwd` и `/etc/group` соответственно.

- `sudo groupadd GroupName` - создание новой группы.
- `sudo usermod -aG GroupName UserName` - добавление пользователя в группу.
- `sudo deluser UserName sudo` - удаление пользователя из группы `sudo`.
- `id UserName` - посмотреть результат нашей работы.

57. Установив флаг `-N` в `useradd`, мы не добавляем нового
user ни в какие группы.


58. При создании пользователя, когда формируется его
директория, берутся файлы-скелеты из папки `/etc/skel`.
Мы можем отредактировать `.bashrc`, добавив
в переменную окружения все скрипты, которые мы ранее
написали. Теперь мы имеем доступ к ним из любой папки. 

```shell
export PATH=/home/scripts:$PATH'
```

59. Продолжая модифицировать `/etc/skel`, сделаем автоматическое
создание виртуального окружения Python для каждого нового
пользователя.

```shell
> sudo nano /etc/skel/.bashrc

---

if ! [ -e /home/"$LOGNAME"/"$LOGNAME"  ]; then
   cd /home/"$LOGNAME" && python3 -m venv "$LOGNAME"
fi

alias activate='source /home/$LOGNAME/$LOGNAME/bin/activate'
```

> Для большего удобства при создании пользователя указывайте
> оболочку `bash`: `sudo useradd -m Name -s /bin/bash`, иначе
> `chsh -s /bin/bash`.