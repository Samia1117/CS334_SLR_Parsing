#!/usr/bin/env python
# coding: utf-8

# ### Welcome to Project 3: Building an interpreter and visualizations for a Cat and Mouse program

# In[1]:


# filename later gets updated to the .mc filename input by user

filepath = ""
extension = ".txt"
filename = "parsedata" + extension            ## FIRST RUN


# In[2]:


def makeTable(filename, LRtable):
    # Open parsedata.txt and do some file processing
    # This file is same for every .mc file to be processed, so it is done just once at the beginning
    file = open(filename, "r")
    idx = 0
    for line in file:
        lookaheads = line.split('&')
        LRtable.append(lookaheads)   # keep \n for now
        if idx == 38:
            break
        idx +=1
    idx = 0
    for line in file:
        lookaheads = line.split('&')[1:]         # get rid of the extra numbered row for variables
        LRtable[idx] = LRtable[idx] + lookaheads  # we'll concatenate it with the row of terminals already numbered
        idx +=1
        
    n = LRtable[0].index('$\n')
    for i in range(len(LRtable)):
        withNln =  LRtable[i][-1]
        LRtable[i][-1] = withNln[0:-1]
        withNln2 =  LRtable[i][n]
        LRtable[i][n] = withNln2[0:-1]
    return LRtable
    #print(LRtable)


# In[3]:


table = []
LRtable = makeTable(filename, table)  ### FIRST RUN
LRtable2 = LRtable.copy()

# print(len(LRtable[0]))
# print(len(LRtable[1]))


# In[4]:


# a nice visualization of the table

# from tabulate import tabulate
# print(tabulate(LRtable))


# In[5]:


# functions from project 1 - works as described there

def valid_int(word, digits):
    try:
        int(word)
    except ValueError:
        return False
    else:
        if word.startswith("0"):
            if len(word) >1:
                return False
        if len(word)>3:
            return False
        return True
    
def valid_variable(word, digits, letters):
    word = list(word)
    digits_in_word = set(word).intersection(set(digits))
    letters_in_word = set(word).intersection(set(letters))
    if (digits_in_word.union(letters_in_word) != set(word)):
        return False                  # foreign symbol outside letters and digits
    if (digits_in_word == set(word)):
        if len(word)<4:        # all digits but length less than 4
            return False
    return True     

def get_token_type(word, digits, letters, keywords, 
              punctuations):
    if ((word in keywords) or (word in punctuations)):
        return (word, "NULL")
    if valid_int(word, digits):
        return ("integer", word)
    if valid_variable(word, digits, letters):
        return ("variable", '0')
    else:
        return ("error", '0')

def comment_starts(wordsList):
    return wordsList.index('//')

def has_comment(wordsList):
    if '//' in wordsList:
        return True
    return False


# In[6]:


# Just a simple initialization of the variables we will deal with

def create_symtable(word, token_type, value, symtable):
    if (value == "NULL"):
        return
    if token_type == "integer":
        return
    variables_found = [symtable[k][1] for k in range(len(symtable)) if symtable[k][0] == "variable"]
    if token_type == "variable":
        if (word in variables_found):
            return   # no need to deal with this variable again
        else:
            symtable.append(["variable", word, [0, 0], 1])  # ["TYPE","CH VALUE", "POSITION", "ORIENTATION"]
            # 1 = north, 2 = east, 3 = south, 4 = west
        
    return
                


# In[7]:


def scanner(filename, symtable):  
    tuplist = []
    file = open(filename, "r")
    line_index = 0
    for line in file:
        if ('//' in line):
            idx = line.index('//')
            line = line[0:idx]
        words_in_line = line.strip().split(" ")
        if words_in_line == []:
            continue
        while(words_in_line[0] == '' or words_in_line[0] == '\t'):
            words_in_line = words_in_line[1:]
            if(len(words_in_line)) ==0:
                break
        if words_in_line == []:
            continue
        while(words_in_line[-1] == '' or words_in_line[-1] == '\t'):
            n = len(words_in_line)
            words_in_line = words_in_line[0:n]
        line_index +=1
        for word in words_in_line:
            if word == "":
                continue
            word = word.lower()
            (token_type, value) = get_token_type(word, digits, letters, keywords, punctuations)
            if token_type == "error":
                print("error on line: ", line_index, "on word: ", word, " with value: ", value)
                print(words_in_line)
                return
            else:
                if token_type == "intger":
                    word = int(word)
                tuplist.append((token_type, word)) # a list of the vaild tokens and their characters one by one
                create_symtable(word, token_type, value, symtable) # Throw this information away for now
    return tuplist


