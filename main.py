from utilities.file_reader import read_trans_table, read_txt_file
from scanner import Scanner
from parser import Parser

def main():
    # Reading program
    table = read_trans_table()
    program_file = read_txt_file()
    
    # Scanner Logic
    scanner = Scanner()
    scanner.scan_file(program_file, table)
    i = scanner.get_ids()
    n = scanner.get_nums()
    t = scanner.get_tokens()

    # print('Identifiers')
    # for x in range(len(i)):
    #     print(x, '|', i[x])
    print('\n', 'Numbers')
    for x in range(len(n)):
        print(x, '|', n[x])    
    # print('\n', 'Tokens')
    # for x in t:
    #     print(x)


    # Parser Logic
    parser = Parser(i, n, t)
    parser.declaration_list()
    if(parser.get_current_token() == "$"):
        print("THE PROGRAM HAS NO SYNTAX ERRORS")


if __name__ == '__main__':
    main()