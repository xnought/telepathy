from __future__ import annotations
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import pandas as pd


# https://github.com/zeno-ml/zeno/blob/main/zeno/server.py#L52
def custom_generate_unique_id(route: APIRoute):
    return route.name


app = FastAPI(
    title="Telepathy Server", generate_unique_id_function=custom_generate_unique_id
)


# https://github.com/zeno-ml/zeno
def to_camel(string):
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


# https://github.com/zeno-ml/zeno
class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


def disable_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class TestResponse(CamelModel):
    test: str


@app.get("/test", response_model=TestResponse)
def test():
    return TestResponse(test="test")


def main(host="localhost", port=8000):
    disable_cors(app)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
