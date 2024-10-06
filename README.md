# keenecap
## Description
This project is designed to interact with a Keenetic router, providing functionalities such as authentication, capturing network traffic, and downloading capture files.

## Installation

### Prerequisites
Ensure that TShark is installed on your system. TShark is a network protocol analyzer that is part of the Wireshark suite. You can install it using your package manager. For example, on Ubuntu, you can run:
```bash
sudo apt-get install tshark
```
To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
To start the main application, execute:
```bash
python main.py
```

## Features
- Authenticate with the router
- Start and stop network captures
- Download capture files
- Manage capture interfaces

## Directory Structure
- `keenecap/`: Contains the core modules for interacting with the router.
- `captures/`: Directory for storing capture files (tracked but contents are ignored).
- `main.py`: Entry point for the application.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
