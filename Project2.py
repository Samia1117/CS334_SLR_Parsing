#!/usr/bin/env python
# coding: utf-8

# ### Welcome to CS 334 spring 2021, Project 2
# ### 01 April, 2021

# In[1]:


# Open parsedata.txt and do some file processing
# This file is same for every .mc file to be processed, so it is done just once at the beginning

filepath = ""
extension = ".txt"
filename = "parsedata" + extension
file = open(filename, "r")

LRtable = []
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
print(LRtable)


# In[2]:


# Get rid of the newlines
n = LRtable[0].index('$\n')
for i in range(len(LRtable)):
    withNln =  LRtable[i][-1]
    LRtable[i][-1] = withNln[0:-1]
    withNln2 =  LRtable[i][n]
    LRtable[i][n] = withNln2[0:-1]

print(LRtable[0])
print(LRtable)
# Keep a copy of the table so that I don't have to change the global variable name LRtable
LRtable2 = LRtable.copy()


# In[3]:


# # just ensuring that got rid of the '' as well when no '\n' to remove
print(len(LRtable[0]))
print(len(LRtable[1]))
print(len(LRtable[2]))


# In[4]:


# a nice visualization of the table
from tabulate import tabulate
print(tabulate(LRtable))


# In[5]:


# functions from project 1 -- will not give detailed description again

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


'''scanner (main) function from Project 1: the only change made to it were to:

1. Not make entries in the symbol table since we have no use for it (we want to consider all and not only unique tokens)
2. Put each (token type, word (-i.e. token)) identified in program in a list called tuplist
   
Return:
       tupist - list of tuples with strings (token_type, word), where the token is a valid token
       If invalid token is encountered at any point, returns an empty list''' 

def scanner(filename):
    tuplist = []
    file = open(filename, "r")
    line_index = 0
    for line in file:
        words_in_line = line.strip().split(" ")
        if (words_in_line[0] == ''):
            continue
        if has_comment(words_in_line):
            comment_index = comment_starts(words_in_line)
            comment_index -=1
            # ignore white spaces until a non empty character is reached - (correcting error from project 1)
            while(words_in_line[comment_index] == ''):
                comment_index -=1
            # ignore comments:
            words_in_line = words_in_line[0:comment_index+1]
        line_index +=1
        for word in words_in_line:
            word = word.lower()
            (token_type, value) = get_token_type(word, digits, letters, keywords, punctuations)
            if token_type == "error":
                print("error")
                return []
            else:
                tuplist.append((token_type, word)) # a list of the vaild tokens and their characters one by one
                #print("Token is: " + word + ", with token type: " + token_type  + ", and value: " + value + "\n")
    #print(strList)
    return tuplist
            


# In[7]:


'''Function to return a shortened string version of the cat and mouse program given the list of valid tokens in the program
    This shortened version has only 1-character prefixes of all token types, mostly using first character
    (e.g. 'i' for 'integers') with a few exceptions when non-first characters are chosen for a handful of 
    'special' tokens

Arguments:
          strList - list of strings that are the valid 'token types' found
          specials - token types for whom non-first characters are chosen as their 1-character representation
          shorthands - list of rules dictating which non-first characters to choose for each special token
Return:
       inputStr - the shortened string version of the list of tokens in the cat and mouse program plus a $ added at the end
                    - input to the parser'''
def refine_strList(strList, specials, shorthands):
    inputStr = ''
    for item in strList:
        if item not in specials:
            inputStr += item[0]
        else:
            i = specials.index(item)
            inputStr += shorthands[i]
    return inputStr                      #+'$'


# In[8]:


'''Return: None;
    Just print the parsing stack as it is dynamically updated; and a rule stack, where the rules used to reduce
    tokens are added in the bottom up fashion/ in the reverse order from that used in derivation of program from grammar
Arguments: 
    state - corresponding to rows in the LR parsing table starting from the row labelled 0
    inputStr - a string representing all the valid tokens ina cat and mouse program; 
    each character is the prefix (or a special letter in the middle) of a token
    tokenidx - the index of character in inputStr that is currently the lookahead and is guiding the parsing
    stack - a parsing stack where terminals, variables, and states are temporarily stored by shifting them,
    and eventually popped off by reduction rules
    rulestack - list of tuples of the form (LHS, RHS) corresponding to reduction rules used in parsing input string
    
Global arguments (because they're static):
     ruleToVar - a list of tuples, representing rules of reduction corresponding to entries in the table;
                 the rules in the form: (LHS, RHS); and the index in the list represents the rule number
     LR table - the LR table given, formatted to dimensions 38 by 23'''
     
