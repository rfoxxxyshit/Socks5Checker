# Socks5Checker
<p align="center"><a href="https://www.codacy.com/gh/rfoxxxyshit/Socks5Checker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rfoxxxyshit/Socks5Checker&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/d4656ba0c1ee42b9b0f6f589193c3bc7"/></a></p>
<p align="center">CLI-скрипт для проверки Socks5 прокси на работоспособность.</p>

# Установка

Для работоспособности Socks5Checker необходимо установить `python3`, и следующие библиотеки:

1. `aiohttp`
2. `aiohttp_socks`
3. `psutil`

Все зависимости можно установить следующей командой:

```bash
python3 -m pip install -r requirements.txt
```

# Использование
Вам необходимо создать в корневой папке скрипта файл с названием proxy.txt и поместить туда ваши прокси.

После этого можно запускать скрипт коммандой `python3 checker.py`. 
На окончании проверки скрипт создает файлы allProxys.txt, fastProxys.txt, slowProxys.txt, куда помещает все прокси, быстрые и медленные соответственно.

# Скриншоты
<p align="center">
    <img src="https://i.imgur.com/SOzbnir.jpg" alt="Socks5Checker">
</p>

