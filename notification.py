import http.client, urllib.request, urllib.parse, urllib.error, base64
import json, datetime

def notify(cam_id):
    try:
        conn = http.client.HTTPSConnection('detectorserver.azurewebsites.net')
        cam_data = {"cam_id": cam_id,
                "problems": "fight",
                "datetime": datetime.datetime.now()}
        conn.request("POST", f"/inform?cam-data=\"{cam_data}\"".replace(" ", "%20"))
        response = conn.getresponse()
        data = response.read()
        print(data)
        print(type(data))
        data = json.loads(data)
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))