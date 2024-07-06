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

def hash_password(password: str) -> bytes:
    """Takes a password and returns hashed version of it"""
    return hashpw(password.encode("utf8"), gensalt())