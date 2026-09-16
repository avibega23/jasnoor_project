from pyngrok import ngrok
import subprocess
import time

ngrok.set_auth_token('3JMR5OGIChwqS8wWFi5jUrvY7mt_69bQot3dP7MFvd7rGyCL6')

public_url = ngrok.connect(8501)
print("Streamlit is running on:", public_url)

process = subprocess.Popen(["streamlit", "run", "app.py"])
process.wait()
