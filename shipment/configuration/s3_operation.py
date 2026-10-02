import sys
import boto3
import pandas as pd

from io import BytesIO
from pandas import DataFrame

from shipment.constants import S3_BUCKET_NAME
from shipment.exception import shippingException
from shipment.logger import logging


class S3Operation:

    def __init__(self):
        logging.info("Entered S3Operation class")

        try:
            self.bucket_name = S3_BUCKET_NAME
            self.s3_client = boto3.client("s3")

            logging.info(
                f"S3 client created successfully for bucket: {self.bucket_name}"
            )

        except Exception as e:
            raise shippingException(e, sys) from e

    def upload_file(self, file_path: str, s3_key: str):
        """
        Upload a local file to S3.

        file_path:
            Local file path.

        s3_key:
            File path inside S3 bucket.
            Example: models/shipping_price_model.pkl
        """

        logging.info("Entered upload_file method")

        try:
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=self.bucket_name,
                Key=s3_key
            )

            logging.info(
                f"Successfully uploaded {file_path} to s3://"
                f"{self.bucket_name}/{s3_key}"
            )

        except Exception as e:
            raise shippingException(e, sys) from e

    def download_file(self, s3_key: str, local_file_path: str):
        """
        Download a file from S3 to local machine.
        """

        logging.info("Entered download_file method")

        try:
            self.s3_client.download_file(
                Bucket=self.bucket_name,
                Key=s3_key,
                Filename=local_file_path
            )

            logging.info(
                f"Successfully downloaded s3://"
                f"{self.bucket_name}/{s3_key}"
                f" to {local_file_path}"
            )

        except Exception as e:
            raise shippingException(e, sys) from e

    def read_csv(self, s3_key: str) -> DataFrame:
        """
        Read a CSV file directly from S3 into pandas DataFrame.
        """

        logging.info("Entered read_csv method")

        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            df = pd.read_csv(response["Body"])

            logging.info(
                f"Successfully read CSV from "
                f"s3://{self.bucket_name}/{s3_key}"
            )

            return df

        except Exception as e:
            raise shippingException(e, sys) from e

    def list_files(self, prefix: str = ""):
        """
        List files inside S3 bucket.

        prefix:
            Example:
            models/
            data/
        """

        logging.info("Entered list_files method")

        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )

            files = []

            if "Contents" in response:
                for obj in response["Contents"]:
                    files.append(obj["Key"])

            logging.info(
                f"Found {len(files)} files with prefix '{prefix}'"
            )

            return files

        except Exception as e:
            raise shippingException(e, sys) from e