import re
def multiline_comment_remove(buffer1):
    #MULTILINE_COMM=r"\b/\*.+?\*/\b"
    #MULTILINE_COMM=r"\b/\*(.|\n)+?\*/\b"
    #MULTILINE_COMM=r"\s*/\*(.|\n)+?\*/\s*"
    #MULTILINE_COMM=r"(\b/\*(.|\n)+?\*/\b)|(\s*/\*(.|\n)+?\*/\s*)"
    MULTILINE_COMM=r"(\b/\*(.|\n)+?\*/\b)|(\n\t*?/\*(.|\n)+?\*/\t*\n)|(\t*/\*(.|\n)+?\*/\t*)| (//[^\r\n]*)"

    # x = re.search(MULTILINE_COMM, buffer1)
    # print(x)

    #Find all comments in buffer
    y = re.finditer(MULTILINE_COMM, buffer1)
    for i in y:
        buffer1 = buffer1.replace(i.group(), '')
        #Replace comments with whitespace

    return buffer1

def print_symbol_table(symbol_table):
    for symbol in symbol_table:
        print("{}\t {}".format(symbol[0],symbol[1]))

def add_to_symbol_table(i,col,k,type_found,token):
    symbol_table.append((token,"Line {} cols {}-{} is {}".format(i+1,col+1,k,type_found)))
    return True
def id_type_finder(token):
    KEYWORDS=r"^boolean$|^break$|^continue$|^class$|^else$|^extends$|^float$|^for$|^if$|^int$|^new$|^null$|^private$|^public$|^return$|^static$|^super|^this$|^void$|^while$"
    BOOL_CONST=r"^true$|^false$"
    if(re.search(KEYWORDS,token)):
        return "T_{}".format(token.capitalize())
    elif(re.search(BOOL_CONST,token)):
        return "T_BoolConstant"
    else: 
        return "T_Identifier"

KEYWORDS=["boolean", "break", "continue", "class", "else", "extends",
"false", "float", "for", "if", "int", "new",
"null", "private", "public", "return", "static", "super",
"this", "true", "void", "while"]
# operators=["{", "}", "[", "]", ",", ";", "(", ")", "=", "-", "!", "+", "*", "/", "<<", ">>", "<", ">",
#  "%",  "<=",  ">=",  "==",  "!=",  "&&",  "||",  "."]
OPERATORS_SC=["{", "}", "[", "]", ",", ".", ";", "(", ")", "=", "-", "!", "+", "*", "/", "<", ">","%"]
OPERATORS_DC=["<<", ">>","<=",  ">=",  "==",  "!=",  "&&",  "||"]
OPERATORS=r"^\{$|^\}$|^\[$|^\]$|^\,$|^\.$|^\;$|^\($|^\)$|^\=$|^\-$|^\!$|^\+$|^\*$|^\/$|^\<$|^\>$|^\%$|^\<\<$|^\>\>$|^\<\=$|^\>\=$|^\=\=$|^\!\=$|^\&\&$|^\|\|$"
# BEG_COMMENT="[/][*]"
# END_COMMENT="[*][/]"
# MULTILINE_COMM="^/*(.*?)\*/$"
# SINGLE_COMMENT="//[^\r\n]*"
IDENTIFIER=r"^[A-Za-z_][A-Za-z0-9_]*$"
DEC=r"^[0-9]+$"
HEX=r"0[xX][0-9A-Fa-f]"

WHITESPACE="[\s]"

symbol_table=[]





# buffer1=[]
# buffer2=[]
#with open("code.txt","rb") as f:
with open("code.txt","r") as f:
    buffer1=f.read(4096)
    buffer2=f.read(4096)
# print(buffer1)
# print(buffer2)
buffer1=multiline_comment_remove(buffer1)

col=0#Keep track of column value

lines=re.split(r"\n",buffer1)# Splits into lines
for i in range(len(lines)):
    match=False
    k=1
    col=0
    # for k in range(1,len(lines[i])):
    while(k<=len(lines[i])):#While loop because sometimes I need to decrement the cursor to find operators

        #Searches with regexp for possible tokens, obj null if search unsuccessful
        id=re.search(IDENTIFIER,lines[i][col:k])
        dec=re.search(DEC,lines[i][col:k])
        hex=re.search(HEX,lines[i][col:k])
        operators=re.search(OPERATORS,lines[i][col:k])

        #If token is found
        if (id or dec or hex or operators):
            match=True
            if id: type_found="T_Identifier"
            elif dec: type_found="T_IntegerConstant"
            elif hex: type_found="T_IntegerConstant"
            elif operators: type_found=operators.group()
            
            if(k==len(lines[i])): 
                add_to_symbol_table(i,col,k,type_found,lines[i][col:k])
                #If end of line

            #Set type found to longest found token
        elif (match):
            #End of longest token found
            match=False
            if type_found=="T_Identifier":
                type_found=id_type_finder(lines[i][col:k-1])
            #Check for keywords    
            add_to_symbol_table(i,col,k,type_found,lines[i][col:k-1])
            #Add to symbol table
            if(re.search(OPERATORS,lines[i][k-1:k])or re.search(OPERATORS,type_found)):k-=1
            #If operator is next char or last char found, decrement. Just so we dont miss any chars
            col=k
        else: 
            #If whitespace, continue
            col=k
        k+=1

print_symbol_table(symbol_table)


        
    






#buffer_split=re.split("[\n]",buffer1)


#for i in range(len(buffer_split)):

    #if(x=re.search(IDENTIFIER,buffer1))









