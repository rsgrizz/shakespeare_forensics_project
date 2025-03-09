"""
generators/__init__.py
Created by RSGrizz

Data generation module initialization
"""

from .contact_generator import ContactGenerator
from .sms_generator import SMSGenerator
from .call_generator import CallGenerator

__all__ = [
    'ContactGenerator',
    'SMSGenerator',
    'CallGenerator'
]

def initialize_generators():
    """Initialize all generators"""
    return {
        'contact': ContactGenerator(),
        'sms': SMSGenerator(),
        'call': CallGenerator()
    }

