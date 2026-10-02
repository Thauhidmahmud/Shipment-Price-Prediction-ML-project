import sys
import boto3
import pandas as pd

from shipment.constants import S3_BUCKET_NAME
from shipment.exception import shippingException
from shipment.logger import logging


class S3Operation:

    def __init__(self):
        try:
            logging.info("Creating S3 client")
            self.client = boto3.client("s3")
            logging.info("S3 client created successfully")
        except Exception as e:
            raise shippingException(e, sys) from e

    def upload_file(self, file_path: str, s3_key: str):
        try:
            logging.info(
                f"Uploading {file_path} to "
                f"s3://{S3_BUCKET_NAME}/{s3_key}"
            )

            self.client.upload_file(
                file_path,
                S3_BUCKET_NAME,
                s3_key
            )

            logging.info("File uploaded successfully")
            return True

        except Exception as e:
            raise shippingException(e, sys) from e

    def download_file(self, s3_key: str, local_file_path: str):
        try:
            logging.info(
                f"Downloading "
                f"s3://{S3_BUCKET_NAME}/{s3_key}"
            )

            self.client.download_file(
                S3_BUCKET_NAME,
                s3_key,
                local_file_path
            )

            logging.info("File downloaded successfully")
            return local_file_path

        except Exception as e:
            raise shippingException(e, sys) from e

    def read_csv(self, s3_key: str):
        try:
            logging.info(
                f"Reading CSV from "
                f"s3://{S3_BUCKET_NAME}/{s3_key}"
            )

            response = self.client.get_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_key
            )

            df = pd.read_csv(response["Body"])

            logging.info("CSV read successfully")
            return df

        except Exception as e:
            raise shippingException(e, sys) from e

    def list_files(self, prefix: str = ""):
        try:
            response = self.client.list_objects_v2(
                Bucket=S3_BUCKET_NAME,
                Prefix=prefix
            )

            files = []

            if "Contents" in response:
                for obj in response["Contents"]:
                    files.append(obj["Key"])

            return files

        except Exception as e:
            raise shippingException(e, sys) from e