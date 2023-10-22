class File_Parser(object):
    def __init__(self, path: str):
        self._conditions = []
        self._output = []
        self._path = path

    def get_conditions(self) -> list:
        return self._conditions

    def get_output(self) -> list:
        return self._output

    def parse(self, path: str):
        f = open(path, "r")

        for line in f:
            print(line)

        f.close()



