import traceback

from .train_controller import TrainController
from typing import DefaultDict
import threading

class TrainControllerManager:

    def __init__(self, train_signals) -> None:
        self._train_controllers = DefaultDict(TrainController)
        self._train_signals = train_signals
        self.update()

    def update(self, thread=True):
        # Get keys
        train_signals = set(self._train_signals.keys())
        train_controller_keys = set(self._train_controllers.keys())

        # Update trains
        trains_to_add = train_signals - train_controller_keys
        trains_to_remove = train_controller_keys - train_signals

        for i in trains_to_add:
            self.add(self._train_signals[i], i)

        for i in trains_to_remove:
            self.remove(i)

        # Update trains
        for train in self._train_controllers.values():
            train.update()

        if thread:
            threading.Timer(0.01, self.update).start()

    def add(self, signals, train_id: int = None):
        if train_id is None:
            train_id = len(self._train_controllers) + 1
        self._train_controllers[train_id] = TrainController(signals)
    def remove(self, train_id: int):
        self._train_controllers.pop(train_id)

    def get_ids(self):
        return self._train_controllers.keys()

    def launch_ui(self, train_id: int):
        print("Launching UI for train " + str(train_id))
        try:
            # Create a TrainModel instance with the required 'train_signals' argument
            self._train_controllers[train_id] = TrainController(self._train_signals[train_id])

            # Now you can call the 'launch_tm_ui' method
            self._train_controllers[train_id].launch_tc_ui()

        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()
            print("Train model not initialized yet in track_controller_track_model_api's train_info dictionary")