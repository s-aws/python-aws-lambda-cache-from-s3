# python-aws-lambda-cache-from-s3
## Read a JSON from S3 and cache locally for faster reads
### Requirements:
* python modules
	* boto3
	* json
* S3 bucket
* json config file in S3
### Recommended:
* lambda

#### Usage (lambda):
```python
import json
import boto3
from load_config import get_local_config as get_config

configuration = json.loads(get_config(
    filename = 'config', # is also the keyname in S3
    localdir = '/tmp', # when caching locally
    bucketname = 'aws-sh', 
    prefix = 'config/playlistof.me/lambda/', # prepended to the keyname
    regionname = 'us-east-1'))
    
client = boto3.client(configuration['service']['name'], region_name = configuration['service']['region'])

def js_response(typeOfResponse, response):
    json_response = {
        configuration['return']['bodykeyname']: response,
        configuration['return']['statuskeyname']: typeOfResponse}
    try:
        return json_response
    except Exception as e:
        print(e)

def lambda_handler(event, context):
    try:
        response = client.list_objects_v2(Bucket = configuration['service']['bucketname'])
        return js_response(configuration['httpCode']['OK'], response['Contents'][0]['Key'])
    except Exception as e:
        print(e)
```

##### Local usage:
```bash
$ python3
```python
Python 3.7.6 (default, Feb 26 2020, 20:54:15)
[GCC 7.3.1 20180712 (Red Hat 7.3.1-6)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from load_config.s3_to_local import get_local_config as get_config
>>> configuration = get_config(
...     filename = 'config', # is also the keyname in S3
...     localdir = '/tmp', # when caching locally
...     bucketname = 'aws-sh',
...     prefix = 'config/playlistof.me/lambda/', # prepended to the keyname
...     regionname = 'us-east-1')
```