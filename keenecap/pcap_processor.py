import os
from credslayer import process_pcap

from keenecap.logger import logger

def process_pcap_with_logging(output_path, prefix='captures/', delete_after=False):
    # Process the pcap file
    # ...

    if delete_after:
        os.remove(output_path)
    logger.debug(f"Starting pcap processing for {output_path}")
    try:
        process_pcap(prefix+output_path)

    except Exception as e:
        logger.error(f"Error processing pcap: {e}") 
    logger.debug(f"Completed pcap processing for {output_path}")
