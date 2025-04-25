from main import app, produto_controller
from classes.models import Produto

@app.get('/create-produto')
def create_produto(id_prod:int = 0,
                   nome_prod:str = '',
                   preco_inteiro_prod:int = 0,
                   desconto_prod:int = 0):
    produto_controller.clear_produto()
    produto_controller.create_produto(id_prod, nome_prod, preco_inteiro_prod, desconto_prod)
    return {'produto': produto_controller.return_last_made_produto()}