# In[8]:


def refine_strList(strList, specials, shorthands):
    inputStr = ''
    for item in strList:
        if item not in specials:
            inputStr += item[0]
        else:
            i = specials.index(item)
            inputStr += shorthands[i]
    return inputStr 


# In[9]:


# Has 5 fields -- maximum number of variables or terminals on the RHS of a production rule
# node.name is the first attribute and identifies the type of node
# Typically, 5th attribute (node.four) has a reference to another node
class Node(object):
    def __init__(self, name = "null", one = "null", two = "null", three = "null", four = "null"):
        self._name = name
        self._one = one
        self._two = two
        self._three = three
        self._four = four
        
    @property
    def name(self):
        return self._name
    @property
    def one(self):
        return self._one
    @property
    def two(self):
        return self._two
    @property
    def three(self):
        return self._three
    @property
    def four(self):
        return self._four
    
    @name.setter
    def name(self, value):
        self._name = value
    @one.setter
    def one(self, value):
        self._one = value
    @two.setter
    def two(self, value):
        self._two = value
    @three.setter
    def three(self, value):
        self._three = value
    @four.setter
    def four(self, value):
        self._four = value


# In[10]:


''' Return: a node object
    Parameters: two empty nodes objects: LHS and RHS, and a list of 'attributes' that are added to RHS node, and 
    then a reference from LHS is made to RHS through its fourth field
'''
def buildNode(LHS, RHS, attributes):      # RHS node is to be popped off the stack
    if ';' in attributes:
        attributes.remove(';')
    n = len(attributes)
    if n>5:
        print("6 attribute node found: ", attributes)
    for i in range(n):
        attribute = attributes[i]        # First build the RHS node, then set it as the rightmost field of LHS node 
        if i==0:
            RHS.name = attribute
        elif i==1:
            RHS.one = attribute
        elif i ==2:
            RHS.two = attribute
        elif i ==3:
            RHS.three = attribute
        elif i ==4:
            RHS.four = attribute
        #node.add_attribute(i, attribute)
        if (i== (n-1)):
            print("My fields are the following: ")
            print(RHS.name)
            print(RHS.one)
            print(RHS.two)
            print(RHS.three)
            print(RHS.four)
    if (RHS.name in ["cat", "mouse", "hole", "move", "clockwise", "repeat"]):
        LHS.name = "statement"
    elif (RHS.name in ["north", "east", "south", "west"]):
        LHS.name = RHS.name
    elif (RHS.name == "size"):
        LHS.name = "program"
    elif (RHS.name in ["sequenceNode", "statement"]):
        LHS.name = "sequenceNode"
    elif type(RHS.name) is Node:
        LHS.name = "sequenceNode"
    LHS.four = RHS
    return LHS


# In[11]:


'''Return: None
    Parameters: 2 stacks: the ststack building nested nodes, the 'vis_stack' to help visualize node building
    Updates the ststack to build program node, "semi bottom-up"
'''
def updateSTstack(ststack, vis_stack, org_vals, RHSnode, rule_num, ruleToVar):
    print("Original values: ", org_vals)
    if ("".join(RHSnode) == ruleToVar[rule_num][1]):
        #LHS = ruleToVar[rule_num][0]
        LHSnode = Node()
        RHSnode = Node()
        LHSnode = buildNode(LHSnode, RHSnode, org_vals)
        print("Found rule to RHS variable correspondence! Can use it to decide type of Node")
        vis_stack.append(ruleToVar[rule_num][0])
        ststack.append(LHSnode)
        print("LHS node is of type: ", LHSnode.name)
    print("STstack: ", ststack)
    print("vis stack: ", vis_stack)
    return


