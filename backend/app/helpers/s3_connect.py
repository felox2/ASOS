from app.config import settings
from fastapi import HTTPException
import boto3
import uuid

class S3Connect:
     def uploadFile(file):

        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.ACCESS_KEY_ID,
                aws_secret_access_key=settings.ACCESS_KEY_SECRET,
                endpoint_url=settings.INTERNAL_STORAGE_URL,
                
            )

            print(s3_client)
            random_uuid = str(uuid.uuid4())
            file_name = f"{random_uuid}"
            
            s3_client.upload_fileobj(
                file.file if hasattr(file, 'file') else file,  
                settings.BUCKET,
                file_name 
            )

            return f"{settings.EXTERNAL_STORAGE_URL}/{settings.BUCKET}/{file_name}"
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))