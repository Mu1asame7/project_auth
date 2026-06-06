import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
