#!/usr/bin/python3
"""Utility module"""
from bcrypt import hashpw, gensalt, checkpw
import re


def check_if_word_exists(word: str = None, sentence: str = None) -> bool:
    """Uses regex to check if a word exists in another string"""
    if not word or not sentence:
        return False
    
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    if pattern.search(sentence):
        return True
    return False


def sort_dict_by_values(dictionary, reverse: bool = True):
    """Sorts a dictionary by value"""
    return {keys: values for keys, values in sorted(dictionary.items(), key=lambda item: item[1], reverse=reverse)}

def validate_email_pattern(email: str = None) -> bool:
        """Checks to ensure that the email entered is an email pattern using regex"""
        if not email:
            return False
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        # Match the email against the pattern
        return bool(pattern.match(email))