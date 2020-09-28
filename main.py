import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import dummy, model, prediction

# create the main app
app = FastAPI()

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


# load config file
config = json.load(open("./config.json", "r"))

if __name__ == "__main__":
    # read port from config
    port = config['api_port']
    assert port is not None and isinstance(port, int), "The api_port has to be an integer! E.g. 8081"

    uvicorn.run(app, host="0.0.0.0", port=port)
