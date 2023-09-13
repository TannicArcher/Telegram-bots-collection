apt update
apt upgrade -y

apt install -y htop git nginx build-essential libssl-dev libffi-dev
apt install -y python3-pip python3-dev python3-setuptools python3-venv
apt install -y screenfetch neofetch python-is-python3
sudo apt install screen

python -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
deactivate

touch /etc/systemd/system/SessionMaker.service

echo """
Description=SessionMaker service
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/root/SessionMaker
ExecStart=/root/SessionMaker/.venv/bin/hypercorn main.py -b 5000
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target
""" > /etc/systemd/system/SessionMaker.service

systemctl enable SessionMaker.service
systemctl start SessionMaker.service

set "$(hostname) $(hostname -i)"

touch /etc/nginx/conf.d/SessionMaker.conf
echo """
server {
    server_name $1;
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
""" > /etc/nginx/conf.d/SessionMaker.conf

nginx -s reload