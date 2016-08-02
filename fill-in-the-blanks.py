# IPND Stage 2 Final Project

# You've built a Mad-Libs game with some help from Sean.
# Now you'll work on your own game to practice your skills and demonstrate what you've learned.

# For this project, you'll be building a Fill-in-the-Blanks quiz.
# Your quiz will prompt a user with a paragraph containing several blanks.
# The user should then be asked to fill in each blank appropriately to complete the paragraph.
# This can be used as a study tool to help you remember important vocabulary!

# Note: Your game will have to accept user input so, like the Mad Libs generator,
# you won't be able to run it using Sublime's `Build` feature.
# Instead you'll need to run the program in Terminal or IDLE.
# Refer to Work Session 5 if you need a refresher on how to do this.

# To help you get started, we've provided a sample paragraph that you can use when testing your code.
# Your game should consist of 3 or more levels, so you should add your own paragraphs as well!

sample = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by
adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you
don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary,
tuple, and ___4___ or can be more complicated such as objects and lambda functions.'''

parts_of_speech1  = ["___1___", "___1___s","___2___", "___3___", "___4___", "___5___"]

# Checks if a word in parts_of_speech is a substring of the word passed in.
def word_in_pos(word, parts_of_speech):
    for pos in parts_of_speech:
        if pos in word:
            return pos
    return None

# Plays a full game of mad_libs. A player is prompted to replace words in ml_string,
# which appear in parts_of_speech with their own words.
def play_game(ml_string, parts_of_speech1):
    replaced = []
    already_input=[]
    input_list=[]
    ml_string = ml_string.split()
    for word in ml_string:
        matched = word_in_pos(word, parts_of_speech1)
        if matched != None:
            if matched not in already_input:
                user_input = raw_input("Type in a: " + matched + " ")
                already_input.append(matched) #store the replaced terms
                input_list.append (user_input) # store the replace values
                if len(already_input)==1:
                    already_input.append("___1___s")
                    input_list.append(user_input)
                word = word.replace(matched, user_input)
            else:
                word = input_list[already_input.index(matched)]
        replaced.append(word)
        print replaced
    replaced = " ".join(replaced)
    return replaced

print play_game(sample, parts_of_speech1)