def handleNextEntry(state, inputStr, tokenidx, stack, rulestack):
    print("stack: ", stack)
    print("token index ", tokenidx)
    print("State, ", state)
    lookahead = '$'
    if tokenidx<len(inputStr):
        lookahead = inputStr[tokenidx]
    print("current lookahead: ", lookahead)
    lookahead_index = lookaheads.index(lookahead)
    print("lookahead index", lookahead_index)
    entry = LRtable[state][lookahead_index]
    print("table entry: ", entry)
    if entry == '':
        print("blank entry on this lookahead = ", lookahead, " with state = ",state, " breaking")
        return
    if entry.startswith('s'):
        stack.append(lookahead)
        next_state = int(entry[1:])
        stack.append(next_state)
        handleNextEntry(next_state, inputStr, tokenidx+1, stack, rulestack)
    elif entry.startswith('r'):
        rule_num = int(entry[1:])
        RHSvar = ruleToVar[rule_num][1]
        LHSvar = ruleToVar[rule_num][0]
        rulestack.append([rule_num, LHSvar, RHSvar])
        for i in range(2*len(RHSvar)):
            print("popping using reduction rule number: ", rule_num, " rule: ", LHSvar, " -> ", RHSvar, " Stack contents: ", stack)
            stack.pop()
        next_state = int(stack[-1]) # before I push the LHS variable, mark which state I was last in
        print("stack after popping: ", stack)
        stack.append(LHSvar)
        print("stack after appending LHS var: ", stack)
        lookahead = stack[-1]
        print("next lookahead: ", lookahead)
        lookahead_index = lookaheads.index(lookahead)
        entry = LRtable[next_state][lookahead_index] # now LHS variable is the lookahead, and the last state is new state; squeezing in the operation that we do at the beginning of the function, to avoid complication/need to change the code further
        stack.append(entry)   # this entry is only a number
        print("stack after appending entry after that lookahead: ", stack)
        next_state = int(stack[-1]) # same as entry
        print("final state of stack after reduction and pushing variable and new state: ", stack)
        handleNextEntry(next_state, inputStr, tokenidx, stack, rulestack)
    elif entry == 'acc':
        print("lookahead is $, stack contents = ", stack, " and entry is ", entry, " so, accept")
        print ("*** VALID PROGRAM ***: program-string can be derived using the grammar")
        print("with rulestack: " , rulestack)
    else:
        print("Encountered blank entry with stack = ", stack, "lookahead ", lookahead, "entry: ", entry )
        print ("*** INVALID PROGRAM ***: not syntactically correct")
        


# In[9]:


## Set up the input files and global parameters

filepath = "dataproj2/"
#filepath = input("Please enter a filepath + "/", (empty string if same directory as this file): ")

keywords = ["begin", "halt","cat", "mouse", "clockwise", "move", "north", "south", "east", "west", "hole", 
          "repeat", "size", "end"]
punctuations = [";"]               # only ; for now
letters = list("abcdefghijklmnopqrstuvwxyz")
digits = list("0123456789")
specials = ['size', 'move', 'clockwise', 'end', 'halt']
shorthands = ['z', 'o', 'l', 'd', 't']

filename = input("Please enter a filename, (e.g. sample1.mc/ sample2.mc): ")
filename = filepath + filename


# In[10]:


# More global variables

LRtable = LRtable2[1:]
lookaheads = LRtable2[0]
print(lookaheads)
ruleToVar = [('P*','P'), ('P', 'ziibLt'), ('L', 'S;'), ('L', 'LS;'), ('S', 'cviiD'), 
             ('S', 'mviid'), ('S', 'hii'), ('S', 'ov'), ('S', 'ovi'), ('S', 'lv'), ('S', 'riLd'),
             ('D', 'n'), ('D', 's'), ('D', 'e'), ('D', 'w')]
rulestack = []


# In[11]:


'''Main driver function

Arguments:
    filename - the name of the .mc file containing cat and mouse program
Global arguments:
    specials - token types for whom non-first characters are chosen as their 1-character representation
    shorthands - list of rules dictating which non-first characters to choose for each special token
Returns:
    None - calls the SLR(1) parsing algorithm and so prints parsing stack contents, as well as 
            order of use of rules (I have left the rules in the tuple format: (LHS, RHS))'''

def parser(filename, rulestack):
    tuplist = scanner(filename)
    inputStr = ''
    if tuplist !='[]':     
        # print(tuplist)
        strList = [tuplist[k][0] for k in range(len(tuplist))]
        # print(strList)
        inputStr = refine_strList(strList, specials, shorthands)
    else:
        print("INVALID program: has invalid tokens")
    print(inputStr)
    stack = []
    state = 0
    stack.append(state)
    tokenidx = 0
    handleNextEntry(state, inputStr, tokenidx, stack, rulestack)
    for i in range(len(rulestack)):
        ruleidx = rulestack[-i-1][0]
        print("Rule number, rule in right order: ", rulestack[-1-i][0], ruleToVar[ruleidx], "\n")


# In[12]:


parser(filename, rulestack)


# ### Thank you!
