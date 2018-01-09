import random
from flask import Flask, render_template, request,url_for, redirect, session

app = Flask(__name__)


""" All variable set`s have 4 items, this feature is used by creating 4 element lists where elements are compared
    with iterators. Main function is mastermind, the other functions are helper-functions for mastermind. """


""" Generate random numbers. Populate answer lists & set number of guesses to zero """
def random_answer_list():

    del answer_list[:]
    answer_list.extend([random.randint(1,9),random.randint(1,9),random.randint(1,9),random.randint(1,9)])


def count_guess():

    number_of_guess = int(request.form["guesses"])
    number_of_guess += 1

    return number_of_guess


""" Get previous entered values if exist"""
def populate_prev_guess_list(prev_guess):

    for iterate in range (0,len(prev_numbers)):
        if request.form[prev_numbers[iterate]]:
            prev_guess[iterate] += request.form[prev_numbers[iterate]]

    return prev_guess


""" Get entered values & add to previous value list """
def populate_guess_list(guess_list,prev_guess):

    for iterate in range (0,len(guess_numbers)):
        if request.form[guess_numbers[iterate]]:
            guess_list.append(int(request.form[guess_numbers[iterate]]))
            prev_guess[iterate] += request.form[guess_numbers[iterate]]

    return guess_list,prev_guess


"""  Get right guesses & Get right value in wrong place"""
def right_guesses(answer_list,guess_list):

    matches = 0
    part_match = 0
    temporary_list = list(answer_list)
    for iterate in range(0,len(answer_list)):
        if answer_list[iterate] == int(request.form[guess_numbers[iterate]]):
            matches += 1
            temporary_list.remove(answer_list[iterate])
            guess_list.remove(answer_list[iterate])

    if guess_list:
        for item in guess_list:
            if item in temporary_list:
                part_match += 1
                temporary_list.remove(item)

    return matches,part_match


@app.route("/mastermind/", methods=['GET', 'POST'])
def mastermind():
    guess_list = list()
    prev_guess = ["","","",""]

    """ Get values if any from guesser.
        Generate random numbers or get numbers hidden inside form if they exist """

    if request.method == 'POST':
            number_of_guess = count_guess()
            prev_guess = populate_prev_guess_list(prev_guess)
            guess_list,prev_guess = populate_guess_list(guess_list,prev_guess)

            if len(answer_list) == len(guess_list) == 4:
                flag = True
                matches,part_match = right_guesses(answer_list,guess_list)
            else:
                flag = False
                number_of_guess = matches = part_match = 0

            return render_template('mastemind-template.html',answer_list=answer_list,number_of_guess=number_of_guess,prev_guess=prev_guess,matches=matches,part_match=part_match,flag=flag)

    else:
            random_answer_list()
            number_of_guess = 0

            return render_template('mastemind-template.html',answer_list=answer_list,number_of_guess=number_of_guess,prev_guess=prev_guess,flag=True)


@app.errorhandler(404)
def page_not_found(error):

    return 'No luck, This page does not exist', 404


if __name__ == "__main__":

    """ Define global variables from html-form. """
    answer_numbers = ["answer1","answer2","answer3","answer4"]
    guess_numbers = ["guessnumber1","guessnumber2","guessnumber3","guessnumber4"]
    prev_numbers = ["prev1","prev2","prev3","prev4"]
    answer_list = list()

    app.run(debug=True)                   #Remove debug = True before deplying!!!!
