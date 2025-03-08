# 🤖 Seu Bot

Welcome to the Seu Bot project! This is a Python-based robot project designed to run on a Raspberry Pi. Seu Bot can control 5V motors and LEDs, making it a great platform for learning about robotics, GPIO programming, and Python development.

## 📦 Dependencies

To get started with Seu Bot, you'll need to install the following dependencies on your Raspberry Pi:

```sh
sudo apt-get install python3 python3-pip python3-venv libsdl2-2.0-0 libsdl2-dev libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-ttf-2.0-0
```

These dependencies include Python 3, pip, virtual environment tools, and various SDL2 libraries required for handling multimedia and graphics.

## 🌐 Environment

Set up a virtual environment to manage your project's dependencies:

```sh
python3 -m venv seubot-env
source seubot-env/bin/activate
```

This will create and activate a virtual environment named `seubot-env`.

## 📥 Install

Install the required Python packages listed in the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

This will ensure that all necessary libraries and dependencies are installed for the project.

## ⚙️ Configuration

Create a `config.json` file with the following structure to configure your bot:

```json
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

This configuration file specifies the GPIO pins used for controlling the motors and LEDs, as well as log file settings.

## 🔧 Hardware

To build Seu Bot, you'll need the following hardware components:

- Raspberry Pi (any model with GPIO pins. I'mm running on a `10 years old` Rasp 3 B+)
- 5V DC motors (2x)
- Motor driver (e.g., L298N)
- LEDs (3x: green, blue, red)
- Resistors (appropriate values for LEDs. There are kits with dozens. You will need many of them)
- Transistors (I've used some [IRLZ34N MOSFET](https://www.amazon.de/dp/B0893WBH6H))
- Breadboard and jumper wires (Simple and cheap as [this ones](https://www.amazon.de/-/en/AUKENIEN-Breadboard-Flexible-U-shaped-Raspberry/dp/B0B2DJCL5P) would do the job)
- Power supply for the motors (I've used [this battery shields](https://www.amazon.de/dp/B0DF7VP1PP) with the `18650 lit-ion batteries` and also a [`5V power adapters`](https://www.amazon.de/Universal-Multi-Voltage-Adapter-Household-Electronics-black/dp/B0932NCXFQ) for testing)

Looks simpler then really is. Trust me. 
If you are not familiar basics of eletronics, spare some time to research about how to connect all that stuff in the above list. It's not hard, but it takes some time to get into the mood. ;) 

## 🛠️ SeuBot Admin

Seu Bot includes an admin interface that allows you to update the configuration via HTTP requests. To enable the admin interface, set `enable_admin` to `true` in your `config.json` file:

```json
{
    "enable_admin": true,
    ...
}
```

Once the admin flag is enabled, SeuBot will start a small web server that can be used for changing the bot config.

The admin interface will be available at `http://<your-raspberry-pi-ip>:8000`.

### 🔄 Update Configuration

To update the configuration, send a POST request to `http://<your-raspberry-pi-ip>:8000/update-config` with the new configuration in the request body. For example:

```sh
curl -X POST "http://<your-raspberry-pi-ip>:8000/update-config" -H "Content-Type: application/json" -d '{
    "new_config": {
        "bot_name": "Seu Bot",
        "bot_logfile": "bot_logs",
        "enable_admin": true,
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
}'
```

This will update the configuration and save it to the `config.json` file.
Notice that the way you define this file you need to implement @SeuBot class accordingly. 
This example has 2 motors and 3 lights. You can add as much as you want.

## 🛠️ Implementing your own Bot

[`SeuBot`](/seubot/seubot.py) class is in charge to manage the robot. 
So from there, you will set your motors and lights. SeuBot also gets the events from the main thread and decides `what_todo()`, basically controling the associated hardware with the events comning from the controller.  

Motors are actually defined as [`MotorSets`](/hardware/motor.py), in order to facilitate its control. So far we have a single MotorSet, with left and right motors. 

[`Light`](/hardware/light.py) basically abstracts LED from gpiozero lib with its most basic operations.


## 🚀 Usage

Once everything is set up, you can run the bot using the following command:

```sh
python main.py
```

This will start the bot and it will begin executing it as per your configuration. If everything is fine you should be able to control it with the controller.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## 📄 License

This project is licensed under the MIT License.