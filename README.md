# Air-Connect

AirConnect is a Python application that allows users to scan available WiFi networks, connect to a selected network, and manage network connections with a user-friendly interface. It provides functionalities to display WiFi networks, connect to a selected network, and retry scanning if needed.

AirConnect is developed by Enes Can Adil.

## Features

- Scan for available WiFi networks
- Display network details in a formatted table
- Connect to a selected WiFi network
- Retry scanning for networks
- Exit the program gracefully

## Requirements

- Python 3.x
- `pywifi` library
- `rich` library
- `art` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/c4nng/AirConnect.git
    ```

2. Navigate to the project directory:
    ```bash
    cd AirConnect
    ```

3. Install the required Python packages using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the program:
    ```bash
    python AirConnect.py
    ```

2. Follow the prompts to:
    - Select a WiFi network index or press 'q' to quit
    - Enter the password for the selected network
    - Optionally, choose to scan again or exit

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For more information or to follow updates, visit our GitHub repository: [AirConnect on GitHub](https://github.com/c4nng/AirConnect)
