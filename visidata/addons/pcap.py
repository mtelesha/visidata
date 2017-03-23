from visidata import *

def open_pcap(path):
#    import pyshark
#    vs = PcapSheet(path.name, pyshark.FileCapture(path.resolve()))
    vs = PcapSheet(path.name, path)
    return vs


class PcapSheet(Sheet):
    def reload(self):
        import pyshark
        self.cap = pyshark.FileCapture(self.source.resolve())
        self.columns = [Column('packet')]
        self.command('^J', 'vd.push(PcapPacket("n", cursorRow))', 'dive into this packet')
        self.rows = [x for x in self.cap]

class PcapPacket(SheetObject):
    pass
#    def reload(self):
#        self.columns = [Column('packet')]
#        self.rows = [x for x in self.cap]

