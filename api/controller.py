import sys

from fastapi import FastAPI

import core
from .model import Document, Summary

sys.path.append('..')

api = FastAPI()


@api.post("/summary/")
async def get_summary(doc: Document, strategy: str):
    return core.summarize(doc, strategy)


@api.get("/")
def get_root():
    return "Hello world!"
