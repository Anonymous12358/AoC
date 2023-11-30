import bitstring
import operator
from functools import reduce


class Packet:
    OPERATIONS = [operator.add,
                  operator.mul,
                  min,
                  max,
                  None,
                  operator.gt,
                  operator.lt,
                  operator.eq,
                  ]
    OP_NAMES = "+*mMl><="

    def __init__(self, version, type_id, number, subs):
        self.version = version
        self.type_id = type_id
        self.number = number
        self.subs = subs

    def get_value(self):
        if self.type_id == 4:
            return self.number
        else:
            return reduce(Packet.OPERATIONS[self.type_id], map(Packet.get_value, self.subs))

    def __repr__(self):
        if self.type_id == 4:
            return f"{self.number}"
        else:
            return f"{Packet.OP_NAMES[self.type_id]} {self.subs}"

    @staticmethod
    def from_bitstream(bits):
        version = bits.read('uint:3')
        type_id = bits.read('uint:3')
        number, subs = 0, []
        if type_id == 4:
            while bits.read('bool:1'):
                number = (number << 4) + bits.read('uint:4')
            number = (number << 4) + bits.read('uint:4')
        else:
            length_id = bits.read('uint:1')
            if length_id == 0:
                subs_end = bits.read('uint:15') + bits.pos
                while bits.pos < subs_end:
                    subs.append(Packet.from_bitstream(bits))
            else:
                for _ in range(bits.read('uint:11')):
                    subs.append(Packet.from_bitstream(bits))

        return Packet(version, type_id, number, subs)


def parse_inp(raw_inp):
    return bitstring.ConstBitStream(hex=raw_inp)


def sum_version(packet):
    return packet.version + sum(map(sum_version, packet.subs))


def part_a(raw_inp):
    packet = Packet.from_bitstream(parse_inp(raw_inp))
    return sum_version(packet)


def part_b(raw_inp):
    packet = Packet.from_bitstream(parse_inp(raw_inp))
    return packet.get_value()
