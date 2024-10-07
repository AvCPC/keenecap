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
python main.py --help
usage: main.py [-h] -i IP [-p PORT] -l LOGIN -P PASSWD [-v] [-s SIZE] [--delete] [--filter FILTER] [--no-process]

Router management script for Keenetic routers. This script allows you to authenticate, manage network traffic captures, and handle capture files.

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Router IP address. This is the address used to access the router's web interface.
  -p PORT, --port PORT  Router port (default 80). Specify the port if your router uses a non-standard port for web access.
  -l LOGIN, --login LOGIN
                        Username for authentication. This is the username you use to log into the router.
  -P PASSWD, --passwd PASSWD
                        Password for authentication. This is the password associated with the login username.
  -v, --verbose         Enable verbose mode for debugging. Use this option to see detailed logs for debugging purposes.
  -s SIZE, --size SIZE  Capture size limit in MB (default 1.0 MB). Specify the maximum size of the capture file before it is processed.
  --delete              Delete the pcap file after processing. Use this option to automatically remove the capture file after it has been processed.
  --filter FILTER       Optional filter for tshark processing. Use this to specify a tshark filter to apply during capture processing.
  --no-process          Disable processing of pcap files. Use this option to skip the processing step and only capture the data.

Example usage: python main.py -i 192.168.1.1 -l admin -P password --size 2.0 --delete

```

## Features
- Authenticate with the router
- Start and stop network captures
- Download capture files
- Manage capture interfaces

## Additional Scripts

### scripts/process_pcap.py
This script is used to process pcap files independently. It allows you to specify a pcap file for processing and optionally delete the file after processing. To use this script, run:

```bash
python scripts/process_pcap.py -f path/to/pcapfile.pcap --delete
```
- `keenecap/`: Contains the core modules for interacting with the router.
- `captures/`: Directory for storing capture files .
- `results/`: Directory for storing log file with dumped creds.
- `main.py`: Entry point for the application.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
