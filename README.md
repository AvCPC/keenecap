# keenecap
```
                    
                        ██╗  ██╗███████╗███████╗███╗   ██╗███████╗ ██████╗ █████╗ ██████╗ 
                        ██║ ██╔╝██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██╗
                        █████╔╝ █████╗  █████╗  ██╔██╗ ██║█████╗  ██║     ███████║██████╔╝
                        ██╔═██╗ ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝  ██║     ██╔══██║██╔═══╝ 
                        ██║  ██╗███████╗███████╗██║ ╚████║███████╗╚██████╗██║  ██║██║     
                        ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     
                                                                                                                         
                                                                                                                             

                    01001011 01100101 01100101 01101110 01100101 01000011 01100001 01110000 

                     .-.-. .-.-. .-.-. .-.-.      .-.-. .-.-. .-.-. .-.-. .-.-. .-.-. .-.-. 
                    ( T .'( e .'( A .'( m .'.-.-.( O .'( n .'( e .'( F .'( 1 .'( s .'( t .' 
                     `.(   `.(   `.(   `.(  '._.' `.(   `.(   `.(   `.(   `.(   `.(   `.(  
```                                                               


## Description
keenecap interacts with Keenetic routers for authentication, network traffic capture, and file management, using CredSlayer for credential extraction.

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
usage: main.py [-h] -i IP [-p PORT] -l LOGIN -P PASSWD [-v] [-s SIZE] [--delete]

```

## Features
- Authenticate with the router
- Start and stop network captures
- Download capture files
- Manage capture interfaces

## Directory Structure
- `keenecap/`: Contains the core modules for interacting with the router.
- `captures/`: Directory for storing capture files .
- `results/`: Directory for storing log file with dumped creds.
- `main.py`: Entry point for the application.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
