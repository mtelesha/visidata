
from visidata import *

option('binStride', 16, 'number of bytes on a row for .bin sheets')

def open_bin(p):
    vs = Sheet(p.name, p)
    vs.loader = lambda vs=vs: load_bin(vs)
    return vs

@async
def load_bin(vs):
    n = int(options.binStride)

    # rows will be a list of pairs: (offset, slice)
    vs.columns = [
        Column('offset',
                type=int,
                getter=lambda r: r[0],
                fmtstr='%x')
    ]

    for i in range(n):
        vs.columns.append(Column('x%02x' % i,
                                 type=int,
                                 getter=lambda r,i=i:r[1][i],
                                 fmtstr='%02X'))

    vs.columns.append(Column('bytes', width=n+1, getter=lambda r: r[1]))

    data = vs.source.read_bytes()
    vs.rows = []
    for i in range(0, len(data), n):
        vs.rows.append((i, data[i:i+n]))
