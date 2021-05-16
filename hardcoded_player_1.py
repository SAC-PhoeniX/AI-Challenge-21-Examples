import requests
import json
import math

get_url = 'http://localhost:3000'
post_url = 'http://localhost:4000'
get_headers = {'Content-Type': 'application/json'}
post_headers = {'Content-Type': 'application/json'}

positions2go = [[110, 370],[320,370],[320,620],[680,620],[850,320]]
current_pos = []

while True:
    data = requests.get(get_url, headers=get_headers)
    jsonData = json.loads(data.text)

    current_x = float(jsonData["tankA"]["x"])
    current_y = float(jsonData["tankA"]["y"])
    current_r = float(jsonData["tankA"]["r"])

    if len(positions2go) > 0:
        print(positions2go[0], abs(positions2go[0][0] - current_x), abs(positions2go[0][1] - current_y))
        if abs(positions2go[0][0] - current_x) > 30 or abs(positions2go[0][1] - current_y) > 30:
            wanted_r_rad = math.atan2((positions2go[0][1] - current_y),(positions2go[0][0] - current_x))
            # atan2 is arctan but it chooses the right quadrant by itself. Returns between PI and -PI.
            wanted_r = -((wanted_r_rad * 180) / math.pi)
            if abs(current_r - wanted_r) <= 30:
                m, r = 1, 0
            else:
                m, r = 0, 1
        else:
            positions2go.pop(0)
            m, r = 0, 0
    else:
        m, r = 0, 0
        print("ERROR: No position specified to go.")

    f = 0

    data = {"m": m, "r":r, "f":f}
    data = json.dumps(data)
    response = requests.post(post_url, data=data, headers=post_headers)


