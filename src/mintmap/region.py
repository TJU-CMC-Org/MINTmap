# region.py


class Region():

    def __init__(self, opts={}):
        range_list = opts.pop('range', [])
        self.__dict__ = opts
        # convert to zero indexed
        self.start = range_list[0] + self.molecule.padding_size - 1
        # inclusive, convert to zero indexed
        self.end = range_list[1] + self.molecule.padding_size - 1
        self.range = range(self.start, self.end + 1)
        self.left_range = range(0, self.start)
        self.right_range = range(
            self.end + 1,
            self.molecule.padded_sequence_length
        )

    def __repr__(self):
        return str({**self.__dict__, 'molecule': {'name': self.molecule.name}})

    def overflow_left(self, start, end):
        return start in self.left_range and end in self.range

    def on_start(self, start, end):
        return start == self.start

    def inside(self, start, end):
        return start in self.range and end in self.range

    def on_end(self, start, end):
        return end == self.end

    def overflow_right(self, start, end):
        return start in self.range and end in self.right_range
