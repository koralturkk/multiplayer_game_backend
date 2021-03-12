
import uvicorn
from fastapi import FastAPI
from .api.api import router as api_router
from .settings.config import PROJECT_NAME
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo

app = FastAPI(title=PROJECT_NAME)
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
app.include_router(api_router)

# Running of app.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

