import csv

def read_trans_table():
    table = []
    with open('tabla_transicion.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table.append(row)
        return table

def read_txt_file():
    symbol_list = []
    with open('program.txt') as text_file:
        lines = text_file.read()
        symbol_list = list(lines)
    return symbol_list
