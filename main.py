import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import dummy, model, prediction

# create the main app
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # TODO apply app specific configs here
    pass


# include the routers
app.include_router(dummy.router)
app.include_router(model.router, prefix=model.PREFIX)
app.include_router(prediction.router, prefix=prediction.PREFIX)


# custom exception handlers
@app.exception_handler(model.ModelNotFoundException)
async def model_not_found_exception_handler(request: Request, exc: model.ModelNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Model not found!"}  # TODO better message
    )


if __name__ == "__main__":
    # load config file
    config = json.load(open("./config.json", "r"))

    # read port from config
    port = config['api']['api_port']
    assert port is not None and isinstance(port, int), "The api_port has to be an integer! E.g. 8081"

    print("hello main")

    uvicorn.run(app, host="0.0.0.0", port=port)
