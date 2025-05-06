# API para busca e criação de Agendamentos #

Para iniciar o servidor da API apenas para a máquina local, use:
```
uvicorn main:app --reload
```

Para iniciar a API para LAN, use:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

Caso não tenha o Uvicorn baixado, use:
```
pip install 'uvicorn[standard]'
```