# In[12]:


# More global variables

LRtable = LRtable2[1:]
lookaheads = LRtable2[0]
#print(lookaheads)

ruleToVar = [('P*','P'), ('P', 'ziibLt'), ('L', 'S;'), ('L', 'LS;'), ('S', 'cviiD'), 
             ('S', 'mviiD'), ('S', 'hii'), ('S', 'ov'), ('S', 'ovi'), ('S', 'lv'), ('S', 'riLd'),
             ('D', 'n'), ('D', 's'), ('D', 'e'), ('D', 'w')]
rulestack = []


# In[13]:


def handleNextEntry(state, inputStr, tokenidx, stack, rulestack, ststack, vis_stack, wordList):
    lookahead = '$'
    org_word = ""
    if tokenidx<len(inputStr):
        lookahead = inputStr[tokenidx]
        org_word = wordList[tokenidx]
    lookahead_index = lookaheads.index(lookahead)
    entry = LRtable[state][lookahead_index]
    if entry == '':
        print("blank entry on this lookahead = ", lookahead, " with state = ",state, " breaking")
        print("##INVALID program##")
        return
    if entry.startswith('s'):
        stack.append(lookahead)
        ststack.append(org_word)
        vis_stack.append(org_word)
        
        next_state = int(entry[1:])
        stack.append(next_state)
        handleNextEntry(next_state, inputStr, tokenidx+1, stack, rulestack, ststack, vis_stack, wordList)
    elif entry.startswith('r'):
        rule_num = int(entry[1:])
        RHSvar = ruleToVar[rule_num][1]
        LHSvar = ruleToVar[rule_num][0]
        rulestack.append([rule_num, LHSvar, RHSvar])
        print("popping using reduction rule number: ", rule_num, " rule: ", LHSvar, " -> ", RHSvar, " Stack contents: ", stack)
        RHSnode = []
        org_vals = []
        for i in range(2*len(RHSvar)):
            if(i%2!=0):
                val = stack.pop()
                RHSnode.insert(0, val)
                continue
            org_val = ststack.pop()
            vis_stack.pop()
            org_vals.insert(0, org_val)
            stack.pop()
        updateSTstack(ststack, vis_stack, org_vals, RHSnode, rule_num, ruleToVar)
        next_state = int(stack[-1])            # before I push the LHS variable, mark which state I was last in
        stack.append(LHSvar)
        lookahead = stack[-1]
        lookahead_index = lookaheads.index(lookahead)
        entry = LRtable[next_state][lookahead_index] 
        stack.append(entry)   
        next_state = int(stack[-1])
        #print("final state of stack after reduction and pushing variable and new state: ", stack)
        handleNextEntry(next_state, inputStr, tokenidx, stack, rulestack, ststack, vis_stack, wordList)
    elif entry == 'acc':
        print("lookahead is $, stack contents = ", stack, " and entry is ", entry, " so, accept")
        print ("*** VALID PROGRAM ***: program-string can be derived using the grammar")
        #print("with rulestack: " , rulestack)
        # print("with original stack: " , org_stack)
        return ststack
    else:
        print("Encountered blank entry with stack = ", stack, "lookahead ", lookahead, "entry: ", entry )
        print ("*** INVALID PROGRAM ***: not syntactically correct")
    return


# In[14]:


## Set up input files and global parameters -- my files are in a folder called 'dataproj2'. Change to "" if in same folder

filepath = "dataproj2/"
#filepath = input("Please enter a filepath + "/", (empty string if same directory as this file): ")

keywords = ["begin", "halt","cat", "mouse", "clockwise", "move", "north", "south", "east", "west", "hole", 
          "repeat", "size", "end"]
punctuations = [";"]               
letters = list("abcdefghijklmnopqrstuvwxyz")
digits = list("0123456789")
specials = ['size', 'move', 'clockwise', 'end', 'halt']
shorthands = ['z', 'o', 'l', 'd', 't']

