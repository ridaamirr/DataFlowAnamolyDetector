double_operators=['++','--','+=','-=','*=','/=']
keywords_to_ignore=['//','else','break','continue']  
only_reference_keywords=['for','if','while','return','elseif','cout']
data_types=['int','short','long','float','double','char','bool']
operators=['+','-','/','*','%'] 
char_to_ignore=['(',')','=']

defined_variables=[]
referened_variables=[]
initalized_variables=[]
for_loop_variable=[]
array_variables=[]
statements=[]

def is_essential(statement):
    tokens=statement.split()
    return tokens[0] not in keywords_to_ignore 

def convert_doubleoperators(line): 
    tokens=line.split()
    for token in tokens: 
        if '++' in token:  
            line = line.replace(token, "")
            token = token.replace('++', "")
            new_line=token+' = '+token+' + 1'  
            line=line+ ' '+new_line
        elif '--' in token:
            line = line.replace(token, "")
            token = token.replace('--', "")
            new_line=token+' = '+token+' - 1'  
            line=line+ ' '+new_line
        elif '+=' in token: 
            line = line.replace(token, "")
            token = token.replace('+=', " ")
            token2=token.split()
            new_line=token2[0]+' = '+token2[0]+' + '+token2[1]  
            line=line+new_line
        elif '-=' in token: 
            line = line.replace(token, "")
            token = token.replace('-=', " ")
            token2=token.split()
            new_line=token2[0]+' = '+token2[0]+' - '+token2[1]  
            line=line+new_line
        elif '*=' in token: 
            line = line.replace(token, "")
            token = token.replace('*=', " ")
            token2=token.split()
            new_line=token2[0]+' = '+token2[0]+' * '+token2[1]  
            line=line+new_line
        elif '/=' in token: 
            line = line.replace(token, "")
            token = token.replace('/=', " ")
            token2=token.split()
            new_line=token2[0]+' = '+token2[0]+' / '+token2[1]  
            line=line+new_line
    return line

def isNum(str):
    for i in range(len(str)):
        if str[i]>='0' and str[i]<='9':
            return True
    return False 

def removeStrings(str): 
    i=0 
    toreturn='' 
    while i!=len(str) and str[i]!='\"': 
        toreturn+=str[i] 
        i=i+1 
    i=i+1
    while i<len(str) and str[i]!='\"': 
        i=i+1 
    i=i+1
    while i<len(str):
        toreturn+=str[i] 
        i=i+1 
    return toreturn  

def removeArray(tokens):  
    toreturn=[]
    for token in tokens: 
        if '[' in token and ']' in token: 
            token=token.replace('[',' ')
            token=token.replace(']',' ')  
            tok2=token.split()      
            for tok in tok2: 
                tokens.append(tok)
    for token in tokens: 
        if '[' in token and ']' in token: 
            continue 
        else: 
            toreturn.append(token)
    return toreturn

def handlerhs(tokens,firstelement): 
    undefined=[]
    tokens=removeArray(tokens)  
    for token in tokens:             
        if  (token not in operators and token not in defined_variables and not isNum(token) and token!='==' and token!='=' and token !='!=' and token not in referened_variables and token not in for_loop_variable and token!='&&' and token!='||' and token not in data_types and token not in array_variables) or token in initalized_variables:
            if token not in undefined:
                undefined.append(token)
        elif token in defined_variables and token!=firstelement: 
            defined_variables.remove(token)
            referened_variables.append(token) 
    return undefined

fptr=open("file.txt","r")
data_read=fptr.readlines()

chars_to_remove="\n\t"

for i in range(len(data_read)):
    for char in chars_to_remove:
        data_read[i] = data_read[i].replace(char, "") 

chars_to_remove="(),><;"

for char in chars_to_remove:
    data_read[0] = data_read[0].replace(char, " ")

tokens = data_read[0].split()
tokens=tokens[3:]  

