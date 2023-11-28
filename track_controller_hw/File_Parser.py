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

        string_to_send = ""
        """
        # loop through each line of code
        for line in f:
            # split the line into words
            words = line.split()
            if words[0] == "#":
                continue
            elif words[0] != "IF":
                print("Incorrect File Format")

            else:
                # loop through each word in the line
                for word_index, word in enumerate(words):
                    if word == "THEN":
                        continue
                    if word

        """
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
