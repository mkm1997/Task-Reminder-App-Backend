import requests



data = requests.get("https://channels.readthedocs.io/en/latest/installation.html")

print(data.content)