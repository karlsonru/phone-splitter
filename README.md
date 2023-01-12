# phone-splitter
Web-app, определяющее телефонного провайдера и регион по DEF коду. 
Принимает файл в формате .csv или .txt с телефонами. 
Возвращет файл .csv, в котором указан телефон, оператор, регион.

Внешние зависимости указаны в файле requirements.txt
Установка
`pip3 install -r requirements.txt`

Для запуска Flask приложегния нужно использовать WSGI сервер перед ним. Используется gunicorn.
Нужно файл сервиса phone_splitter.service поместить в /lib/systemd/system
Затем запустить командой:
`service phone_splitter start`

Для перенаправления в nginx в блоке server по адресу /etc/nginx/sites-available/default настроить редирект запросов:
`
location /phone-splitter {
    include proxy_params;
    proxy_pass http://unix:/.../phone-splitter/cdr-parser.sock;
}
`

После перечитать конфигурацию nginx:

`nginx -s reload`