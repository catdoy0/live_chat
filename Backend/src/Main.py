from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .Sql import DatabasePool, InitializeDatabase

CORS_origins = [
    "http://localhost:5173"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"""
    {app.title}
    version = {app.version}

    Creating Database and Table if not exists...
          """)
    if not InitializeDatabase.CreateDatabase() or not InitializeDatabase.CreateTables():
        print("""
        \033[31mfailed to Initialize Database
        """)
        raise RuntimeError("wtf happened")
    print("     Creating connection pool...")
    DatabasePool.init_poot()
    yield
    print("Closing...")

app = FastAPI(
    title = "Live Chat API",
    version = "0.00000000000000000000001",
    debug = True,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"]
)

@app.get("/")
def root():
    return "Hello, The Server is up!"
