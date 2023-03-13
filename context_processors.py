"""Module for custom Flask context processors"""

from datetime import datetime

def inject_now():
    """Inject the current datetime into templates"""
    return {'now': datetime.utcnow()}