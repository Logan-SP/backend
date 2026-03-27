
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware

from models import Produto
from database import create_db_and_tables, get_session

app = FastAPI(title="API Mercadinho")


# CORS — ESSA PARTE É O QUE RESOLVE TUDO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/produtos")
def criar_produto(produto: Produto, session: Session = Depends(get_session)):
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto


@app.get("/produtos")
def listar_produtos(session: Session = Depends(get_session)):
    produtos = session.exec(select(Produto)).all()
    return produtos


@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, dados: Produto, session: Session = Depends(get_session)):
    produto = session.get(Produto, produto_id)
    if not produto:
        return {"erro": "Produto não encontrado"}

    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade

    session.commit()
    session.refresh(produto)
    return produto


@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
    produto = session.get(Produto, produto_id)
    if not produto:
        return {"erro": "Produto não encontrado"}

    session.delete(produto)
    session.commit()
    return {"mensagem": "Produto deletado"}
