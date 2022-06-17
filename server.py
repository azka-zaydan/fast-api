import imp
import os
from app.main import app

if __name__ == "__main__":
    os.system("uvicorn app.main:app --reload")