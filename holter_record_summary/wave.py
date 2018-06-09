class Wave:
    def __init__(self, _type, onset, offset, tags=None):
        self.type = _type
        self.onset = int(onset)
        self.offset = int(offset)
        self.tags = tags

    def __str__(self):
        return 'Wave of type {} with onset {} and offset {}, tagged : {}'.format(self.type, self.onset, self.offset,
                                                                                 self.tags)