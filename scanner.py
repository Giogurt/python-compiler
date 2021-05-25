import re

class Scanner:    

    def __init__(self):
        self.ids_table = []
        self.nums_table = []
        self.symbol_table = []
        self.token_list = []
        self.del_list = [
            "+","-","*","/","<","<=",">",">=","==","!=","=",";",",","(",")","[","]","{","}"
        ]
        self.state = 0
        self.temp_string = ''
        self.temp_del = ''
        self.temp_num = ''

    def get_ids(self):
        return self.ids_table
    def get_nums(self):
        return self.nums_table
    def get_dels(self):
        return self.del_list
    def get_tokens(self):
        return self.token_list

    def error_handler(self, err_state):
        msg = 'ERROR: '
        switcher={
            72: msg + 'INVALID CHARACTER',
            73: msg + 'COMMENT NEVER ENDS',
            74: msg + '! NEEDS TO BE FOLLOWED BY A =',
            75: msg + 'IDS CANNOT CONTAIN DIGITS',
            76: msg + 'NUMS CANNOT CONTAIN LETTERS',
            77: msg + 'REACHED END OF FILE PREMATURELY'
        }
        return switcher.get(err_state, "UNKNOWN ERROR")
    def error_handler_end(self, err_state):
        msg = 'ERROR: '
        switcher={
            53: msg + 'COMMENT NEVER ENDS',
            54: msg + 'COMMENT NEVER ENDS',
        }
        err_msg = switcher.get(err_state, 'REACHED END OF FILE PREMATURELY')
        print(err_msg)
        exit()

    def append_char(self, symbol):
        # We need to check what type of symbol we currently have to see
        # where to add it
        if(re.search('\S', symbol)):
            if(self.state < 53 or self.state > 54):
                if(re.search('\+|\-|\*|\/|<|=|>|\,|;|\(|\)|\[|\]|\{|\}|\!', symbol)):
                    if len(self.temp_del) > 0:
                        if(re.search('<|=|>|\!', symbol)):
                            self.temp_del += symbol
                        else:
                            self.temp_del = 0
                    else:
                        self.temp_del += symbol
                else:
                    # if(self.state < 45):
                        # print(len(self.temp_del))
                    if(len(self.temp_del) == 0):
                    
                        if(re.search('[0-9]', symbol)):
                            self.temp_num += symbol
                        else:
                            self.temp_string += symbol
            elif(self.state == 53):
                if(symbol == '*'):
                    self.temp_del = symbol
            else:
                if(symbol == '/'):
                    self.temp_del += symbol

    def add_string(self):
        id = ""
        sym_entry = -1
        if self.temp_string == "else":
            id = "res"
            sym_entry = 1
        elif self.temp_string == "if":
            id = "res"
            sym_entry = 2
        elif self.temp_string == "int":
            id = "res"
            sym_entry = 3
        elif self.temp_string == "return":
            id = "res"
            sym_entry = 4
        elif self.temp_string == "void":
            id = "res"
            sym_entry = 5
        elif self.temp_string == "while":
            id = "res"
            sym_entry = 6
        elif self.temp_string == "input":
            id = "res"
            sym_entry = 7
        elif self.temp_string == "output":
            id = "res"
            sym_entry = 8
        else:
            self.ids_table.append(self.temp_string)
            id = "id"
            sym_entry = len(self.ids_table) - 1
        self.token_list.append([id, sym_entry])

    def add_num(self):
        id = "num"
        self.nums_table.append(self.temp_num)
        sym_entry = len(self.nums_table) - 1
        self.token_list.append([id, sym_entry])
    
    def add_del(self):
        if(self.temp_del != '*/'):
            id = "del"
            sym_entry = -1
            for x in range(len(self.del_list)):
                if self.del_list[x] == self.temp_del:
                    sym_entry = x
                    break
            if sym_entry != -1:
                self.token_list.append([id, sym_entry])
    def scan_file(self, chars, T):
        for symbol in chars:
            delimiter_flag = False

            # Check to see if we are in a non terminal state
            if(T[self.state]['e'] != 'E' and T[self.state]['e'] != 'A'):
                self.append_char(symbol)
                ts = symbol

                # Depending on the symbol we transform it so the dictionary can recognice it
                if(re.search('e|l|s|i|f|n|t|r|t|u|v|o|d|w|h|p|\+|\-|\*|\/|<|=|>|\;|\(|\)|\[|\]|\{|\}|\!', symbol)):
                    ts = symbol
                else:
                    if(re.search('\,', symbol)):
                        ts = 'comma'
                    elif(re.search('\d', symbol)):
                        ts = 'digit'
                    elif(re.search('\s', symbol)):
                        ts = 'white_character'
                    elif(re.search('[a-zA-Z]', symbol)):
                        ts = 'letter'
                    else:
                        ts = 'rare_character'

                # Go to the next state
                self.state = int(T[self.state][ts])

            # Handle comments
            # if(self.state >= 53 and self.state <= 54):
            #     self.temp_del = ''
            # if(self.temp_del == "/"):
            #     if(symbol == "*"):
            #         self.temp_del = ''

            # Handle the accepting state
            if(T[self.state]['e'] == 'A'):
                if (self.temp_string != ''):
                    self.add_string()
                    self.temp_string = ''
                if (self.temp_num != ''):
                    self.add_num()
                    self.nums_table.append(self.temp_num)
                    self.temp_num = ''
                if (self.temp_del != ''):
                    self.add_del()
                    self.temp_del = ''
                    delimiter_flag = True

                if (delimiter_flag == False):
                    self.append_char(symbol)

                self.state = 0

            # ERROR WAS DETECTED
            elif(T[self.state]['e'] == 'E'):
                msg = self.error_handler(self.state)
                print(msg)
                exit()

        # Check the last state when the file has been read
        # to check for errors at the end
        if(self.state != 0):
            self.error_handler_end(self.state)