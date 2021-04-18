import requests
import json

def get_cat_picture():
    r = requests.get('https://aws.random.cat/meow')
    cat_api_result = json.loads(r.text)
    cat_pic_url = cat_api_result.get('file')
    cat_pic_req = requests.get(cat_pic_url)
    filename = cat_pic_url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(cat_pic_req.content)
    return filename

get_cat_picture()