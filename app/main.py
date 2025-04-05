from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException, Depends,Request
from fastapi.responses import JSONResponse
from app.models import *
from app.database import init_db, Session, get_session
from typing import Annotated
from sqlmodel import select
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]

# class UnicornException(Exception):
#     def __init__(self, name: str,statuscode:int):
#         self.name = name
#         self.status_code = statuscode

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )

@app.get("/product/")
async def get_all_product(session:SessionDep):
    statement = select(Product).order_by(Product.order)
    result = session.exec(statement).all()
    return result

@app.get("/product/{id}")
async def get_product_by_product_id(id,session:SessionDep):
    statement = select(Product).where(Product.productCode == id)
    result = session.exec(statement).first()
    return result

@app.post("/add-product/")
async def add_product(product: Product, session:SessionDep):
    statement  = select(Product).where(Product.name == product.name)
    existing_product = session.exec(statement).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    try:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    except:
        raise HTTPException(status_code=400, detail="Failed add product")

@app.put("/edit-product/")
async def edit_product_by_id(product:Product, session:SessionDep):
    product_statement = select(Product).where(Product.id == product.id)
    product_exist = session.exec(product_statement).one()
    if not product_exist:
        raise  HTTPException(status_code=400, detail="Product not found")
    product_exist.name = product.name
    try:
        session.add(product_exist)
        session.commit()
        session.refresh(product_exist)
        return product_exist
    except Exception as error:
        raise HTTPException(status_code=400, detail="Failed edit product, {error}")

    
@app.get("/certificate/")
async def get_all_certificate(session:SessionDep):
    statement = select(Certificate)
    result = session.exec(statement).all()
    return result

@app.get("/certificate/{id}")
async def get_certificate_by_id(id,session:SessionDep):
    statement = select(Certificate).where(Certificate.id == id)
    result = session.exec(statement).first()
    return result

@app.post("/add-certificate/")
async def add_certificate(cert: Certificate, session:SessionDep):
    statement  = select(Certificate).where(Certificate.id == cert.id)
    existing_cert = session.exec(statement).first()
    if existing_cert:
        raise HTTPException(status_code=400, detail="Certificate already registered")
    try:
        session.add(cert)
        session.commit()
        session.refresh(cert)
        return cert
    except:
        raise HTTPException(status_code=400, detail="Failed add cert")