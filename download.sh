mkdir door_timer

cd door_timer

curl -L -o config.json https://github.com/Provo-City-School-District/DoorTimer/raw/main/config.json
curl -L -o door_logger.py https://github.com/Provo-City-School-District/DoorTimer/raw/main/door_logger.py
curl -L -o door_parser.py https://github.com/Provo-City-School-District/DoorTimer/raw/main/door_parser.py

mkdir lib
cd lib

curl -L -o date.py https://github.com/Provo-City-School-District/DoorTimer/raw/main/lib/date.py
curl -L -o gpio_loader.py https://github.com/Provo-City-School-District/DoorTimer/raw/main/lib/gpio_loader.py

cd ..

# Remove myself
rm -- "$0"
