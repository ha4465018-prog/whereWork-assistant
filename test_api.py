import urllib.request
import urllib.error
try:
    response = urllib.request.urlopen("http://127.0.0.1:8000/chat?query=hello")
    print(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("Error:", e.code)
    print(e.read().decode("utf-8"))
