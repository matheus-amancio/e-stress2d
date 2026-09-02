import os

import marimo
from fastapi import FastAPI

# Resolve o caminho absoluto relativo a este arquivo (api.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_dir, "app.py")

server = marimo.create_asgi_app().with_app(path="", root=app_path)

app = FastAPI()
app.mount("/", server.build())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
