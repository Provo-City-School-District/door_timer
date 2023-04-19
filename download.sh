mkdir door_timer

wget https://github.com/Provo-City-School-District/DoorTimer/raw/main/config.json
wget https://github.com/Provo-City-School-District/DoorTimer/raw/main/door_logger.py
wget https://github.com/Provo-City-School-District/DoorTimer/raw/main/door_parser.py

mkdir lib
cd lib

wget https://github.com/Provo-City-School-District/DoorTimer/raw/main/lib/date.py
wget https://github.com/Provo-City-School-District/DoorTimer/raw/main/lib/gpio_loader.py

cd ..

# Remove myself
rm -- "$0"
