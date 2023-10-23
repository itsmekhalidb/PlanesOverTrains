import traceback

from .train_model import TrainModel
from typing import DefaultDict
import threading

from api.train_model_train_controller_api import TrainModelTrainControllerAPI
from api.track_model_train_model_api import TrackModelTrainModelAPI

class TrainModelManager:

    # def __init__(self, train_signals) -> None:
    def __init__(self, train_signals, track_signals) -> None:
        self._train_models = DefaultDict(TrainModel)
        self._train_signals = train_signals
        # self._track_signals = track_signals

        self._track_to_train_signals = track_signals
        self.update()

    def update(self, thread=True):
        # Get keys
        # track_to_train_keys = set(self._track_to_train_signals.get_keys())
        train_model_keys = set(self._train_models.keys())

        # Update trains
        # trains_to_add = track_to_train_keys - train_model_keys
        # trains_to_remove = train_model_keys - track_to_train_keys

        # for i in trains_to_add:
        #     self.add(self._track_to_train_signals[i], i)
        #
        # for i in trains_to_remove:
        #     self.remove(i)

        for train in self._train_models.values():
            train.update()

        if thread:
            threading.Timer(0.01, self.update).start()

    # def add(self, track_to_train_signals: TrackToTrainSignals, train_id):
    #     if train_id is None:
    #         train_id = len(self._train_models) + 1
    #     ts = TrainSignals()
    #     self._train_signals[train_id] = ts
    #     self._train_models[train_id] = TrainModel(ts, track_to_train_signals)

    # def remove(self, train_id: int):
    #     self._train_signals.pop(train_id)
    #     self._train_models.pop(train_id)

    def get_ids(self):
        return self._train_models.keys()

    def launch_ui(self, train_id: int):
        print("Launching UI for train " + str(train_id))

        try:
            # Create a TrainModel instance with the required 'train_signals' argument
            self._train_models[train_id] = TrainModel(self._train_signals, self._track_to_train_signals)

            # Now you can call the 'launch_tm_ui' method
            self._train_models[train_id].launch_tm_ui()

        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()
            print("Train model not initialized yet")