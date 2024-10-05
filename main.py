import argparse
import logging
import concurrent.futures
from keenecap.keenetic import Router  # Import the class from router.py
from keenecap.logger import logger, log_progress


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
    parser.add_argument("-s", "--size", type=int, default=1, help="Capture size limit in MB (default 1 MB).")

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

    # Start the capture worker and pcap analysis in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(capture_worker, router, executor, lambda: stop_threads, args.size)
            future.result()  # Wait for the capture worker to complete
        except KeyboardInterrupt:
            logger.info("Capture worker stopping...")
            stop_threads = True
            future.result()  # Wait for the capture worker to complete
            capture_interfaces = router.get_capture_interfaces()
            if capture_interfaces:
                for interface in capture_interfaces["monitor"]["capture"]["interface"].keys():
                    router.stop_capture(interface)
                    router.delete_remote_capture_file(interface)

    # Retrieve router version
    version_info = router.get_version()
    if version_info:
        logger.info("Version information retrieved successfully")

    # Start the capture worker and pcap analysis in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            executor.submit(capture_worker, router, executor)
        except KeyboardInterrupt:
            logger.info("Capture worker stopped by user")
            capture_interfaces = router.get_capture_interfaces()
            if capture_interfaces:
                for interface in capture_interfaces["monitor"]["capture"]["interface"].keys():
                    router.stop_capture(interface)
                    router.delete_remote_capture_file(interface)

def capture_worker(router, executor, stop_flag, capture_size_mb):
    """Worker to manage packet captures on all interfaces."""
    import time
    import os
    from keenecap.credentials_extract import analyze_pcap_with_sniff

    # Initial check for running captures
    capture_interfaces = router.get_capture_interfaces()
    if not capture_interfaces:
        logger.error("Failed to retrieve capture interfaces")
        return

    for interface, details in list(capture_interfaces["monitor"]["capture"]["interface"].items())[-3:]:
        if details["statistics"]["started"]:
            logger.info(f"Capture already running on interface {interface}, stopping and downloading...")
            capture_file = details["capture-file"]
            router.stop_capture(interface)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"{interface}_capture_{timestamp}.pcap"
            router.download_capture_file(capture_file, output_path)
            router.delete_remote_capture_file(interface)
        logger.info(f"Starting new capture on interface {interface}...")
    router.start_capture(interface)

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
                logger.info(f"Capture on interface {interface} exceeds {capture_size_mb}MB, processing...")
                router.stop_capture(interface)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_path = f"{interface}_capture_{timestamp}.pcap"
                router.download_capture_file(capture_file, output_path)
                executor.submit(analyze_pcap_with_sniff, output_path)
                router.delete_remote_capture_file(interface)
                router.start_capture(interface)

        time.sleep(2)  # Monitor every 2 seconds
        
        
main()
