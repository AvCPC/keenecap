import logging
import coloredlogs

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

def log_progress(message):
    """Log a message that refreshes the current line."""
    print(f"\r{message}", end='', flush=True)
