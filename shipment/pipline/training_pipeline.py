import sys

from shipment.exception import shippingException
from shipment.logger import logging

from shipment.configuration.mongo_operation import MongoDBOperation

from shipment.entity.artifact_entity import (
    DataIngestionArtifacts,
    DataValidationArtifacts,
    DataTransformationArtifacts,
    ModelTrainerArtifacts,
    ModelEvaluationArtifacts,
    ModelPusherArtifacts
)

from shipment.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)

from shipment.components.data_ingestion import DataIngestion
from shipment.components.data_validation import DataValidation
from shipment.components.data_transformation import DataTransformation
from shipment.components.model_trainer import ModelTrainer
from shipment.components.model_evaluation import ModelEvaluation
from shipment.components.model_pusher import ModelPusher


class TrainPipeline:

    def __init__(self):

        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()

        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

        self.mongo_op = MongoDBOperation()

    # ---------------------------------------------------------
    # Data Ingestion
    # ---------------------------------------------------------

    def start_data_ingestion(self) -> DataIngestionArtifacts:

        logging.info(
            "Entered the start_data_ingestion method of TrainPipeline class"
        )

        try:

            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
                mongo_op=self.mongo_op
            )

            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            logging.info(
                "Got the train_set and test_set from mongodb"
            )

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    # ---------------------------------------------------------
    # Data Validation
    # ---------------------------------------------------------

    def start_data_validation(
        self,
        data_ingestion_artifact: DataIngestionArtifacts
    ) -> DataValidationArtifacts:

        logging.info(
            "Entered the start_data_validation method of TrainPipeline class"
        )

        try:

            data_validation = DataValidation(
                data_ingestion_artifacts=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = (
                data_validation.initiate_data_validation()
            )

            logging.info(
                "Performed the data validation operation"
            )

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    # ---------------------------------------------------------
    # Data Transformation
    # ---------------------------------------------------------

    def start_data_transformation(
        self,
        data_ingestion_artifact: DataIngestionArtifacts
    ) -> DataTransformationArtifacts:

        logging.info(
            "Entered the start_data_transformation method "
            "of TrainPipeline class"
        )

        try:

            data_transformation = DataTransformation(
                data_ingestion_artifacts=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                "Exited the start_data_transformation method "
                "of TrainPipeline class"
            )

            return data_transformation_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    # ---------------------------------------------------------
    # Model Training
    # ---------------------------------------------------------

    def start_model_trainer(
        self,
        data_transformation_artifact: DataTransformationArtifacts
    ) -> ModelTrainerArtifacts:

        logging.info(
            "Entered the start_model_trainer method "
            "of TrainPipeline class"
        )

        try:

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = (
                model_trainer.initiate_model_trainer()
            )

            logging.info(
                "Model training completed"
            )

            logging.info(
                "Exited the start_model_trainer method "
                "of TrainPipeline class"
            )

            return model_trainer_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    # ---------------------------------------------------------
    # Model Evaluation
    # ---------------------------------------------------------

    def start_model_evaluation(
        self,
        model_trainer_artifact: ModelTrainerArtifacts
    ) -> ModelEvaluationArtifacts:

        logging.info(
            "Entered the start_model_evaluation method "
            "of TrainPipeline class"
        )

        try:

            model_evaluation = ModelEvaluation(
                model_evaluation_config=self.model_evaluation_config,
                model_trainer_artifact=model_trainer_artifact
            )

            model_evaluation_artifact = (
                model_evaluation.initiate_model_evaluation()
            )

            logging.info(
                "Model evaluation completed"
            )

            logging.info(
                "Exited the start_model_evaluation method "
                "of TrainPipeline class"
            )

            return model_evaluation_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    # ---------------------------------------------------------
    # Model Pusher
    # ---------------------------------------------------------

    def start_model_pusher(
        self,
        model_trainer_artifact: ModelTrainerArtifacts
    ) -> ModelPusherArtifacts:

        logging.info(
            "Entered the start_model_pusher method "
            "of TrainPipeline class"
        )

        try:

            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config,
                model_trainer_artifact=model_trainer_artifact
            )

            model_pusher_artifact = (
                model_pusher.initiate_model_pusher()
            )

            logging.info(
                "Model pusher completed"
            )

            logging.info(
                "Exited the start_model_pusher method "
                "of TrainPipeline class"
            )

            return model_pusher_artifact

        except Exception as e:
            raise shippingException(e, sys) from e

    # ---------------------------------------------------------
    # Run Complete Pipeline
    # ---------------------------------------------------------

    def run_pipeline(self) -> None:

        logging.info(
            "Entered the run_pipeline method of TrainPipeline class"
        )

        try:

            # 1. Data Ingestion
            data_ingestion_artifact = (
                self.start_data_ingestion()
            )

            # 2. Data Validation
            data_validation_artifact = (
                self.start_data_validation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )

            # 3. Data Transformation
            data_transformation_artifact = (
                self.start_data_transformation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )

            # 4. Model Training
            model_trainer_artifact = (
                self.start_model_trainer(
                    data_transformation_artifact=data_transformation_artifact
                )
            )

            # 5. Model Evaluation
            model_evaluation_artifact = (
                self.start_model_evaluation(
                    model_trainer_artifact=model_trainer_artifact
                )
            )

            # 6. Model Pusher
            if model_evaluation_artifact.is_model_accepted:

                model_pusher_artifact = (
                    self.start_model_pusher(
                        model_trainer_artifact=model_trainer_artifact
                    )
                )

                logging.info(
                    "Model accepted and pushed successfully"
                )

            else:

                logging.info(
                    "Model evaluation failed. Model was not pushed."
                )

            logging.info(
                "Exited the run_pipeline method of TrainPipeline class"
            )

        except Exception as e:
            raise shippingException(e, sys) from e