import os
import sys
import json
import boto3

def delete_bucket(bucketName):
    s3 = boto3.client('s3')
    object_list = []
    try:
        versionConfig = {
            "Status": "Suspended"
        }
        s3.put_bucket_versioning(Bucket=bucketName,VersioningConfiguration=versionConfig)
        object_vers = s3.list_object_versions(Bucket=bucketName)
        for ver in object_vers['Versions']:
            key = ver['Key']
            versionId = ver['VersionId']
            #print("Object Key = %s, Version = %s" % (key, versionId))
            s3.delete_object(Bucket=bucketName,Key=key,VersionId=versionId)
            print("Deleted Object: %s, Version: %s" % (key, versionId))
    except Exception as e:
        print("Error while deleting bucket",e)

def usage():
    print("usage: python delete_versioned_bucket_objects.py <bucket_name>")
    sys.exit(0)

def main():
    if len(sys.argv) != 2:
        usage()
    bucketName = sys.argv[1]
    delete_bucket(bucketName)

if __name__ == "__main__":
    main()
