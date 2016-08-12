'''
http://docs.quantifiedcode.com/python-anti-patterns/correctness/implementing_java-style_getters_and_setters.html
'''
class Square(object):
    def __init__(self, length):
        self._length = length

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @length.deleter
    def length(self):
        del self._length

r = Square(5)
r.length  # automatically calls getter
r.length = 6  # automatically calls setter