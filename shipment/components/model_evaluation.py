
import os
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from shipment.logger import logging
from shipment.exception import shippingException

from shipment.entity.config_entity import ModelEvaluationConfig
from shipment.entity.artifact_entity import (
    ModelTrainerArtifacts,
    ModelEvaluationArtifacts
)


class ModelEvaluation:

    def __init__(
        self,
        model_evaluation_config: ModelEvaluationConfig,
        model_trainer_artifact: ModelTrainerArtifacts
    ):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:

        logging.info(
            "Entered initiate_model_evaluation method"
        )

        try:

            # Create evaluation artifact directory
            os.makedirs(
                self.model_evaluation_config.MODEL_EVALUATION_ARTIFACTS_DIR,
                exist_ok=True
            )

            # Load test data
            test_df = pd.read_csv(
                self.model_evaluation_config.TEST_DATA_FILE_PATH
            )

            logging.info("Loaded test data")

            # Separate input and target
            X_test = test_df.iloc[:, :-1]
            y_test = test_df.iloc[:, -1]

            # Load trained model
            model = self.model_evaluation_config.UTILS.load_object(
                self.model_trainer_artifact.trained_model_file_path
            )

            logging.info("Loaded trained model")

            # Prediction
            y_pred = model.predict(X_test)

            logging.info("Prediction completed")

            # Evaluation metrics
            r2 = r2_score(y_test, y_pred)

            rmse = np.sqrt(
                mean_squared_error(y_test, y_pred)
            )

            mae = mean_absolute_error(
                y_test, y_pred
            )

            logging.info(f"R2 Score: {r2}")
            logging.info(f"RMSE: {rmse}")
            logging.info(f"MAE: {mae}")

            print(f"R2 Score: {r2}")
            print(f"RMSE: {rmse}")
            print(f"MAE: {mae}")

            # Model acceptance
            is_model_accepted = r2 > 0

            evaluation_artifact = ModelEvaluationArtifacts(
                evaluation_score=r2,
                is_model_accepted=is_model_accepted
            )

            return evaluation_artifact

        except Exception as e:
            raise shippingException(e, sys) from e