import os
import sys

sys.path.append(str(os.getcwd()))

from backend import DataHandler, RedisHandler, DatasetManager, ModelFactory, ModelManager, Predictor, Trainer


def pytest_runtest_setup(item):
    # TODO define test logger
    try:
        print(f"Instantiating singletons for {str(item)}...")
        # instantiate singletons
        DataHandler()
        RedisHandler()
        DatasetManager()
        ModelFactory()
        ModelManager()
        Predictor()
        Trainer()
    except Exception:
        raise SystemExit("Error while starting singletons!")
