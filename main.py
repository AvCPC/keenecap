import argparse
import logging
import concurrent.futures
import time
from pyshark.capture.capture import TSharkCrashException
from keenecap.keenetic import Router  # Import the class from router.py
from keenecap.logger import logger, log_progress
import os
from keenecap.pcap_processor import process_pcap_with_logging

stop_threads = False

def main():
    global stop_threads
    # Argument parser configuration
    parser = argparse.ArgumentParser(description="Router management script.")
    parser.add_argument("-i", "--ip", required=True, help="Router IP address.")
    parser.add_argument("-p", "--port", type=int, default=80, help="Router port (default 80).")
    parser.add_argument("-l", "--login", required=True, help="Username for authentication.")
    parser.add_argument("-P", "--passwd", required=True, help="Password for authentication.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode for debugging.")
    parser.add_argument("-s", "--size", type=float, default=1.0, help="Capture size limit in MB (default 1.0 MB).")
    parser.add_argument("--delete", action="store_true", help="Delete the pcap file after processing.")

    # Parse command line arguments
    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    ip_with_port = f"{args.ip}:{args.port}"

    # Create an instance of the Router class
    router = Router(ip_addr=ip_with_port, login=args.login, password=args.passwd)

    # Authentication
    if router.authenticate():
        logger.info("Authentication successful")
    else:
        logger.error("Authentication failed")
        return

    try:
        router.get_version()
        # Start the capture worker and pcap analysis in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                future = executor.submit(capture_worker, router, executor, lambda: stop_threads, args.size, args)
                try:
                    future.result()  # Wait for the capture worker to complete
                except TSharkCrashException:
                    logger.info("TShark crashed during capture, likely due to a KeyboardInterrupt.")
            
            except KeyboardInterrupt:
                logger.info("Capture worker stopping...")
                stop_threads = True
                future.result()  # Wait for the capture worker to complete
                capture_interfaces = router.get_capture_interfaces()
                if capture_interfaces:
                    for interface in capture_interfaces["monitor"]["capture"]["interface"].keys():
                        capture_file = capture_interfaces["monitor"]["capture"]["interface"][interface]["capture-file"]
                        #logger.info(f"Capture file for interface {interface}: {capture_file}")
                        router.stop_capture(interface)
                        router.delete_remote_capture_file(interface)
                os._exit(0)        
    except RuntimeError as e:
        logger.error(f"Aborting due to error: {e}")



def capture_worker(router, executor, stop_flag, capture_size_mb, args):
    """Worker to manage packet captures on all interfaces."""
    import time
    import os

    # Initial check for running captures
    capture_interfaces = router.get_capture_interfaces()
    if not capture_interfaces:
        logger.error("Failed to retrieve capture interfaces")
        return

    try:
        for interface, details in list(capture_interfaces["monitor"]["capture"]["interface"].items())[-3:]:
            if details["statistics"]["started"]:
                logger.info(f"Capture already running on interface {interface}, stopping and downloading...")
                router.stop_capture(interface)
                capture_interfaces = router.get_capture_interfaces()
                capture_file = capture_interfaces["monitor"]["capture"]["interface"][interface]["capture-file"]
                router.stop_capture(interface)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_path = f"{interface}_capture_{timestamp}.pcap"
                router.download_capture_file(capture_file, output_path)
                router.delete_remote_capture_file(interface)
        
            logger.info(f"Starting new capture on interface {interface}...")
            router.start_capture(interface)
    except TSharkCrashException as e:
        logger.error(f"TShark crashed: {e}")
        return

    while True:
        if stop_flag():
            logger.info("Stopping capture worker...")
            break

        capture_interfaces = router.get_capture_interfaces()
        if not capture_interfaces:
            logger.error("Failed to retrieve capture interfaces")
            break


        for interface, details in list(capture_interfaces["monitor"]["capture"]["interface"].items())[-3:]:

            capture_file = details["statistics"]["file"]
            bytes_total = details["statistics"]["bytes-total"]

            if bytes_total > capture_size_mb * 1_000_000:  # Check if capture size exceeds specified limit
                router.stop_capture(interface)
                logger.debug(f"Capture on interface {interface} exceeds {capture_size_mb}MB, processing...")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_path = f"{interface}_capture_{timestamp}.pcap"
                #time.sleep(1)
                capture_interfaces = router.get_capture_interfaces()
                #print(capture_interfaces)
                capture_file = capture_interfaces["monitor"]["capture"]["interface"][interface]["capture-file"]  
                logger.debug(f"Downloading capture file {capture_file} to {output_path}")
                router.download_capture_file(capture_file, output_path)
                executor.submit(process_pcap_with_logging, output_path, '', args.delete)
                router.delete_remote_capture_file(interface)
                router.start_capture(interface)

        time.sleep(2)  # Monitor every 2 seconds
        
        
main()
