import pandas as pd

class block_info:
    def __init__(self, filepath: str):
        self.block_dict = self.load_block_info(filepath)

    def load_block_info(self, filepath: str):
        df = pd.read_excel(filepath)
        block_dict = {}

        for index, row in df.iterrows():
            line = row['line color'].lower()
            block_number = row['block number']

            block_info = {
                'grade': row['grade'],
                'elevation': row['elevation'],
                'length': row['length'],
                'section': row['section'],
                'speed limit': row['speed limit'],
                'switch position': bool(row['switch position']),
                'underground': bool(row['underground']),
                'beacon': row['beacon']
            }

            if line in block_dict:
                block_dict[line][block_number] = block_info
            else:
                block_dict[line] = {block_number: block_info}

        return block_dict

    def get_block_info(self, line, block_number):
        if line in self.block_dict and block_number in self.block_dict[line]:
            return self.block_dict[line][block_number]
        else:
            return None

    def get_all_blocks_for_line(self, line):
        return self.block_dict.get(line, {})



# How to Use:
# tm = block_info('block_information.xlsx')
# red_48 = tm.get_block_info('red', 48)['grade']
# print(red_48)