filename = input("Please enter a filename, (e.g. sample1.mc/ sample2.mc): ")
filename2 = filepath + filename


# In[15]:


# Same as in project 2
def parser(filename, rulestack, ststack, vis_stack, symtable):
    tuplist = scanner(filename, symtable)
    inputStr = ''
    wordList = []
    if tuplist != []:     
        strList = [tuplist[k][0] for k in range(len(tuplist))] # tupilist[1] is the word in line encountered
        wordList = [tuplist[k][1] for k in range(len(tuplist))]
        inputStr = refine_strList(strList, specials, shorthands)
    else:
        print("INVALID program: has invalid tokens")
    print(inputStr)
    stack = []
    state = 0
    stack.append(state)
    tokenidx = 0
    ststack = handleNextEntry(state, inputStr, tokenidx, stack, rulestack, ststack, vis_stack, wordList)
    return wordList


# In[16]:


ststack = []   #st stack will have 1 item at the end: a "program node" with references to all program statements
symtable = []
vis_stack = []
wordList = parser(filename2, rulestack, ststack, vis_stack, symtable)    ## SECOND RUN


# In[17]:


def direction_number(direction):  # directions = ["north =1", "east = 2", "south = 3", "west =4"]
    if direction == "north":
        return 1
    if direction == "east":
        return 2
    if direction == "south":
        return 3
    if direction == "west":
        return 4


# In[18]:


def addMovement(node, prev_position, new_position, statement_list, symtable): # of form moveRelative c3 -5 0
    result = check_same_position(node, new_position, symtable)
    # first display them on the same square anyway
    varname = node.one
    xoffset = (int(scale_factor))*(new_position[0] - prev_position[0])
    yoffset = -1*((int(scale_factor)))*(new_position[1] - prev_position[1])   # -1 because JSAWAA interprets (0,30) as 30 units south!
    command = "moveRelative " + varname + " " + str(xoffset) + " " + str(yoffset)
    statement_list.append(command)
    
    if result == "don't continue":   # then delete them
        more_command = "remove " + varname
        statement_list.append(command)
        print("removed something")
    print("prev_position: ", prev_position, "new_position ", new_position)
    return
    #print("calculated offsets:(x,y) ", xoffset, " ", yoffset)


# In[19]:


def check_same_position(node, new_pos, symtable):                      
    all_pos = [symtable[k][2] for k in range(len(symtable))]  # all positions in symtable 
    for i in range(len(all_pos)):
        if new_pos != [0,0] and new_pos == all_pos[i]:# if at least once this new position matches with another position already in symtable
            idx = i                               # index of other creature with new position
            if node.one != symtable[idx][1]:      # but not itself
                print("Something about to step on the same square as another!")# then we should get to this print, but I never did!
                if node.name == "cat" and symtable[idx][0] == "cat":
                    var = node.one
                    vars_found = [symtable[k][1] for k in range(len(symtable))]
                    cat_idx = vars_found.index(var)
                    symtable[cat_idx][1] = "REMOVED CAT"
                    print("REMOVED A CAT! SAME POSITION")
                    return "don't continue"
                elif node.name == "mouse" and symtable[idx][0] == "mouse":
                    hole_positions = [symtable[k][2] for k in range(len(symtable)) if symtable[k][0] == "hole"]
                    if new_pos in hole_positions:
                        return "continue"
                    var = node.one    # otherwise not in a hole
                    vars_found = [symtable[k][1] for k in range(len(symtable))]
                    mouse_idx = vars_found.index(var)
                    symtable[mouse_idx][1] = "REMOVED MOUSE"     # remove this mouse, not the other one
                    print("REMOVED A MOUSE! SAME POSITION")
                    return "don't continue"
                else:  # cat and mouse in same position
                    if node.name == "cat":    # then remove the mouse
                        symtable[idx][1] = "REMOVED MOUSE"
                        print("REMOVED A MOUSE! CAT ATE IT!")
                        return "don't continue"
                    else:# this var is a mouse, needs to be removed
                        var = node.one
                        vars_found = [symtable[k][1] for k in range(len(symtable))]
                        mouse_idx = vars_found.index(var)
                        symtable[mouse_idx][1] = "REMOVED MOUSE"
                        return "don't continue"
                        print("REMOVED A MOUSE! RAN INTO A CAT")
                    
    return "continue"


