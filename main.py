
import subprocess
from pyngrok import ngrok
import requests

# Set the ngrok authentication token
ngrok.set_auth_token("2cPw5QwrSvEFWsSvwXCSwqFXsRf_5s7zCyKP9RPgCvV5y8rbk")

# Establish a tunnel to the local port 11434
ngrok_tunnel = ngrok.connect(11434)

# Make a GET request to the ngrok tunnel URL
response = requests.get(ngrok_tunnel.public_url)

# Check the response status code
if response.status_code == 200:
    print("Success! Your request was received.")
    # Print the response content
    print(response.text)

    # Example: Execute a command through the ngrok tunnel
    command_to_execute = "ollama --version"
    # Use subprocess.Popen for more control over the subprocess
    process = subprocess.Popen(command_to_execute, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Communicate with the process
    stdout, stderr = process.communicate(input=b'\n')  # Sending a newline to simulate user pressing enter
    print("Command Output:")
    print(stdout.decode())  # Assuming the command output is text
    print("Command Error (if any):")
    print(stderr.decode())  # Print stderr

else:
    print(f"Error: {response.status_code} - {response.reason}")
