from mv.database import cache_or_sql, read_internal_file


def leituras(cd_multi_empresa: int, nocache: bool = False):
    sql_query = read_internal_file("view_sinais_vitais").format(cd_multi_empresa = cd_multi_empresa)
    results = cache_or_sql(key = f"hosp.{id}.sinais_vitais", 
                           sql_query = sql_query,
                           nocache = nocache)
    return results
