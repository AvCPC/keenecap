import requests
import hashlib
from keenecap.logger import logger
from urllib.parse import quote

class Router:
    def __init__(self, ip_addr, login, password):
        self.ip_addr = ip_addr
        self.login = login
        self.password = password
        self.session = requests.Session()
    
    def authenticate(self):
        """Authenticate on the router using an MD5 then SHA256 challenge."""
        response = self._send_request("auth")

        if response.status_code == 401:
            # Generate MD5 then SHA256 hash with header information
            md5_string = f"{self.login}:{response.headers['X-NDM-Realm']}:{self.password}"
            md5_hash = hashlib.md5(md5_string.encode('utf-8')).hexdigest()

            sha_string = f"{response.headers['X-NDM-Challenge']}{md5_hash}"
            sha_hash = hashlib.sha256(sha_string.encode('utf-8')).hexdigest()

            # Send a new request with hashed credentials
            response = self._send_request("auth", post_data={"login": self.login, "password": sha_hash})
            return response.status_code == 200
        return response.status_code == 200

    def _send_request(self, query, post_data=None):
        """Send a GET or POST request to the router and log debugging information."""
        url = f"http://{self.ip_addr}/{query}"

        # If we have data to send, it's a POST request
        if post_data:
            response = self.session.post(url, json=post_data)
        else:
            response = self.session.get(url)

        # Log request details
        logger.debug(f"Request URL: {url}")
        logger.debug(f"HTTP Status Code: {response.status_code}")

        return response

    def get_version(self):
        """Retrieve the router version."""
        payload = {"show": {"version": {}}}
        response = self._send_request("/rci/", post_data=payload)
        if response.status_code == 200:
            logger.debug("Version retrieved successfully")
            version_info = response.json()
            description = version_info["show"]["version"]["description"]
            arch = version_info["show"]["version"]["arch"]
            release = version_info["show"]["version"]["release"]
            logger.info(f"Description: {description}, Arch: {arch}, Release: {release}")
            return version_info
        else:
            logger.error("Failed to retrieve version")
            return None

    def start_capture(self, interface):
        """Start packet capture on a specified interface."""
        url = f"rci/monitor/capture/interface/{interface}"
        payload = {"enable": True}
        response = self._send_request(url, post_data=payload)
        if response.status_code == 200:
            logger.info(f"Capture started successfully on interface {interface}")
            return True
        else:
            logger.error(f"Failed to start capture on interface {interface}")
            return False

    def delete_remote_capture_file(self, interface):
        """Delete the remote capture file on a specified interface."""
        url = f"rci/monitor/capture/interface/{interface}"
        payload = {"enable": False, "reset": True}
        response = self._send_request(url, post_data=payload)
        if response.status_code == 200:
            logger.info(f"Remote capture file deleted successfully on interface {interface}")
            return True
        else:
            logger.error(f"Failed to delete remote capture file on interface {interface}")
            return False

    def stop_capture(self, interface):
            """Stop packet capture on a specified interface."""
            url = f"rci/monitor/capture/interface/{interface}"
            payload = {"enable": False}
            response = self._send_request(url, post_data=payload)
            if response.status_code == 200:
                logger.info(f"Capture stopped successfully on interface {interface}")
                return True
            else:
                logger.error(f"Failed to stop capture on interface {interface}")
                return False

    def get_capture_interfaces(self):
        """Retrieve available capture interfaces."""
        response = self._send_request("rci/show/monitor/capture/interface/status")
        if response.status_code == 200:
            logger.debug("Capture interfaces retrieved successfully")
            interfaces_info = response.json()
            for interface, details in interfaces_info["monitor"]["capture"]["interface"].items():
                interface_id = details["id"]
                started = details["statistics"]["started"]
                bytes_total = details["statistics"]["bytes-total"]
                capture_file = details["capture-file"]
                logger.info(f"Interface ID: {interface_id}, Started: {started}, Bytes Total: {bytes_total}, File: {capture_file}")
            return interfaces_info

    def download_capture_file(self, capture_file, output_path):
        """Download the capture file from the router."""
        encoded_capture_file = quote(capture_file)
        url = f"http://{self.ip_addr}/ci/{encoded_capture_file}"
        response = self._send_request(url)
        if response.status_code == 200:
            sanitized_output_path = output_path.replace('/', '_')
            with open(f"captures/{sanitized_output_path}", 'wb') as file:
                file.write(response.content)
            logger.info(f"Capture file downloaded successfully to {output_path}")
            return True
        else:
            logger.error("Failed to download capture file")
            return False


