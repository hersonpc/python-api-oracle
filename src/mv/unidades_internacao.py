from mv.database import cache_or_sql, read_internal_file


def listar(cd_multi_empresa: int, nocache: bool = False):
    sql_query = read_internal_file("view_unid_int").format(cd_multi_empresa = cd_multi_empresa)
    results = cache_or_sql(key = f"hosp.{id}.unidades", 
                           sql_query = sql_query,
                           nocache = nocache)
    return results
