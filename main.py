from utilities.file_reader import read_trans_table, read_txt_file
from scanner import Scanner

def main():
    table = read_trans_table()
    program_file = read_txt_file()
    scanner = Scanner()
    scanner.scan_file(program_file, table)
    

if __name__ == '__main__':
    main()