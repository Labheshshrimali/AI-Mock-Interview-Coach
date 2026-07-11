import soundfile as sf
import numpy as np
import requests

# 1. Create a dummy audio file (3 seconds of random noise)
sr = 16000
audio_data = np.random.randn(sr * 3) * 0.1 
sf.write("dummy_test.wav", audio_data, sr)

# 2. Send it to the FastAPI endpoint
url = "http://localhost:8000/session/demo/answer"
files = {'audio': ('dummy_test.wav', open('dummy_test.wav', 'rb'), 'audio/wav')}
data = {'question': 'Tell me about a time you disagreed with a teammate.'}

print("Sending request to FastAPI...")
try:
    response = requests.post(url, files=files, data=data)
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print("Error:", e)
