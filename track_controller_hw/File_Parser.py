class File_Parser():
    def __init__(self, path: str):
        self._path = path
        self._char_mapping = {
            'THEN': '=', 'FED': 'F', '!FED': 'f',
            'ABC': 'A', '!ABC': 'a', 'ZYX': 'Z', '!ZYX': 'z',
            'D13': 'D', '!D13': 'd', 'F28': 'E', '!F28': 'e',
            'and': '1', 'or': '0', 'A1': 'B', '!A1': 'b',
            'C12': 'C', '!C12': 'c', 'Z150': 'Y', '!Z150': 'y',
            'G29': 'G', '!G29': 'g'}

    def get_values(self):
        return self._char_mapping

    def get_path(self) -> str:
        return self._path

    def set_path(self, path):
        self._path = path

    def parse(self) -> str:
        f = open(self.get_path(), "r")

        string_to_send = ""

        # loop through each line of code
        for line in f:
            # split the line into words
            words = line.split()
            if line.isspace():
                string_to_send += " "
            elif words[0] == "D13":
                string_to_send += "D"
            elif words[0] == "F28":
                string_to_send += "E"
            elif words[0] == "#":
                continue
            elif words[0] == "BLO":
                if words[1] == "NOT":
                    if words[2] == "FED":
                        string_to_send += "f"
                    elif words[2] == "ABC":
                        string_to_send += "a"
                    elif words[2] == "ZYX":
                        string_to_send += "z"
                    else:
                        raise ValueError("Incorrect File Format: Word[2]")
                elif words[1] == "FED":
                    string_to_send += "F"
                elif words[1] == "ABC":
                    string_to_send += "A"
                elif words[1] == "ZYX":
                    string_to_send += "Z"
                else:
                    raise ValueError("Incorrect File Format: Word[1]")
            elif words[0] == "OPP":
                if words[1] == "AND":
                    string_to_send += "1"
                elif words[1] == "OR":
                    string_to_send += "0"
            else:
                raise ValueError("Incorrect File Format: Word[0]")
        """
            elif words[0] != "IF":
                print("Incorrect File Format")
                raise ValueError("Incorrect File Format")
            else:
                # loop through each word in the line
                for word in words[1:]:  # Start from index 1 to skip the first word
                    if word not in self.get_values():
                        print("Incorrect Values in File")
                        break
                    string_to_send += self.get_values()[word]
                string_to_send += " "
        """

        f.close()
        return string_to_send


if __name__ == "__main__":
    jes = File_Parser('PLC1.txt')

    hello = jes.parse()

    print(hello)
