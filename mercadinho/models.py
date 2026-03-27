
from typing import Optional
from sqlmodel import SQLModel, Field


class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    preco: float
    quantidade: int
