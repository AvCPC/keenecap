import logging
import coloredlogs
import credslayer.core.logger as credslayer_logger

# Configuration du logger commun
logger = logging.getLogger("common_logger")
coloredlogs.install(
    level='INFO',
    logger=logger,
    fmt='%(asctime)s %(hostname)s %(levelname)s %(message)s',
    level_styles={
        'info': {'color': 'green'},
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

def log_progress(message):
    """Log a message that refreshes the current line."""
    print(f"\r{message}", end='', flush=True)
