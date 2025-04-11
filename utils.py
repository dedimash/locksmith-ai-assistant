import os
import logging.config
import yaml

def setup_logging(
    default_path='logging_config.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    
    Args:
        default_path (str): Path to logging configuration file
        default_level (int): Default logging level
        env_key (str): Environment variable that can be used to override the config path
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log"),
                logging.StreamHandler()
            ]
        )

def handle_api_error(func):
    """
    Decorator to handle API errors
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"API Error in {func.__name__}: {str(e)}")
            # Return None or a default value
            return None
    return wrapper

def cleanup_old_files(directory, max_age_days=7):
    """
    Clean up old files in a directory
    
    Args:
        directory (str): Directory to clean up
        max_age_days (int): Maximum age of files in days
    """
    import datetime
    import time
    
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(directory):
        logger.warning(f"Directory {directory} does not exist")
        return
    
    now = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Check file age
        file_age = now - os.path.getmtime(file_path)
        if file_age > max_age_seconds:
            try:
                os.remove(file_path)
                logger.info(f"Removed old file: {file_path}")
            except Exception as e:
                logger.error(f"Error removing file {file_path}: {str(e)}")

def sanitize_input(text):
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text (str): Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove any potentially harmful characters
    import re
    sanitized = re.sub(r'[^\w\s\-\.,\?!]', '', text)
    return sanitized

def validate_phone_number(phone_number):
    """
    Validate phone number format
    
    Args:
        phone_number (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    
    # Basic phone number validation
    pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(pattern, phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')))
