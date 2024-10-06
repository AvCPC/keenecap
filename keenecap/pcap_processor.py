from credslayer import process_pcap
from keenecap.logger import logger

def process_pcap_with_logging(output_path):
    logger.info(f"Starting pcap processing for {output_path}")
    process_pcap(output_path)
    logger.info(f"Completed pcap processing for {output_path}")
