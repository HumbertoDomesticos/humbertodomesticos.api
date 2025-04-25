from main import app, requests

@app.get('/teste/{valor}')
def teste(valor):
    return {"valor:":valor}

@app.get('/teste-2')
def teste_2(id:int = 0):
    return {'id':id}