import os
import time
import logging
import coloredlogs
import credslayer.core.logger as credslayer_logger

# Configuration du logger commun
logger = logging.getLogger("keenecap")
coloredlogs.install(
    level='INFO',
    logger=logger,
    fmt='%(asctime)s %(hostname)s %(levelname)s %(message)s',
    level_styles={
        'info': {'color': 'white'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red', 'bold': True},
        'critical': {'color': 'red', 'bold': True, 'background': 'white'},
        'debug': {'color': 'blue'}
    },
    field_styles={
        'asctime': {'color': 'magenta'},
        'hostname': {'color': 'cyan'},
        'levelname': {'bold': True},
        'message': {'color': 'white'}
    }
)

# Set the credslayer logger to only show errors
credslayer_logger.logger.setLevel(logging.ERROR)

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

# Create a timestamped file at the start of the program
timestamp = time.strftime("%Y%m%d_%H%M%S")
results_file_path = os.path.join('results', f"results_{timestamp}.log")

def found(session, msg):
    log_message = "[FOUND] [{} {}] {}".format(session.protocol, str(session), msg)
    logger.info(log_message)
    with open(results_file_path, 'a') as f:
        f.write(log_message + '\n')

credslayer_logger.found = found 

def log_progress(message):
    """Log a message that refreshes the current line."""
    print(f"\r{message}", end='', flush=True)
