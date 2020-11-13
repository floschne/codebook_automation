import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import general, model, prediction, training
from backend.exceptions import ModelNotAvailableException, ErroneousMappingException, ErroneousModelException, \
    ModelMetadataNotAvailableException, PredictionError, ModelInitializationException, ErroneousDatasetException, \
    NoDataForCodebookException, DatasetNotAvailableException, InvalidModelIdException
from logger import backend_logger

# create the main app
app = FastAPI(title="Codebook Automation API",
              description="An easy to use API for AI based prediction of Codebook Tags for CodeAnno documents.",
              version="beta")


@app.on_event("startup")
async def startup_event():
    # TODO apply app specific configs here
    pass


# include the routers
app.include_router(general.router)
app.include_router(model.router, prefix=model.PREFIX)
app.include_router(prediction.router, prefix=prediction.PREFIX)
app.include_router(training.router, prefix=training.PREFIX)


# custom exception handlers
@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


@app.exception_handler(ModelNotAvailableException)
async def model_not_available_exception_handler(request: Request, exc: ModelNotAvailableException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


@app.exception_handler(ModelInitializationException)
async def model_initialization_exception_handler(request: Request, exc: ModelInitializationException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message,
                 "caused_by": exc.caused_by}
    )


@app.exception_handler(ErroneousMappingException)
async def erroneous_mapping_exception_handler(request: Request, exc: ErroneousMappingException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )


@app.exception_handler(ErroneousModelException)
async def erroneous_model_exception_handler(request: Request, exc: ErroneousModelException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


@app.exception_handler(ModelMetadataNotAvailableException)
async def model_metadata_not_available_exception_handler(request: Request, exc: ModelMetadataNotAvailableException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


@app.exception_handler(ErroneousDatasetException)
async def erroneous_dataset_exception_handler(request: Request, exc: ErroneousDatasetException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message,
                 "caused_by": exc.caused_by}
    )


@app.exception_handler(NoDataForCodebookException)
async def no_data_for_codebook_exception_handler(request: Request, exc: NoDataForCodebookException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


@app.exception_handler(InvalidModelIdException)
async def invalid_model_id_exception_exception_handler(request: Request, exc: InvalidModelIdException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


@app.exception_handler(DatasetNotAvailableException)
async def dataset_not_available_exception_exception_handler(request: Request, exc: DatasetNotAvailableException):
    backend_logger.error(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


if __name__ == "__main__":
    # load config file
    config = json.load(open("./config.json", "r"))

    # read port from config
    port = config['api']['api_port']
    assert port is not None and isinstance(port, int), "The api_port has to be an integer! E.g. 8081"

    uvicorn.run(app, host="0.0.0.0", port=port, debug=True)
