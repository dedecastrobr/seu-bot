

Dependencies

```
sudo apt-get install python3 python3-pip python3-venv libsdl2-2.0-0 libsdl2-dev libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-ttf-2.0-0
```

Environment

```
python3 -m venv seubot-env
source seubot-env/bin/activate
```


Install
```
pip install -r requirements.txt
```

config.json
```
{
    "bot_name": "Seu Bot",
    "bot_logfile": "bot_logs",
    "enable_admin": false,
    "admin_logfile": "admin_logs",
    "gpio": {
        "motors": {
            "left_motor": {
                "forward_pin": "22",
                "backward_pin": "23"
            },
            "right_motor": {
                "forward_pin": "17",
                "backward_pin": "14"
            }
        },
        "lights": {
            "green_light": "22",
            "blue_light": "23",
            "red_light": "17"
        }
    }
}
```