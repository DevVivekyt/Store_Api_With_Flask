"""
blocklist.py


This file just contains the blocklist of the JWT tokens. It will be imported by app and the logout resouces so that tokens can be added to the blocklist when the user logout. 
"""

BLOCKLIST = set()