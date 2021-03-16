
import uvicorn
from fastapi import FastAPI
from api.api import router as api_router
from core.config import PROJECT_NAME
from db.mongodb_utils import close_mongo_connection, connect_to_mongo
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title=PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(api_router)

# Running of app.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

