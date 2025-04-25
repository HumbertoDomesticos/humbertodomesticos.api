from main import app, access_controller

@app.get('/is-connected')
def is_connected():
    return {"dado": access_controller.teste_query()}