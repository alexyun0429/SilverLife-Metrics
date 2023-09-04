import http.client
import mimetypes
from codecs import encode
import base64
from PIL import Image
from io import BytesIO
import json

chosen_expression = 1 # 0: teethy smile, 1: pout, 2: sad 3: neutral, 100: generates open eyes when subject has closed eyes 

conn = http.client.HTTPSConnection("www.ailabapi.com")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=image_target; filename={0}'.format('file')))

fileType = mimetypes.guess_type("IMAGE FILE PATH")[0] or 'application/octet-stream'
dataList.append(encode('Content-Type: {}'.format(fileType)))
dataList.append(encode(''))

with open("IMAGE FILE PATH", 'rb') as f:
  dataList.append(f.read())
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=service_choice;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))
dataList.append(encode(str(chosen_expression))) # append our chosen expression 

dataList.append(encode(""))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
   'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
   'ailabapi-api-key': 'BB1FwHanL3zyKZdPtTCVKRsoQcg9qzJ1EfGi0cemp22xMHr7YUA9vdDrU56svx3X'  # added authorization API key here/can be a key from any account doesn't matter  
}
conn.request("POST", "/api/portrait/effects/emotion-editor", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# Convert bytes to string and parse as JSON
response_json = json.loads(data.decode("utf-8"))
print(response_json)

# Decode the base64 image data
img_data = base64.b64decode(response_json['data']['image'])

# Convert the image bytes to an Image object and show it
img = Image.open(BytesIO(img_data))
img.show()

