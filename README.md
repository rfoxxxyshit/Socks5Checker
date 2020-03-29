# Socks5Checker
<p align="center">CLI-скрипт для проверки Socks5 прокси на работоспособность.</p>

# Установка

Для работоспособности Socks5Checker необходимо установить `Python3`, и следующие библиотеки:

1. `aiohttp`
2. `aiohttp_socks`
3. `asyncio`

Библиотеки Python устанавливаются следующей коммандой:

`python3 -m pip install module_name`

# Использование
Вам необходимо создать в корневой папке скрипта файл с названием proxy.txt и поместить туда ваши прокси.

После этого можно запускать скрипт коммандой `python3 checker.py`. 
На окончании проверки скрипт создает файлы allProxys.txt, fastProxys.txt, slowProxys.txt, куда помещает все прокси, быстрые и медленные соответственно.

# Скриншоты
<p align="center">
    <img src="https://i.imgur.com/SOzbnir.jpg" alt="Socks5Checker">
</p>

