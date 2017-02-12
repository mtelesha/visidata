
from visidata import *


def open_dbf(p):
    vs = Sheet(p.name, p)
    vs.loader = lambda vs=vs: load_dbf(vs)
    return vs


@async
def load_dbf(vs):
    import dbfread
    tbl = dbfread.DBF(vs.source.resolve())
    vs.columns = [ColumnItem(colname, colname) for colname in tbl.field_names]
    for record in tbl:
        vs.rows.append(record)
