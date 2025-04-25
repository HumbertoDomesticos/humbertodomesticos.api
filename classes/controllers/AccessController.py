from classes.models import Access

class AccessController:
    def __init__(self):
        self.access_obj = Access('root', '', 'localhost', '3306', 'loja_humb')

    def is_connected(self):
        return self.access_obj.is_connected()
    
    def teste_query(self):
        return self.access_obj.custom_select_query('SELECT * FROM produtos')