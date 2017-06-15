from py4j.java_gateway import JavaGateway


class MaltRunner:
    def __init__(self):
        self.gateway = JavaGateway()
        self._new_array = self.gateway.new_array
        self._JString = self.gateway.jvm.java.lang.String

    def _init_array(self, tokens):
        arr = self._new_array(self._JString, len(tokens))
        arr[:] = tokens
        return arr

    def parse_strings(self, tokens):
        return str(self.gateway.entry_point.parse_one(self._init_array(tokens)))

    def parse_many(self, sentences):
        return map(str, self.gateway.entry_point.parseMany(self._init_array(sentences)))