from fastapi import FastAPI, requests
import uvicorn
from classes.controllers import ProdutoController, AccessController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # libera para seu frontend
    allow_credentials=True,
    allow_methods=["*"],  # permite todos os métodos HTTP
    allow_headers=["*"],  # permite todos os headers
)

access_controller = AccessController()
produto_controller = ProdutoController()

from rotas import *

if __name__ == '__main__':
    uvicorn.run(app)