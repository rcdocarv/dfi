#   resotre deleted file
#   sudo extundelete /dev/sda3 --restore-file /home/suser/daphi/www/app_http.py
#   panel serve app_http.py --port 5000 --address 127.0.0.1 --allow-websocket-origin=da-phy.com --allow-websocket-origin=www.da-phy.com
#   panel serve app.py --port 5000 --address 127.0.0.1 --allow-websocket-origin=da-phy.com --allow-websocket-origin=www.da-phy.com
panel serve app.py --port 5000 --address 127.0.0.1 --allow-websocket-origin=da-phy.com --allow-websocket-origin=www.da-phy.com