import uvicorn
import os
from fastapi import FastAPI, Depends, Response, status
from fastapi.openapi.utils import get_openapi
import mv_database as mv

app = FastAPI()


@app.get("/hospitais", 
         summary="Dados dos hospitais",
         tags=["Hospital"])
def get_hospitais():
    results = mv.cache_or_sql("hospitais", "SELECT CD_MULTI_EMPRESA, DS_MULTI_EMPRESA, CD_CGC, CD_UF FROM MULTI_EMPRESAS WHERE CD_ATIVO = 1", timeout = 600)
    return {
            "code": 200,
            "message": "success",
            "empresas": results
    }


@app.get("/hospitais/{id}/unidades", 
         summary="Unidades de internação do hopsital",
         tags=["Hospital"])
def get_unidades_internacao(id: int):
    sql_query = mv.read_sql("/api/sql/unidades_hospitalares.sql")
    results = mv.cache_or_sql(f"hosp.{id}.unidades", 
                              sql_query.format(cd_multi_empresa = id), 
                              timeout = 600)
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


@app.get("/internacao/sinais_vitais", 
         summary="Sinais vitais dos pacientes internados",
         tags=["Internações"])
def get_unidades_internacao():
    results = mv.sql_file("/api/sql/sinais_vitais.sql")
    return {
            "code": 200,
            "message": "success",
            "data": results
    }



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="HDT API",
        version="0.1 beta",
        description="MV API by Herson Melo",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    print("="*3, "API Core v0.1", "="*60)
#     print("ORACLE_HOME:", os.environ.get('ORACLE_HOME'))
#     print("LD_LIBRARY_PATH:", os.environ.get('LD_LIBRARY_PATH'))
    
#     ORACLE_HOME = os.environ.get('ORACLE_HOME')
#     USERNAME = os.environ.get('ORACLE_USERNAME')
#     PASSWORD = os.environ.get('ORACLE_PASSWORD')
#     SERVER = os.environ.get('ORACLE_SERVER')
#     DATABASE = os.environ.get('ORACLE_DATABASE')
#     print("Parameters:", f"User: {USERNAME}, Pass: {PASSWORD}, Host: {SERVER}, Database: {DATABASE}")
#     connection = mv.connect()
    
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")