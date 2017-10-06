import collections
from PEManager import *


class Chunk(object):

    def __init__(self, pe_manager, size=0x1000):
        """
        creator of memory chunk that be allocated.

        Args:
            pe_manager(PEManager) : target PEManager to append chunk.
            size(int) : size of chunk.
        """
        if not isinstance(pe_manager, PEManager):
            raise TypeError('data should be of type: PEManager')
        data = bytearray(size)
        section = pe_manager.create_new_data_section(data, ".zigzi1")
        self.pe_manager = pe_manager
        self.rva = section.virtual_address
        self.section_va = pe_manager.get_abs_va_from_rva(self.rva)
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        if type(i) is slice:
            start = i.start + self.rva
            size = i.stop - i.start
            step = i.step
            if step is not None:
                print("NOT SUPPORTED STEP")
                exit()
        else:
            start = self.rva + i
            size = 1

        if start >= self.size + self.rva\
                or start < self.rva:
            raise IndexError(
                "Indexing is out of range Min:0 ~ Max:{} but argument:{}"
                    .format(self.size, start - self.rva)
            )
        if size >= self.size + self.rva \
                or start < self.rva:
            raise IndexError(
                "Indexing is out of range Min:0 ~ Max:{} but argument:{}"
                    .format(self.size, start - self.rva)
            )

        return self.pe_manager.get_data_from_rva(start, size)

    def __delitem__(self, i):
        pass

    def __setitem__(self, i, v):
        if type(i) is slice:
            start = i.start + self.rva
            size = i.stop - i.start
            step = i.step
            if step is not None:
                print("NOT SUPPORTED STEP")
                exit()
        else:
            start = i + self.rva

        if start >= self.size + self.rva \
                or start < self.rva:
            raise IndexError(
                "Indexing is out of range Max:{} but argument:{}"
                    .format(self.size, start - self.rva)
            )
        self.pe_manager.set_bytes_at_rva(start, v)

    def get_va(self):
        return self.section_va
