
import os
from os import environ
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACTS_DIR = os.path.join(os.getcwd(), "artifacts", TIMESTAMP)


MODEL_CONFIG_FILE = "config/model.yaml"
SCHEMA_FILE_PATH = "config/schema.yaml"

DB_URL = environ["MONGO_DB_URL"]
TEST_SIZE=0.2


# Database related constants
DB_NAME = "ShipmentDB"
COLLECTION_NAME = "Shipment_collection"

# Data Ingestion related constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
DATA_INGESTION_TRAIN_DIR = "Train"
DATA_INGESTION_TEST_DIR = "Test"
DATA_INGESTION_TRAIN_FILE_NAME = "train.csv"
DATA_INGESTION_TEST_FILE_NAME = "test.csv"



# Data Validation related constants
DATA_VALIDATION_ARTIFACT_DIR = "DataValidationArtifacts"
DATA_DRIFT_FILE_NAME = "DataDriftReport.yaml"