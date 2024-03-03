import json
import sys
import requests

r = requests.get('https://g.tenor.com/v1/random?q=dance&key=6BJKOZE8D7M2&limit=1')

if r.status_code != 200:
    print("Error!")
    sys.exit(1)

print("Got a response")
data = json.loads(r.text)
url = data['results'][0]['media'][0]['gif']['url']
print(url)


dictionary = {
    "results": [
        {
            "media": [
                {
                    "gif": {
                    }
                }
            ]
        }
    ]
}
