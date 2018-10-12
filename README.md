## automated train ticket booker for my mother

frequent commuters who work in Singapore and live in Malaysia would understand how tough it is to secure a morning train ticket during weekdays because there are a lot of people commute everyday back and from for work. i created an automated bot to help snatch and book train ticket, mainly for my mother.

```
pip install -r requirements.txt
```

include a config.ini file that has the following information

```
[credentials]
username = _____fill in the blank_____
password = _____fill in the blank_____
customer = _____fill in the blank_____

[driver]
path = _____fill in the blank_____
```

* username and password for logging in
* customer as in which customer profile do you want to use to book the ticket
* path is the path to where your selenium driver (i use chromedriver.exe)

i open-sourced this just for fun and maybe someone who really needs this but don't know how to use this can feel free to reach out to me