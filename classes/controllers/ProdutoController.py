from classes.models import Produto
from classes.views import ProdutoView

class ProdutoController:
    def __init__(self):
        self.produtos = []
        self.view = ProdutoView()

    def create_produto(self, 
                       id_prod:int = 0,
                       nome_prod:str = '',
                       preco_inteiro_prod:int = 0,
                       desconto_prod:int = 0):
        self.produtos.append(Produto(id_prod, nome_prod, preco_inteiro_prod, desconto_prod))

    def clear_produto(self):
        self.produtos = []

    def return_last_made_produto(self):
        return self.produtos[-1]