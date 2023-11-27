import socket


class useful_functions:
    @staticmethod
    def get_ip_address():
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)

            return ip_address
        except socket.error as e:
            print(f"Error: {e}")
            return None
