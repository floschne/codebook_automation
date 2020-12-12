import os
import sys

sys.path.append(str(os.getcwd()))

from api.model import CodebookModel


def create_dummy_codebook_models(num: int):
    dummies = list()
    for i in range(num):
        dummies.append(CodebookModel(
            name=f"DummyCodebookModel{i}",
            tags=[f"DummyTag{i}{i + 1}",
                  f"DummyTag{i}{i + 2}",
                  f"DummyTag{i}{i + 3}",
                  f"DummyTag{i}{i + 4}",
                  f"DummyTag{i}{i + 5}"]))
    if num == 1:
        return dummies[0]
    return dummies
