class Parser:
    def __init__(self, ids, nums, tokens):
        self.ids = ids
        self.nums = nums
        self.tokens = tokens
        self.current_token = tokens[0]
        self.token_value = ""
        self.token_pos = 0
        self.res_list = ["err", "else", "if", "int", "return",
                         "void", "while", "input", "output"]
        self.del_list = [
            "+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!=", "=", ";", ",", "(", ")", "[", "]", "{", "}"
        ]
        self.tokens.append(["del", "$"])

    def get_current_token(self):
        return self.current_token

    def error(self):
        print("IMPLEMENTAR ERROR BIEN")
        exit()

    def get_token_value(self):
        value = ""
        if (self.current_token[0] == "res"):
            value = self.res_list[self.current_token[1]]
        elif (self.current_token[0] == "del"):
            value = self.del_list[self.current_token[1]]
        elif (self.current_token[0] == "id"):
            value = self.ids[self.current_token[1]]
        elif (self.current_token[0] == "nums"):
            value = self.nums[self.current_token[1]]
        else:
            print("UNRECOGNIZED TOKEN TYPE")
            exit()
        return value

    def match(self, terminal):
        if (self.token_value == terminal):
            self.token_pos += 1
            self.current_token = self.tokens[0]
            self.token_value = self.get_token_value()
        else:
            self.error()

    def match_id(self):
        if (self.current_token[0] == "id"):
            self.token_pos += 1
            self.current_token = self.tokens[0]
            self.token_value = self.get_token_value()
        else:
            self.error()
    def match_num(self):
        if (self.current_token[0] == "num"):
            self.token_pos += 1
            self.current_token = self.tokens[0]
            self.token_value = self.get_token_value()
        else:
            self.error()

    def check_id(self):
        if (self.current_token[0] == "id"):
            return True
        else:
            return False

    def check_num(self):
        if (self.current_token[0] == "num"):
            return True
        else:
            return False
            
    def declaration_list(self):
        self.token_value = self.get_token_value()
        self.declaration()
        self.declaration_list_prime()

    def declaration_list_prime(self):
        if (self.token_value == "int" or self.token_value == "void"):
            self.declaration()
            self.declaration_list_prime()
        elif(self.token_value == "$"):
            return
        else:
            self.error()

    def declaration(self):
        if (self.token_value == "int"):
            self.var_declaration()
        elif (self.token_value == "void"):
            self.fun_declaration()
        else:
            self.error()
    
    def var_declaration(self):
        self.match("int")
        self.match_id()
        if (self.token_value == "("):
            self.fun_declaration()
            return
        self.var_declaration_prime()
    
    def var_declaration_prime(self):
        if (self.token_value == ";"):
            self.match(";")
        elif (self.token_value == "["):
            self.match("[")
            self.match_num()
            self.match("]")
            self.match(";")
        else:
            self.error()
    
    def fun_declaration(self):
        if (self.token_value == "("):
            self.match("(")
            self.params()
            self.match(")")
            self.compound_stmt()
        elif (self.token_value == "void"):
            self.match("void")
            self.match_id()
            self.match("(")
            self.params()
            self.match(")")
            self.compound_stmt()
        else:
            self.error()
    
    def params(self):
        if (self.token_value == "int"):
            self.param_list()
        elif (self.token_value == "void"):
            self.match("void")
        else:
            self.error()
    
    def param_list(self):
        self.param()
        self.param_list_prime()

    def param_list_prime(self):
        if (self.token_value == ","):
            self.match(",")
            self.param()
            self.param_list_prime()
        elif (self.token_value == ")"):
            return
        else:
            self.error()

    def param(self):
        self.match("int")
        self.match_id()
        self.param_prime()

    def param_prime(self):
        if (self.token_value == "["):
            self.match("[")
            self.match("]")
        elif (self.token_value == "," or self.token_value == ")"):
            return
        else:
            self.error()
    
    def compound_stmt(self):
        self.match("{")
        self.local_declarations()
        self.statement_list()
        self.match("}")
    
    def local_declarations(self):
        if (self.token_value == "int"):
            self.var_declaration()
            self.local_declarations()
        elif (self.check_id() or self.token_value == "{" or self.token_value == "if" or self.token_value == "while"
             or self.token_value == "return" or self.token_value == "input" or self.token_value == "output" ):
            return
        else:
            self.error()

    def statement_list(self):
        self.statement()
        self.statement_list_prime()
    
    def statement_list_prime(self):
        if (self.check_id() or self.token_value == "{" or self.token_value == "if" or self.token_value == "while"
             or self.token_value == "return" or self.token_value == "input" or self.token_value == "output" ):
            self.statement()
        elif (self.token_value == "}"):
            return
        else:
            self.error()
    
    def statement(self):
        if (self.check_id()):
            self.var()
            self.match("=")
            self.expression()
            self.match(";")
        elif (self.token_value == "{"):
            self.compound_stmt()
        elif (self.token_value == "if"):
            self.match("if")
            self.match("(")
            self.expression()
            self.match(")")
            self.statement()
            self.selection_stmt_else()
        elif (self.token_value == "while"):
            self.match("while")
            self.match("(")
            self.expression()
            self.match(")")
            self.statement()
        elif (self.token_value == "return"):
            self.match("return")
            self.return_stmt_prime()
        elif(self.token_value == "input"):
            self.match("input")
            self.var()
            self.match(";")
        elif(self.token_value == "output"):
            self.match("output")
            self.output_stmt_prime()
        else:
            self.error()
    
    def selection_stmt_else(self):
        if(self.token_value == "else"):
            self.match("else")
            self.statement()
        elif (self.check_id() or self.token_value == "{" or self.token_value == "if" or self.token_value == "while"
            or self.token_value == "return" or self.token_value == "input" or self.token_value == "output"
            or self.token_value == "}" or self.token_value == "else" ):
            return
        else:
            self.error()
    
    def return_stmt_prime(self):
        if self.token_value == ";":
            self.match(";")
        elif (self.token_value == "(" or self.check_id() or self.check_num()):
            self.expression()
            self.match(";")
        else:
            self.error()
    
    def output_stmt_prime(self):
        if self.check_id():
            self.var()
            self.match(";")
        elif (self.token_value == "(" or self.check_id() or self.check_num()):
            self.expression()
            self.match(";")
        else:
            self.error()
    
    def var(self):
        self.match_id()
        if(self.token_value == "("):
            #call
            self.match("(")
            self.args()
            self.match(")")
            return
        self.var_prime()

    def var_prime(self):
        if(self.token_value == "["):
            self.match("[")
            self.arithmetic_expression()
            self.match("]")
        elif(self.token_value == "*" or self.token_value == "/" or self.token_value == "+"
            or self.token_value == "-" or self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!=" or self.token_value == ";" or self.token_value == ")"
            or self.token_value == ","):
            return
        else:
            self.error()
    
    def expression(self):
        self.arithmetic_expression()
        self.expression_prime()
    
    def expression_prime(self):
        if(self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!="):
            self.relop()
            self.arithmetic_expression()
        elif(self.token_value == ";" or self.token_value == ")"):
            return
        else:
            self.error()
    
    def relop(self):
        if(self.token_value == "<="):
            self.match("<=")
        elif(self.token_value == "<"):
            self.match("<")
        elif(self.token_value == ">"):
            self.match(">")
        elif(self.token_value == ">="):
            self.match(">=")
        elif(self.token_value == "=="):
            self.match("==")
        elif(self.token_value == "!="):
            self.match("!=")
        else:
            self.error()
    
    def arithmetic_expression(self):
        self.term()
        self.arithmetic_expression_prime()

    def arithmetic_expression_prime(self):
        if(self.token_value == "+" or self.token_value == "-"):
            self.addop()
            self.term()
            self.arithmetic_expression_prime()
        elif(self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!=" or self.token_value == ";" or self.token_value == ")"
            or self.token_value == ","):
            return
        else:
            self.error()
        
    def addop(self):
        if(self.token_value == "+"):
            self.match("+")
        elif(self.token_value == "-"):
            self.match("-")
        else:
            self.error()
    
    def term(self):
        self.factor()
        self.term_prime()
    
    def term_prime(self):
        if(self.token_value == "*" or self.token_value == "/"):
            self.mulop()
            self.factor()
            self.term_prime()
        elif(self.token_value == "+"
            or self.token_value == "-" or self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!=" or self.token_value == ";" or self.token_value == ")"
            or self.token_value == ","):
            return
        else:
            self.error()
    
    def mulop(self):
        if(self.token_value == "*"):
            self.match("*")
        elif(self.token_value == "/"):
            self.match("/")
        else:
            self.error()
    
    def factor(self):
        if(self.token_value == "("):
            self.match("(")
            self.arithmetic_expression()
            self.match(")")
        elif(self.check_id()):
            self.var()
        elif(self.check_num()):
            self.match_num()
        else:
            self.error()

    def args(self):
        if(self.token_value == "(" or self.check_id() or self.check_num()):
            self.args_list()
        elif(self.token_value == ")"):
            return
        else:
            self.error()

    def args_list(self):
        self.arithmetic_expression()
        self.args_list_prime()

    def args_list_prime(self):
        if(self.token_value == ","):
            self.match(",")
            self.arithmetic_expression()
            self.args_list_prime()
        elif(self.token_value == ")"):
            return
        else:
            self.error()         







    

