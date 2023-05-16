from __future__ import annotations
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import pandas as pd
from telepathy import TelepathyPandas


# https://github.com/zeno-ml/zeno/blob/main/zeno/server.py#L52
def custom_generate_unique_id(route: APIRoute):
    return route.name


app = FastAPI(
    title="Telepathy Server", generate_unique_id_function=custom_generate_unique_id
)
telepathy = TelepathyPandas(image_dir="./data/imagewoof/val", limit=100)


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


class QueryRequest(CamelModel):
    text: str


class QueryResponse(CamelModel):
    x: list[float]
    y: list[float]
    score: list[float]
    image_path: list[str]


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    assert telepathy
    output = telepathy(req.text)
    return QueryResponse(
        x=output["x"].tolist(),
        y=output["y"].tolist(),
        score=output["score"].tolist(),
        image_path=output["image_path"].tolist(),
    )


def main(host="localhost", port=8000):
    disable_cors(app)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
