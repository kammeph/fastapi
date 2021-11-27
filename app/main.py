from dotenv.main import find_dotenv
from fastapi import FastAPI, APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from user.routes import users
from dotenv import load_dotenv
from utils.providers import provider
from pythondi import configure

load_dotenv(find_dotenv())
configure(provider=provider)

router = APIRouter(prefix="/api")
router.include_router(users)

app = FastAPI(
    title="FastAPI",
    description="A FastAPI MongoDB Application",
    version="1.0.0",
    contact= {
        "name": "Philipp Kammerer"
    },
    openapi_url="/openapi",
    routes=router.routes,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=exc.args)
