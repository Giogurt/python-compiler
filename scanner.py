import re

def try_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Scanner:    

    def __init__(self):
        self.ids_table = []
        self.nums_table = []
        self.state = 0
        self.temp_string = ''
        self.temp_del = ''
        self.temp_num = ''

    def get_ids(self):
        return self.ids_table
    def get_nums(self):
        return self.nums_table

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
        if(re.search('\S', symbol)):
            if(re.search('\+|\-|\*|\/|<|=|>|\,|;|\(|\)|\[|\]|\{|\}|\!', symbol)):
                if(re.search('<|=|>|\!', symbol)):
                    self.temp_del += symbol
            else:
                if(self.state < 45):
                    if(re.search('[0-9]', symbol)):
                        self.temp_num += symbol
                    else:
                        self.temp_string += symbol

    def scan_file(self, chars, T):
        for symbol in chars:
            # print('state', self.state)
            # print('symbol', symbol)

            if(T[self.state]['e'] != 'E' and T[self.state]['e'] != 'A'):
                self.append_char(symbol)
                # if(try_int(T[self.state][symbol])):
                ts = symbol
                if(re.search('e|l|s|i|f|n|t|r|t|u|v|o|d|w|h|p|\+|\-|\*|\/|<|=|>|\;|\(|\)|\[|\]|\{|\}|\!', symbol)):
                    ts = symbol
                    # print('entre a normal')
                else:
                    if(re.search('\,', symbol)):
                        ts = 'comma'
                        # print('entre a coma')
                    elif(re.search('\d', symbol)):
                        ts = 'digit'
                    elif(re.search('\s', symbol)):
                        ts = 'white_character'
                    elif(re.search('[a-zA-Z]', symbol)):
                        # print('entre a letras')
                        ts = 'letter'
                    else:
                        ts = 'rare_character'
                # print('voy al', T[self.state][ts])
                self.state = int(T[self.state][ts])
                # else:
                # self.state=T[self.state][symbol]

            if(T[self.state]['e'] == 'A'):
                # print('entre a aceptar')
                if (self.temp_string != ''):
                    self.ids_table.append(self.temp_string)
                    self.temp_string = ''
                if (self.temp_num != ''):
                    self.nums_table.append(self.temp_num)
                    self.temp_num = ''
                self.temp_del = ''

                self.append_char(symbol)

                self.state = 0
            # ERROR WAS DETECTED
            elif(T[self.state]['e'] == 'E'):
                msg = self.error_handler(self.state)
                print(msg)
                exit()

            # if(re.search('\S', symbol)):
            #     if(re.search('\+|\-|\*|\/|<|=|>|\,|\(|\)|\[|\]|\{|\}|\!', symbol)):
            #         if(re.search('<|=|>|\!', symbol)):
            #             self.temp_del += symbol
            #     else:
            #         if(self.state < 45):
            #             self.temp_string += symbol
        # if(T[self.state]['e'] != 'E' and T[self.state]['e'] != 'A'):
        if(self.state != 0):
            # print(self.state)
            self.error_handler_end(self.state)
        # else:
            # msg = self.error_handler(77)
            # print(msg)
            # exit()
            # print('entre al final')
            # if (self.temp_string != ''):
            #     self.ids_table.append(self.temp_string)
            # if (self.temp_num != ''):
            #     self.nums_table.append(self.temp_num)
        # print(self.ids_table)
        # print(self.nums_table)
