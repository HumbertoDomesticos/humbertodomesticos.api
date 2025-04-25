class Produto:
    def __init__(self,
                 id_prod:int = 0,
                 nome_prod:str = '',
                 preco_inteiro_prod:int = 0,
                 desconto_prod:int = 0):
        self.id_prod = id_prod
        self.nome_prod = nome_prod
        self.preco_inteiro_prod = preco_inteiro_prod
        self.desconto_prod = desconto_prod

        self.preco_final_prod = self.preco_inteiro_prod * (1 - (desconto_prod/100))

    def __str__(self):
        return f"ID do produto: {self.id_prod}\n\
                 Nome do produto: {self.nome_prod}\n\
                 Preço inteiro: {self.preco_inteiro_prod}\n\
                 Desconto: {self.desconto_prod}\n\
                 Preço Final: {self.preco_final_prod}"