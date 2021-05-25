from utilities.file_reader import read_trans_table, read_txt_file
from scanner import Scanner

def main():
    table = read_trans_table()
    program_file = read_txt_file()
    scanner = Scanner()
    scanner.scan_file(program_file, table)
    i = scanner.get_ids()
    n = scanner.get_nums()
    t = scanner.get_tokens()

    print('Identifiers')
    for x in range(len(i)):
        print(x, '|', i[x])
    print('\n', 'Numbers')
    for x in range(len(n)):
        print(x, '|', n[x])    
    print('\n', 'Tokens')
    for x in t:
        print(x)

if __name__ == '__main__':
    main()