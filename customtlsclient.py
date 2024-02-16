import requests
import socket  # Import the socket module
from cryptography.hazmat.primitives import serialization
import requests
from cryptography.hazmat.primitives import serialization

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from cryptography.hazmat.primitives import serialization
import socket


class CustomTLSClient:
    def __init__(self, hostname, port, aes_key=None):
        self.hostname = hostname
        self.port = port
        self.aes_key = aes_key

    def generate_aes_key(self):
        if self.aes_key is None:
            # Generate a random AES key if not provided
            self.aes_key = serialization.load_pem_private_key(
                open("private_key.pem", "rb").read(),
                password=None,
                backend=default_backend()
            )

    def http_get(self, path="/"):
        try:
            # Generate AES key if not provided
            self.generate_aes_key()

            # Prepare the URL
            url = f"https://{self.hostname}{path}"

            # Create a session with requests library
            session = requests.Session()

            # Set up a custom transport adapter for encryption
            session.mount('https://', CustomAdapter(self.aes_key))

            # Make the HTTP GET request
            response = session.get(url)

            # Print the response
            print("Server response:", response.text)

        except requests.RequestException as e:
            print("HTTP Error:", e)

    def http_post(self, path="/", data=None):
        try:
            # Generate AES key if not provided
            self.generate_aes_key()

            # Prepare the URL
            url = f"https://{self.hostname}{path}"

            # Create a session with requests library
            session = requests.Session()

            # Set up a custom transport adapter for encryption
            session.mount('https://', CustomAdapter(self.aes_key))

            print("caling post method,data=",data)
            # Make the HTTP POST request
            response = session.post(url, data=data)

            # Print the response
            print("Server response:", response.text)

        except requests.RequestException as e:
            print("HTTP Error:", e)


class CustomAdapter(HTTPAdapter):
    def __init__(self, aes_key):
        self.aes_key = aes_key
        super().__init__()

    def init_poolmanager(self, *args, **kwargs):
        self.poolmanager = CustomPoolManager(self.aes_key)

class CustomPoolManager(PoolManager):
    def __init__(self, aes_key):
        self.aes_key = aes_key
        super().__init__()

    def _new_connections(self, scheme, host, port, request_context):
        conn = super()._new_connections(scheme, host, port, request_context)
        conn.set_aes_key(self.aes_key)
        return conn

    def urlopen(self, method, url, body=None, headers=None, retries=None, redirect=True, assert_same_host=True, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, pool_timeout=None, release_conn=None, chunked=False, body_pos=None, **response_kw):
        response_kw['response_class'] = CustomHTTPResponse
        return super().urlopen(method, url, body=body, headers=headers, retries=retries, redirect=redirect, assert_same_host=assert_same_host, timeout=timeout, pool_timeout=pool_timeout, release_conn=release_conn, chunked=chunked, body_pos=body_pos, **response_kw)

class CustomHTTPResponse(requests.packages.urllib3.response.HTTPResponse):
    def __init__(self, *args, **kwargs):
        self.aes_key = None
        super().__init__(*args, **kwargs)

    def set_aes_key(self, aes_key):
        self.aes_key = aes_key

    def _decode(self, content, charset, json_decoder):
        if self.aes_key:
            content = decrypt_content(content, self.aes_key)
        return super()._decode(content, charset, json_decoder)

def decrypt_content(content, aes_key):
    decrypted_content = content  # Placeholder for decryption logic
    return decrypted_content