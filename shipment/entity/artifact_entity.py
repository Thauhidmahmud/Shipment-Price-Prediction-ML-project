
from dataclasses import dataclass

# Data Ingestion Artifacts
@dataclass
class DataIngestionArtifacts:
    train_data_file_path:str
    test_data_file_path:str


@dataclass
class DataValidationArtifacts:
    data_drift_file_path: str
    validation_status: bool