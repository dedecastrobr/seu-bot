# Seu Bot

Welcome to the Seu Bot project! This is a Python-based robot project designed to run on a Raspberry Pi. Seu Bot can control 5V motors and LEDs, making it a great platform for learning about robotics, GPIO programming, and Python development.

## Dependencies

To get started with Seu Bot, you'll need to install the following dependencies on your Raspberry Pi:

```sh
sudo apt-get install python3 python3-pip python3-venv libsdl2-2.0-0 libsdl2-dev libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-ttf-2.0-0
```

These dependencies include Python 3, pip, virtual environment tools, and various SDL2 libraries required for handling multimedia and graphics.

## Environment

Set up a virtual environment to manage your project's dependencies:

```sh
python3 -m venv seubot-env
source seubot-env/bin/activate
```

This will create and activate a virtual environment named `seubot-env`.

## Install

Install the required Python packages listed in the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

This will ensure that all necessary libraries and dependencies are installed for the project.

## Configuration

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

## Hardware

To build Seu Bot, you'll need the following hardware components:

- Raspberry Pi (any model with GPIO pins)
- 5V DC motors (2x)
- Motor driver (e.g., L298N)
- LEDs (3x: green, blue, red)
- Resistors (appropriate values for LEDs)
- Breadboard and jumper wires
- Power supply for the motors (e.g., 4x AA batteries or a 5V power adapter)

## Usage

Once everything is set up, you can run the bot using the following command:

```sh
python main.py
```

This will start the bot and it will begin executing the commands as per your configuration.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.