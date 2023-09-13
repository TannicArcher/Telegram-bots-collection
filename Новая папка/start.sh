sudo systemctl restart nginx
cd /var/www/html/
killall screen
screen -S 'main' -d -m
screen -r 'main' -X stuff $'python main.py \n'
screen -S 'dashboard' -d -m
screen -r 'dashboard' -X stuff $'python dashboard.py \n'
screen -S 'hello' -d -m
screen -r 'hello' -X stuff $'python hello.py \n'
