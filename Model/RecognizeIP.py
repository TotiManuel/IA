import socket

class RecognizeIP:
    def __init__(self):
        pass

    def get_ip(self):
        # Get the hostname
        hostname = socket.gethostname()
        # Get the local IP address
        ip = socket.gethostbyname(hostname)
        return ip

