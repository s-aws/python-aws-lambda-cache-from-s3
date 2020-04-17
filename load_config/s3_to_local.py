import json
import boto3

# defaults
myfileconfig = {
    'localdir': '/tmp', 'filename': 'CHANGE.ME',
    'write': 'w', 'read': 'r'}
    
mys3config = {
    'bucketname': 'CHANGE.ME', 'prefix': '/',
    'regionname': 'CHANGE.ME', 'service': 's3'}
    
def get_local_config(**kwargs):
    global myfileconfig, mys3config
    for keyn, valu in kwargs.items():
        try: 
            if myfileconfig[keyn] is not None:
                myfileconfig[keyn] = valu
        except:
            if mys3config[keyn] is not None:
                mys3config[keyn] = valu
    filename = myfileconfig['filename']
    directory = myfileconfig['localdir']
    filepath = directory + '/' + filename
    readaction = myfileconfig['read']
    writeaction = myfileconfig['write']
    try:
        file = open(filepath, readaction)
        configuration = file.read()
        file.close()
        print('read configuration from disk')
        try:
            json.loads(configuration)
            return configuration            
        except Exception as e:
            print('unable to load local config: "{}"'.format(e))
    except: 
        print('no config file exists')
    configuration = __get_json_from_s3_bucket()
    try:
        file = open(filepath, writeaction)
        file.write(configuration)
        file.close()
        print('wrote configuration to disk')
        return configuration
    except Exception as e:
        print('failed to read/write configuration to disk "{}"'.format(e))

def __get_json_from_s3_bucket():
    key = mys3config['prefix'] + myfileconfig['filename']
    bucket = mys3config['bucketname']
    region = mys3config['regionname']
    service = mys3config['service']
    s3 = boto3.resource(service, region_name = region)
    try:
        print("load_config.py is fetching {}..".format(key))
        configuration = s3.Object(bucket, key)
        print("successfully got {}".format(key))
        return configuration.get()['Body'].read().decode('utf-8')
    except Exception as e:
        print(e)
        