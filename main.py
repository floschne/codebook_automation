import uvicorn
import json
from fastapi import FastAPI

from api.routers import dummy

# create the main app
app = FastAPI()

# include the routers
app.include_router(dummy.router)

# load config file
config = json.load(open("./config.json", "r"))

if __name__ == "__main__":
    # read port from config
    port = config['api_port']
    assert port is not None and isinstance(port, int), "The api_port has to be an integer! E.g. 8081"

    uvicorn.run(app, host="0.0.0.0", port=port)
