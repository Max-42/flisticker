# install 
```bash


apt-get update
apt-get install python3-full python3-dev python3-setuptools python3-pip python3-wheel libjpeg-dev zlib1g-dev tmux git firefox firefox-locale-de wget -y


python3 -m pip install selenium flask webdriver-manager pillow jwt pytz --break-system-packages


wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz

tar -xvf geckodriver-v0.34.0-linux64.tar.gz

mv geckodriver /usr/local/bin/

cd /usr/local/bin/

chmod +x geckodriver

git clone https://github.com/Max-42/flisticker.git
cd /root/flisticker
python3 ./app.py
```

