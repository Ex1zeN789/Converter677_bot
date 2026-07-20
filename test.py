import requests

try:
    response = requests.get("https://api.telegram.org", timeout=10)
    print("Статус:", response.status_code)
    print(response.text)
except Exception as e:
    print("Ошибка:", e)