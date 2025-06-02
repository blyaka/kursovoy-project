import requests

files = {}

log_paths = {
    "auth": "/var/log/auth.log",
    "syslog": "/var/log/syslog"
}

for key, path in log_paths.items():
    try:
        files[key] = open(path, 'rb')
    except Exception as e:
        print(f"[!] {path} не найден или недоступен: {e}")

try:
    r = requests.post("http://192.168.0.103:5000/api/upload-system", files=files)
    print(f"[SEND_SYSTEM_LOGS] {r.status_code} — {r.text}")
except Exception as e:
    print(f"[SEND_SYSTEM_LOGS] Ошибка отправки: {e}")
finally:
    for f in files.values():
        f.close()
