import os
import sys
import cv2
import csv
import boto3

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import controllers.controller as cont

from datetime import datetime
from dotenv import load_dotenv
from models.schemas import User

load_dotenv(dotenv_path='.env')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY_ID')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET = os.getenv('AWS_BUCKET')
AWS_BUCKET_FOLDER = os.getenv('AWS_BUCKET_FOLDER')
AWS_BUCKET_AUDIT_LOG_FOLDER = os.getenv('AWS_BUCKET_AUDIT_LOG_FOLDER')

class S3Controller:
    def __init__(self):
        '''
        Initializes connection with AWS S3 and creates an s3 client.
        '''
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

    def uploadImage(self, image, image_name) -> str | None:
        '''
        Uploads an image to the S3 bucket folder provided the image and the image name.

        params:
        - image => the image read by cv2.imread() function
        - image_name => the name of the image to be stored in s3

        returns:
        - url: str => the URL path of the image uploaded in the s3 bucket folder
        - None => if the image encoding fails
        '''
        success, buffer = cv2.imencode('.jpg', image)

        if not success:
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/s3controller.py uploadImage() - failed to encode image {image_name}\n')
            return None

        img_bytes = buffer.tobytes()
        s3_key = f'{AWS_BUCKET_FOLDER}/{image_name}.jpg'
        self.s3.put_object(
            Bucket=AWS_BUCKET,
            Key=s3_key,
            Body=img_bytes,
            ContentType='image/jpeg'
        )

        url = f'https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}'
        return url
    
    def updateAuditLog(self, event: str, desc: str, user: User) -> bool:
        s3_key = f'{AWS_BUCKET_AUDIT_LOG_FOLDER}/audit-log.csv'
    
        try:
            self.s3.download_file(AWS_BUCKET, s3_key, 'tempReports/auditLog.csv')

            with open('tempReports/auditLog.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime('%m/%d/%Y %H:%M:%S'), event, desc, user.id, user.username, user.email])
            
            self.s3.upload_file('tempReports/auditLog.csv', AWS_BUCKET, s3_key)
            os.remove('tempReports/auditLog.csv')
            return True
        except Exception as e:
            with open('logs.txt', 'a') as file:
                now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                file.write(f'[{now}] Error at function invocation controllers/s3controller.py updateAuditLog() - {repr(e)}\n')
            return False