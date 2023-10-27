import pandas as pd


xl = 'block_information.xlsx'
df = pd.read_excel(xl)
block_dict = {}
for index, row in df.iterrows():
    line = row['line color']
    block_number = row['block number']

    block_info = {
        'grade' : row['grade'],
        'elevation' : row['elevation'],
        'length' : row['length'],
        'section' : row['section'],
        'speed limit' : row['speed limit'],
        'elevation' : row['elevation'],
        'switch position' : bool(row['switch position']),
        'underground' : bool(row['underground']),
        'beacon' : row['beacon']
    }

    if line in block_dict:
        block_dict[line][block_number] = block_info
    else:
        block_dict[line] = {block_number: block_info}


blue_line = block_dict['Blue']
red_line = block_dict['Red']
print(red_line[48])