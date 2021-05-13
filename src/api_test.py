from os.path import normcase
import uvicorn
import os, time
from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.openapi.utils import get_openapi
import mv_database as mv
import mv.hospitais as hospitais
import mv.unidades_internacao as unidades
import mv.sinais_vitais as sinais_vitais

app = FastAPI()

core_version = "0.1.2 beta"
version = "0.0.16"


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    print("="*3, f"Request at [{time.ctime()}] v{version}", "="*3)
    response = await call_next(request)
    process_time = time.time() - start_time
    print("<"*3, f"Request completed in {process_time}s")
    response.headers["X-API-PROCESS-TIME"] = str(process_time)
    response.headers["X-API-VERSION-CORE"] = core_version
    response.headers["X-API-VERSION"] = version
    response.headers["X-API-AUTHOR"] = "Herson Melo <hersonpc@gmail.com>"
    return response


@app.get("/hospitais", 
         summary="Dados dos hospitais",
         tags=["Hospital"])
def get_hospitais(nocache: bool = False):
    results = hospitais.listar(nocache)
    return {
            "code": 200,
            "message": "success",
            "empresas": results
    }


@app.get("/hospitais/{id}/unidades", 
         summary="Unidades de internação do hopsital",
         tags=["Hospital"])
def get_unidades_internacao(id: int, nocache: bool = False):
    results = unidades.listar(cd_multi_empresa = id, nocache = nocache)
    return {
            "code": 200,
            "message": "success",
            "data": results
    }


@app.get("/internacao/atendimentos", 
         summary="Atendimentos ativos",
         tags=["Internações"])
def get_unidades_internacao():
    results = mv.sql_file("/api/sql/atendimentos_ativos.sql", timeout = 120)
    return {
            "code": 200,
            "message": "success",
            "data": results
    }


@app.get("/hospitais/{id}/internacao/sinais_vitais", 
         summary="Sinais vitais dos pacientes internados",
         tags=["Internações"])
def get_sinais_vitais(id: int, nocache: bool = False):
    results = sinais_vitais.leituras(cd_multi_empresa = id, nocache = nocache)
    return {
            "code": 200,
            "message": "success",
            "data": results
    }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title = "HDT API",
        version = core_version,
        description = f"MV API by Herson Melo v{version}",
        routes = app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    print("="*3, f"API Core v{core_version}", "="*60)
