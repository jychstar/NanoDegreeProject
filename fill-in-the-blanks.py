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
# There should be 3 levels with 4 blanks each. The player will first choose a level to play, and then each time the player enter an answer for a blank. If the answer is correct, then continue to the next blank; if not, the player will be asked to enter again.

blanks  = ["___1___","___2___", "___3___", "___4___"]
sample1 = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary, tuple, and ___4___ or can be more complicated such as objects and lambda functions.'''
answer1=["function", "variables","None","list"]

sample2="___1___ intelligence is intelligence exhibited by machines. In ___2___ science, an ideal intelligent machine is a flexible rational agent that perceives its environment and takes actions that maximize its chance of success at some goal.Colloquially, the term ___1___ is applied when a machine mimics ___3___ functions that humans associate with other human minds, such as ___4___ and problem solving."
answer2=["Artificial", "computer", "cognitive","learning"]

sample3="___1___ intelligence (EI) or emotional quotient (EQ) is the capacity of individuals to ___2___ their own, and other people's emotions, to ___3___ between different feelings and ___4___ them appropriately, and to use emotional information to guide thinking and behavior. "
answer3=["Emotional","recognize","discriminate","label"]

# Plays a full game of Fill-in-the-Blanks. The player will first choose a level to play, and then each time the player enter an answer for a blank. If the answer is correct, then continue to the next blank; if not, the player will be asked to enter again.

def start_game():
    user_input = raw_input("choose level: 1, 2, or 3? ")
    if user_input=="1":
        result=play_game(sample1,answer1)
    if user_input=="2":
        result=play_game(sample2,answer2)
    if user_input=="3":
        result=play_game(sample3,answer3)
    return result

def play_game(sample, answer):
    print sample
    # print answer # for debugging purpose
    i=0 # indicate the sequenc of blanks
    user_input=None  #initiate user_input
    for word in answer: # loop over all answers
        while user_input !=word: # keep looping until the anwwer is right
            user_input = raw_input("Type in " + blanks[i] + ", or  quit to give up:")
            if user_input=="quit": # exit mechanism
                return "Good luck next time~"
        i=i+1
    return  "congratulations, you win!" 
print start_game()
