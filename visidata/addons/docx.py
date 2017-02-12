from visidata import *

def open_docx(p):
    import docx
    document = docx.Document(p.resolve())
    return open_pyobj(p.name, document)
#    return TextSheet(document)
