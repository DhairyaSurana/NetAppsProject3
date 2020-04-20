# ServicesKeys.py

import hashlib
import time

# Canvas
token = "4511~odePNgwtl0rGPjG1GkiLjhDkBFNwWmK62uLTyqehy7VYBfojkj2UHH3MSI3T0k6s"

# Marvel
pub_key = "b4682d4a14034068d4a58cf57de6b4f5"
priv_key = "730d03af4f5f5a0144e4cedb28845e9ab1a18fe2"

ts=str(time.time())
apikey = pub_key   # public key 
hash = hashlib.md5((ts + priv_key + pub_key).encode()).hexdigest()