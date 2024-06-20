### Book Cover Segmentation

#### HTTP Request
```
https://bcs-litswap-api-au43kti5qq-et.a.run.app/process
```
#### Parameters

| Parameters    |               | Description  |
| ------------- |:-------------:| -------------|
| filename   | required	  	| `filename` of the book cover image you want to segment that have been already in Google Cloud Storage Bucket|

#### Result

| Parameters    |  Description  |
| ------------- |:--------------|
| | Public URL of the segmented image|


#### Example
```python
import requests
import time

url = "https://bcs-litswap-api-au43kti5qq-et.a.run.app/process"
# Path to image file
starttime = time.time()
results = requests.post(url, data={"filename":"1718449683199_a91.jpg"})
print("time taken:", time.time() - starttime)
print(results.text)
```

```
time taken: 0.8115460872650146
https://storage.googleapis.com/books-litswap/bookImages/processed/1718449683199_a91.jpg
```
