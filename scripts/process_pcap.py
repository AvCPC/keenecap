import argparse
from keenecap.pcap_processor import process_pcap_with_logging

def main():
    parser = argparse.ArgumentParser(description="Process a pcap file.")
    parser.add_argument("file", help="Path to the pcap file to process.")
    args = parser.parse_args()

    process_pcap_with_logging(args.file)

if __name__ == "__main__":
    main()
