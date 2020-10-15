import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import general, model, prediction
from backend import ModelNotAvailableException, ErroneousMappingException, ErroneousModelException, \
    ModelMetadataNotAvailableException
from logger import backend_logger

# create the main app
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # TODO apply app specific configs here
    pass


# include the routers
app.include_router(general.router)
app.include_router(model.router, prefix=model.PREFIX)
app.include_router(prediction.router, prefix=prediction.PREFIX)


# custom exception handlers
@app.exception_handler(ModelNotAvailableException)
async def model_not_available_exception_handler(request: Request, exc: ModelNotAvailableException):
    backend_logger.warn(exc.message)
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


@app.exception_handler(ErroneousMappingException)
async def erroneous_mapping_exception_handler(request: Request, exc: ErroneousMappingException):
    backend_logger.warn(exc.message)
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )


@app.exception_handler(ErroneousModelException)
async def erroneous_model_exception_handler(request: Request, exc: ErroneousModelException):
    backend_logger.warn(exc.message)
    return JSONResponse(
        status_code=500,
        content={"message": exc.message}
    )


@app.exception_handler(ModelMetadataNotAvailableException)
async def model_metadata_not_available_exception_handler(request: Request, exc: ErroneousModelException):
    backend_logger.warn(exc.message)
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