# In[20]:


def addCatorMouse(node, statement_list, symtable):             # of form circle c6 205 61 7 black transparent
    resized_two = int(scale_factor)*(int(node.two))
    resized_three = int(scale_factor)*(int(node.three))
    command = "circle " + node.one + " " + str(resized_two) + " " + str(resized_three) + " "
    if node.name == "cat":
        command += str(15)    #diam = 15
        command += " black yellow"
    else:
        command += str(6)    #diam = 15
        command += " black blue"
    statement_list.append(command)
    
    # Update "variable in symtable to cat or mouse"
    vars_found = [symtable[k][1] for k in range(len(symtable))]
    var_idx = vars_found.index(node.one)    # var name
    symtable[var_idx][0] = node.name    # set variable to cat or mouse
    return
        


# In[21]:


def addHole(node, statement_list, symtable):         # of form rectangle c6 205 61 7 10 black transparent
    holename = str(node.one)+str(node.two)
    symtable.append(["hole", holename, [int(node.one), int(node.two)], 0])  # hole same no direction
    
    resized_two = str(int(scale_factor)*(int(node.one)))
    resized_three = str(int(scale_factor)*(int(node.two)))
    command = "rectangle " + holename + " " + resized_two + " " + resized_three + " " + str(15) + " " + str(15) + " black black"
    statement_list.append(command)
    return


# In[22]:


def JSAWAA_line(symtable, node, statement_list):
    x = int(node.one)
    y = int(node.two)
    for i in range(x):
        step = 15*i
        line = "line hline" +str(i)+ " 0 " + str(step) + " " + str(700) + " " + str(step) + " black"    # line hline2 0 20 450 20 black 
        statement_list.append(line)
        if i*15>800:
            break
    for j in range(y):
        step = 15*j
        line = "line vline" +str(j)+ " "+ str(step) + " 0 " + str(step) + " 600 black"
        statement_list.append(line)
        if j*15>800:
            break
    return


# In[23]:


def update_symtable(symtable, node, statement_list):
    if node.name in ["cat", "mouse"]:
        print("Found cat or mouse node!")
        addCatorMouse(node, statement_list, symtable)
        var = node.one
        vars_found = [symtable[k][1] for k in range(len(symtable))]
        var_idx = vars_found.index(var)
        symtable[var_idx][2] = [int(node.two), int(node.three)]   # var two and three are initial cat and mouse positions
        direction = node.four.name    # orientation node is in var.four
        dir_num = direction_number(direction)
        symtable[var_idx][3] = dir_num
        #print(symtable)
    if node.name == "hole":
        print("Just need to put a hole at position x = : ", node.one, ", y = ", node.two, "!")
        addHole(node, statement_list, symtable)
    if node.name == "size":
        print("Just need to draw a grid of size x = : ", node.one, ", y = ", node.two, "!")
        JSAWAA_line(symtable, node, statement_list)
    if node.name =="clockwise":
        print("Found clockwise node!")
        var = node.one
        vars_found = [symtable[k][1] for k in range(len(symtable))]
        if var not in vars_found:
            print("Error, this cat or mouse has been removed before")
            return
        var_idx = vars_found.index(var)
        symtable[var_idx][3] +=1
        symtable[var_idx][3] = (symtable[var_idx][3])%4
        #print("current list of locations in table: ", [symtable[k][2] for k in range(len(symtable))])
    if node.name == "move":
        print("Found move node!")
        print("current list of locations in table: ", [symtable[k][2] for k in range(len(symtable))])
        var = node.one
        vars_found = [symtable[k][1] for k in range(len(symtable))]
        if var not in vars_found:
            print("Error, this cat or mouse has been removed before")
            return
        var_idx = vars_found.index(var)
        prev_position = symtable[var_idx][2].copy()
        dir_num = symtable[var_idx][3]        # need to move in this direction
        if node.two == "null":
            if (dir_num %2)==0:             #east, west are 0 mod 2; north,south are 1 mod 2; 
                if (dir_num ==2):
                    symtable[var_idx][2][0] +=1    # east
                else:
                    symtable[var_idx][2][0] -=1    # west
            else:
                if (dir_num ==1):
                    symtable[var_idx][2][1] +=1    # north
                else:
                    symtable[var_idx][2][1] -=1    # south
        else:
            if (dir_num %2)==0:             #east, west are 0 mod 2; north,south are 1 mod 2; 
                if (dir_num ==2):
                    symtable[var_idx][2][0] +=int(node.two)    # east
                else:
                    symtable[var_idx][2][0] -=int(node.two)   # west
            else:
                if (dir_num ==1):
                    symtable[var_idx][2][1] +=int(node.two)    # north
                else:
                    symtable[var_idx][2][1] -=int(node.two)    # south
        new_position = symtable[var_idx][2]
        addMovement(node, prev_position, new_position, statement_list, symtable)
        #print(symtable)
    return


