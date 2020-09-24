import uvicorn
from fastapi import FastAPI

from api.model.prediction_result import PredictionResult
from logger import api_logger
from .model import PredictionRequest

api = FastAPI()


@api.get("/")
def get_root():
    return "Hello world from Codebook Automation API!"


@api.post("/info")
async def get_info(req: PredictionRequest, response_model=PredictionResult):
    api_logger.info(f"POST request on /info with %s" % req.json())
    return PredictionResult(doc_id=req.doc.doc_id,
                            proj_id=req.doc.proj_id,
                            codebook_name=req.codebook.name,
                            predicted_tag=req.codebook.tags[0])


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8080)