for i in range(0,len(tokens),2):  
    if '[]' in tokens[i]: 
        tokens[i]=tokens[i].replace('[]','')
    defined_variables.append(tokens[i]) 

data_read=data_read[1:]#removing function defination as it is not needed anymore   

for line in data_read:
    tokens=line.split()  
    is_essential=True 
    for token in tokens:
        if token in keywords_to_ignore:
            is_essential=False
            break
    if is_essential and line!='':
        statements.append(line) 

for statement in statements:
    undefined=[] 
    print(statement)  

    if '{' in statement or '}' in statement: 
        continue
  
    for char in chars_to_remove:
        statement = statement.replace(char, " ")
    while('\"' in statement):
        statement = removeStrings(statement) 
    statement=convert_doubleoperators(statement)

    tokens=statement.split()  

    if tokens[0] in only_reference_keywords: 
        if tokens[0] == 'for' and tokens[1] in data_types:
            for_loop_variable.append(tokens[2])  
        if tokens[0] == 'cout': 
            if 'endl' in tokens: 
                tokens.remove('endl')  
        undefined=handlerhs(tokens[1:],None)
        for var in undefined:
            print("undefined variable: ",var )
        continue

    if tokens[0] == 'cin': 
        for token in tokens[1:]:
            if token in defined_variables: 
                print('Redefination of variable: ',token) 
            elif token in referened_variables: 
                referened_variables.remove(token)
                defined_variables.append(token) 
            elif token in initalized_variables: 
                initalized_variables.remove(token)
                defined_variables.append(token)
            elif tokens[0][0] not in array_variables: 
                print('Undefined variable: ',token)
        continue
                
    if tokens[0] in data_types:  
        if '=' not in statement: 
            for token in tokens[1:]: 
                if token not in defined_variables:
                    initalized_variables.append(token)#only initalization
        else: 
            if tokens[1] in defined_variables: 
                print('Redefination of variable: ',tokens[1]) 
            else:
                defined_variables.append(tokens[1])#new defination  
                undefined=handlerhs(tokens[2:],None)
                for var in undefined:
                    print("undefined variable: ",var )
        continue     
    
    if '[' and ']' in tokens[0]: 
        temptoken=tokens[0].split('[') 
        temptoken[1]=temptoken[1].replace(']','')  
        tokens.append(temptoken[1]) 
        tokens.remove(tokens[0])
        tokens=[temptoken[0]]+tokens

    if tokens[0] in initalized_variables and tokens[1]=='=':  
        if tokens[0] in tokens[1:]: 
            print("undefined variable: ",tokens[0]) 
            continue
        initalized_variables.remove(tokens[0])
        defined_variables.append(tokens[0]) 
        undefined=handlerhs(tokens[1:],None)
        for var in undefined:
            print("undefined variable: ",var )
        continue

    if tokens[0] in defined_variables and tokens[1]=='=':  
        if tokens[0] not in tokens[1:]:
            print("redefination of variable, ",tokens[0])   
        undefined=handlerhs(tokens[2:],tokens[0])
        for var in undefined:
            print("undefined variable: ",var )
        continue 

    if tokens[0] in referened_variables and tokens[1]=='=': 
        referened_variables.remove(tokens[0])
        defined_variables.append(tokens[0])  
        undefined=handlerhs(tokens[2:],tokens[0])
        for var in undefined:
            print("undefined variable: ",var )
        continue

    if tokens[0] not in initalized_variables and tokens[1]=='=' and tokens[0] not in for_loop_variable and tokens[0][0] not in array_variables:  
        undefined=handlerhs(tokens[1:],None)
        undefined.append(tokens[0])  
        for var in undefined:
            print("undefined variable: ",var )
        continue
    
    if tokens[0] in for_loop_variable:  
        undefined=handlerhs(tokens[2:],tokens[0])
        for var in undefined:
            print("undefined variable: ",var )
        continue

for var in defined_variables: 
    print(var,' defined but not referenced')