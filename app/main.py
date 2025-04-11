from fastapi import FastAPI
from app.db import init_db

app = FastAPI(title="DSTU Diploma | AuthService", docs_url="/swagger")
init_db(app)
