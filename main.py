from fastapi import FastAPI, requests
import uvicorn
from classes.controllers import ProdutoController, AccessController

app = FastAPI()

access_controller = AccessController()
produto_controller = ProdutoController()

from rotas import *

if __name__ == '__main__':
    uvicorn.run(app)