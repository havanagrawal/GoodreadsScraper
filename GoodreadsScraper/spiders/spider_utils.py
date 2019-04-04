"""Utility functions for spiders"""

def strip_or_default(s):
    if s:
        return s.strip()
    return None
