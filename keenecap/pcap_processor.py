import os
from credslayer import process_pcap

from keenecap.logger import logger

def process_pcap_with_logging(output_path, prefix='captures/', tshark_filter='not tcp.port==443 and not tcp.port==8443 and not tcp.port==993 and not tcp.port==995 and not tcp.port==465 and not udp.port==500 and not udp.port==4500 and not udp.port==443', delete_after=False, no_process=False):
    # Process the pcap file
    # ...

    logger.debug(f"Starting pcap processing for {output_path}")
    if not no_process:
        try:
            process_pcap(prefix+output_path, tshark_filter=tshark_filter)
        except Exception as e:
            logger.error(f"Error processing pcap: {e}")
    else:
        logger.info("Processing of pcap files is disabled.")
    logger.info(f"Completed pcap processing for {output_path}")
    if delete_after:
        os.remove(prefix+output_path)
