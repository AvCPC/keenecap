import sys
import os
import argparse

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keenecap.pcap_processor import process_pcap_with_logging

def main():
    parser = argparse.ArgumentParser(description="Process a pcap file.")
    parser.add_argument("-f", "--file", required=True, help="Path to the pcap file to process.")
    parser.add_argument("--delete", action="store_true", help="Delete the pcap file after processing.")
    args = parser.parse_args()

    process_pcap_with_logging(args.file, '', delete_after=args.delete)

if __name__ == "__main__":
    main()
