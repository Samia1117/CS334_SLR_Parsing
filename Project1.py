#!/usr/bin/env python
# coding: utf-8

# #### Author: Samia Zaman
# #### Date: 25 Feb, 2021
# ### CS 334 Project 1: Building an interpreter for CATANDMOUSE programming language- Part 1

# In[12]:


'''Return a boolean indicating whether given word was a valid token or not
    Arguments: 
    word - a string that is only a valid variable if it is comprised of numbers and digits
    digits - a list of strings in: 123456789
    letters - a list of strings in: abcdefg....xyz'''

def valid_variable(word, digits, letters):
    word = list(word)
    digits_in_word = set(word).intersection(set(digits))
    letters_in_word = set(word).intersection(set(letters))
    if (digits_in_word.union(letters_in_word) != set(word)):
        return False                  # foreign symbol outside letters and digits
    if (digits_in_word == set(word)):
        if len(word)<4:        # all digits but length less than 4
            return False
    return True               # otherwise, valid - mix of letters and digits


# In[13]:


'''Return a boolean indicating whether given word was a valid token or not
    Arguments: 
    word - a string that is only a valid variable if it is comprised of numbers and digits
    digits - a list of strings in: 123456789'''

def valid_int(word, digits):
    try:
        int(word)               # try casting to an int without program crashing
    except ValueError:
        return False
    else:
        if word.startswith("0"):    # extra conditions that need to be met
            if len(word) > 1:
                return False
        if len(word)>3:
            return False
        return True


# In[14]:


'''Return an integer index where '//' starts - indicating the start of a comment
Arguments:
    wordsList - a list of words (strings)'''
def comment_starts(wordsList):
    return wordsList.index('//')


# In[15]:


'''Return a boolean indicating whether '//' present in line or not
Arguments: 
    wordsList - a list of words (strings)'''
def has_comment(wordsList):
    if '//' in wordsList:
        return True
    return False


# In[16]:


'''Return a tuple of strings indicating the token type and the value of the word
Arguments: 
    word - a string which has a particular "token_type" 
    digits - a list of strings in: 123456789
    letters - a list of strings in: abcdefg....xyz
    keywords - a list of key words
    punctuations - just [;], for now '''

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
    


# In[17]:


'''Search for variable or integer already in table - otherwise insert integer/variable not seen before
Arguments: 
    word - a string with token_type = variable or integer
    value - a string with value = 0 if variable, and value of int if integer
    symTable - add to it 3-element lists of the form: [integer/variable, char value, int value]  '''

def search_and_insert(word, token_type, value, symTable):
    if (value == "NULL"):
        return []
    integers_found = [symTable[k][1] for k in range(len(symTable)) if symTable[k][0] == "integer"]
    variables_found = [symTable[k][1] for k in range(len(symTable)) if symTable[k][0] == "variable"]

    if token_type == "integer":
        if (int(value) in integers_found):
            index = integers_found.index(int(value))
            return [index, 0]
        
        else:
            symTable.append(["integer", int(value), int(value)])
            return[len(symTable), 0]
        
    elif (token_type == "variable"):
        if (word in variables_found):
            index = variables_found.index(word)
            return [index, 0]
        else:
            symTable.append(["variable", word, int(value)])
            return[len(symTable), 0]
    
                


# In[21]:


'''Main function for reading in the file specified, and printing whether each word in file is one of:
    1. A valid token - if so, print the token type and the value associated
    2. Invalid token - then print an error message specifying that line where token is
Additionally, it stores valid, unique tokens into a table, called symTable = 'symbol table'
Arguments:
    filename - file to be read
    symTable - initially an empty list; 
    to be filled with 1x3 arrays of unique tokens followed by their int and char values'''

def scanner(filename, symTable):
    file = open(filename, "r")
    line_index = 0
    for line in file:
        words_in_line = line.strip().split(" ")
        if has_comment(words_in_line):
            comment_index = comment_starts(words_in_line)
            words_in_line = words_in_line[0:comment_index]

        line_index +=1
        for word in words_in_line:
            word = word.lower()
            (token_type, value) = get_token_type(word, digits, letters, keywords, punctuations)
            # print((token_type, value))
            if token_type == "error":
                print("Error at line: " + str(line_index) + " on invalid token: '" + word +"'\n")
                pass
            else:
                print("Token is: " + word + ", with token type: " + token_type  + ", and value: " + value + "\n")
            location = search_and_insert(word, token_type, value, symTable) # Throw this information away for now
            print("location for this token in symbol table is (row, column): ", location, "\n")
    return symTable 
            


# In[19]:


# In[20]:

if __name__ == '__main__':
    pass
# Set up the default inputs to driver function
# Defaults are specific to those specified in CATANDMOUSE programming language
filepath = ""
filename = "p1.mc.txt"
symTable = []
keywords = ["begin", "halt","cat", "mouse", "clockwise", "move", "north", "south", "east", "west", "hole",
          "repeat", "size", "end"]
punctuations = [";"]
letters = list("abcdefghijklmnopqrstuvwxyz")
digits = list("0123456789")


# ### Run the driver function, 'scanner'
scanner(filename, symTable)


# In[22]:

#
# from tabulate import tabulate
# print(tabulate(symTable, headers=["TYPE","CH VALUE", "INT VALUE"]))


# In[ ]:




