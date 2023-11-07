class File_Parser():
    def __init__(self, path: str):
        self._operations = []
        self._operations_number = []
        self._block_number = []
        self._block_occupancy = []
        self._path = path

    def get_operations(self) -> list:
        return self._operations

    def get_operations_number(self) -> list:
        return self._operations_number

    def get_block_number(self) -> list:
        return self._block_number

    def get_block_occupancy(self) -> list:
        return self._block_occupancy

    def get_path(self) -> str:
        return self._path

    def parse(self) -> bool:
        f = open(self.get_path(), "r")
        i = 0
        for line in f:
            i += 1
            print("More" + str(i))
            words = line.split()
            print(words)
            if words[0] != 'IF':
                print("Incorrect PLC Format - IF")
                return False
            self._block_occupancy.append(words[1])
            self._block_number.append(words[2])
            if words[3] != 'THEN':
                print("Incorrect PLC Format - THEN")
                return False
            self._operations.append(words[4])
            self._operations_number.append(words[5])

        f.close()
        return True

"""
jes = File_Parser('traPLCFile.txt')

jes.parse()
print(jes.get_block_occupancy())
print(jes.get_block_number())
print(jes.get_operations())
print(jes.get_operations_number())
"""
