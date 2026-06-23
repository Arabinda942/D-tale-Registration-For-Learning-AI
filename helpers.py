# -*- coding: utf-8 -*-
"""Username/password generation, per the spec:
   ID (username)  = first name
   Password       = FirstName@123
"""
import re
import db


def _clean_first_name(full_name):
    first = full_name.strip().split()[0] if full_name.strip() else "student"
    first = re.sub(r"[^A-Za-z]", "", first)  # letters only
    return first if first else "student"


def generate_password(full_name):
    first = _clean_first_name(full_name)
    return f"{first.capitalize()}@123"


def generate_username(full_name):
    """Lowercase first name; if taken, append 2, 3, 4... until free."""
    first = _clean_first_name(full_name).lower()
    candidate = first
    n = 2
    while db.username_exists(candidate):
        candidate = f"{first}{n}"
        n += 1
    return candidate
