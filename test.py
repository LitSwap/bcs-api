import requests
import time

'''
your localhost url. If running on port 5000
'''
url = "http://192.168.100.60:8080/process"
# Path to image file
starttime = time.time()
results = requests.post(url, data={"filename":"1718455790556_a13.jpg"})
print("time taken:", time.time() - starttime)
print(results.text)