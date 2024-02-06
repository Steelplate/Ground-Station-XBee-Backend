import socket
import ssl

hostname = 'hprc-test.entflammen.com'
context = ssl.create_default_context()

with socket.create_connection((hostname, 8000)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())
        print(ssock.server_hostname)