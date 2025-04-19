import sqlalchemy.dialects.postgresql as pg 
from sqlmodel import SQLModel, Field, Column
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

class ProductBase(SQLModel):
    name:str | None = Field(default=str,nullable=True)
    description:str | None = Field(default=str,nullable=True)
    specification: List[dict] | None = Field(default=List[dict],sa_column=Column(pg.JSONB, nullable=True))
    productInfo: List[dict] | None = Field(default=List[dict],sa_column=Column(pg.JSONB, nullable=True))
    highlightImageURL:str | None = Field(default=str,nullable=True)
    bigImageURL:str| None = Field(default=str,nullable=True)
    smallImageURL:str| None = Field(default=str,nullable=True)
    userManualFileURL:str| None = Field(default=str,nullable=True)
    catalogueFileURL:str| None = Field(default=str,nullable=True)
    quicksheetFileURL:str| None = Field(default=str,nullable=True)
    userManualCoverImageURL:str| None = Field(default=str,nullable=True)
    catalogueCoverImageURL:str| None = Field(default=str,nullable=True)
    quicksheetCoverImageURL:str| None = Field(default=str,nullable=True)
    order:int|None = Field(default=0)

class Product(ProductBase, table = True):
    __tablename__ = "product"
    id: UUID = Field(default_factory=uuid4, primary_key=True,nullable=False)
    productCode: str | None = Field(default=str,nullable=False,unique=True)
    created_at: datetime = Field(default_factory=lambda:datetime.now())
    updated_at: datetime = Field(default_factory=lambda:datetime.now(),sa_column_kwargs={"onupdate": lambda: datetime.now()})
    
class ProductCreate(ProductBase):
    pass

class DocumentBase(SQLModel):
    filename:str | None = Field(default=str,nullable=True)
    path:str | None = Field(default=str,nullable=True)
    thumbnailImage:str | None = Field(default=str,nullable=True)
    type:str | None = Field(default=str,nullable=True)

class Document(DocumentBase, table = True):
    id: UUID = Field(default_factory=uuid4, primary_key=True,nullable=False)
    productId: UUID | None = Field(default=None, foreign_key="product.id")
    created_at: datetime = Field(default_factory=lambda:datetime.now())
    updated_at: datetime = Field(default_factory=lambda:datetime.now(),sa_column_kwargs={"onupdate": lambda: datetime.now()})

class DocumentCreate(DocumentBase):
    pass

class CertificateBase(SQLModel):
    filename:str | None = Field(default=str,nullable=True)
    path:str | None = Field(default=str,nullable=True)
    thumbnailImage:str | None = Field(default=str,nullable=True)

class Certificate(CertificateBase, table = True):
    id: UUID = Field(default_factory=uuid4, primary_key=True,nullable=False)
    created_at: datetime = Field(default_factory=lambda:datetime.now())
    updated_at: datetime = Field(default_factory=lambda:datetime.now(),sa_column_kwargs={"onupdate": lambda: datetime.now()})

class CertificateCreate(CertificateBase):
    pass

class ReceivedEmailBased(SQLModel):
    email:str | None = Field(default=str,nullable=False,)
    message:str | None = Field(default=str,nullable=True,)
    name:str | None = Field(default=str,nullable=True,)

class ReceivedEmail(ReceivedEmailBased, table = True):
    id: UUID = Field(default_factory=uuid4, primary_key=True,nullable=False)
    created_at: datetime = Field(default_factory=lambda:datetime.now())
    updated_at: datetime = Field(default_factory=lambda:datetime.now(),sa_column_kwargs={"onupdate": lambda: datetime.now()})

class ReceivedEmailCreate(ReceivedEmailBased):
    pass