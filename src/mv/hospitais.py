from mv.database import cache_or_execute_sqlfile


def listar(cd_multi_empresa, nocache: bool = False):
    return cache_or_execute_sqlfile(filename = "view_multi_empresa", nocache = nocache)
