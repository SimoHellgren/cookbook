import os
from dotenv import load_dotenv
import uvicorn
from backend.app.main import app

if __name__ == "__main__":
    load_dotenv()

    port = os.getenv("BACKEND_PORT")

    uvicorn.run(
        "run_backend:app",
        host="0.0.0.0",
        port=port,
    )
