
import os
import sys
import shutil

from shipment.logger import logging
from shipment.exception import shippingException

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

    def initiate_model_pusher(self) -> ModelPusherArtifacts:

        logging.info(
            "Entered initiate_model_pusher method"
        )

        try:

            # Create model pusher directory
            os.makedirs(
                self.model_pusher_config.MODEL_PUSHER_ARTIFACTS_DIR,
                exist_ok=True
            )

            # Source model
            source_model_path = (
                self.model_trainer_artifact.trained_model_file_path
            )

            # Destination model
            destination_model_path = (
                self.model_pusher_config.PUSHED_MODEL_FILE_PATH
            )

            # Copy model
            shutil.copy(
                source_model_path,
                destination_model_path
            )

            logging.info(
                f"Model pushed to: {destination_model_path}"
            )

            print(
                f"Model pushed to: {destination_model_path}"
            )

            model_pusher_artifact = ModelPusherArtifacts(
                pushed_model_file_path=destination_model_path
            )

            return model_pusher_artifact

        except Exception as e:
            raise shippingException(e, sys) from e