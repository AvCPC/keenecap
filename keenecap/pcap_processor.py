from credslayer import process_pcap
from credslayer.core.utils import Credentials

from keenecap.logger import logger
def process_found_credentials(credentials: Credentials):
    logger.info("Found:", credentials)
    
def process_pcap_with_logging(output_path, prefix='captures/'):
    logger.info(f"Starting pcap processing for {output_path}")
    try:
        process_pcap(prefix+output_path)
    except Exception as e:
        logger.error(f"Error processing pcap: {e}") 
    logger.info(f"Completed pcap processing for {output_path}")
