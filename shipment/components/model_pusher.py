import os
import sys
import shutil

from shipment.logger import logging
from shipment.exception import shippingException

from shipment.configuration.s3_operation import S3Operation

from shipment.entity.config_entity import ModelPusherConfig
from shipment.entity.artifact_entity import (
    ModelTrainerArtifacts,
    ModelPusherArtifacts
)


class ModelPusher:

    def __init__(
        self,
        model_pusher_config: ModelPusherConfig,
        model_trainer_artifact: ModelTrainerArtifacts
    ):
        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifact = model_trainer_artifact

        # Create S3 operation object
        self.s3_operation = S3Operation()

    def initiate_model_pusher(self) -> ModelPusherArtifacts:

        logging.info(
            "Entered initiate_model_pusher method"
        )

        try:

            # --------------------------------------------------
            # 1. Create local model pusher directory
            # --------------------------------------------------

            os.makedirs(
                self.model_pusher_config.MODEL_PUSHER_ARTIFACTS_DIR,
                exist_ok=True
            )

            # --------------------------------------------------
            # 2. Source model
            # --------------------------------------------------

            source_model_path = (
                self.model_trainer_artifact.trained_model_file_path
            )

            # --------------------------------------------------
            # 3. Local destination model
            # --------------------------------------------------

            destination_model_path = (
                self.model_pusher_config.PUSHED_MODEL_FILE_PATH
            )

            # --------------------------------------------------
            # 4. Copy model locally
            # --------------------------------------------------

            shutil.copy(
                source_model_path,
                destination_model_path
            )

            logging.info(
                f"Model copied locally to: "
                f"{destination_model_path}"
            )

            print(
                f"Model copied locally to: "
                f"{destination_model_path}"
            )

            # --------------------------------------------------
            # 5. Upload model to AWS S3
            # --------------------------------------------------

            s3_key = (
                "models/shipping_price_model.pkl"
            )

            self.s3_operation.upload_file(
                file_path=destination_model_path,
                s3_key=s3_key
            )

            logging.info(
                f"Model uploaded to S3: {s3_key}"
            )

            print(
                f"Model uploaded to S3: {s3_key}"
            )

            # --------------------------------------------------
            # 6. Create artifact
            # --------------------------------------------------

            model_pusher_artifact = ModelPusherArtifacts(
                pushed_model_file_path=destination_model_path
            )

            return model_pusher_artifact

        except Exception as e:
            raise shippingException(e, sys) from e