# In[24]:


def traverse(symtable, node, statement_list):
    a = node.name
    b = node.one
    c = node.two
    d = node.three
    e = node.four
    #print(a, b, c, d, e)
    if type(a) is Node:
        if a.name == "repeat":
            print("#####Found repeat node!: ", a.one, " many times")
            for i in range(int(a.one)):   # a.one = how many times to repeat
                update_symtable(symtable, a.two, statement_list)
                traverse(symtable, a.two, statement_list)
        else:
            update_symtable(symtable, a, statement_list)
            traverse(symtable, a, statement_list)
    if type(b) is Node:
        if b.name == "repeat":
            print("#####Found repeat node: ", b.one, " many times")
            for i in range(int(b.one)):   # a.one = how many times to repeat
                update_symtable(symtable, b.two, statement_list)
                traverse(symtable, b.two, statement_list)
        else:
            update_symtable(symtable, b, statement_list)
            traverse(symtable, b, statement_list)
    if type(c) is Node:
        if c.name == "repeat":
            print("#####Found repeat node: ", c.one, " many times")
            for i in range(int(c.one)):   # a.one = how many times to repeat
                update_symtable(symtable, c.two, statement_list)
                traverse(symtable, c.two, statement_list)
        else:
            update_symtable(symtable, c, statement_list)
            traverse(symtable, c, statement_list)
    if type(d) is Node:
        if d.name == "repeat":
            print("#####Found repeat node: ", d.one, " many times")
            for i in range(int(d.one)):   # a.one = how many times to repeat
                update_symtable(symtable, d.two, statement_list)
                traverse(symtable, d.two, statement_list)
        else:
            update_symtable(symtable, d, statement_list)
            traverse(symtable, d, statement_list)
    if type(e) is Node:
        if e.name == "repeat":
            print("#####Found repeat node: ", e.one, " many times")
            for i in range(int(e.one)):   # a.one = how many times to repeat
                update_symtable(symtable, e.two, statement_list)
                traverse(symtable, e.two, statement_list)
        else:
            update_symtable(symtable, e, statement_list)
            traverse(symtable, e, statement_list)
    else:
        return


# In[25]:


node = ststack[0]                                                             ### THIRD/FINAL RUN
statement_list = []
scale_factor = input("Please enter a SCALE FACTOR to scale movements of cat and mice: ") # CHANGE THIS DEPENDING ON THE PROGRAM!
traverse(symtable, node, statement_list)


# In[26]:


# print(statement_list)


# In[27]:


out_fname = "outfile_" + filename + str(scale_factor) + ".txt"    # DEPENDS ON SCALE FACTOR AND .mc PROGRAM RAN!
f = open(out_fname, "w")
for line in statement_list:
    f.write(line)
    f.write("\n")
f.close()


# In[28]:


from tabulate import tabulate
print(tabulate(symtable, headers=["TYPE","CH VALUE", "POSITION", "ORIENTATION"]))


# ### Thank you!
