
import sys
from shipment.exception import shippingException
from shipment.logger import logging
from shipment.configuration.mongo_operation import MongoDBOperation
from shipment.entity.artifact_entity import (DataIngestionArtifacts)

from shipment.entity.config_entity import (DataIngestionConfig)

from shipment.components.data_ingestion import DataIngestion

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.mongo_op = MongoDBOperation()


         # This method is used to start the data ingestion
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config, mongo_op=self.mongo_op
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact

        except Exception as e:
            raise shippingException(e, sys) from e


    # This method is used to start the training pipeline
    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
    
            logging.info("Exited the run_pipeline method of TrainPipeline class")

        except Exception as e:
            raise shippingException(e, sys) from e 