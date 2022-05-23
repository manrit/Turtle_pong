# importing needed modules
import math
import random
import turtle
import time
from turtle import *

# making all variables global
global name_1, name_2, game_type, time_limit, time_limit_seconds, score_limit
global rally_counter, player_1_score, player_2_score


# function for resetting the paddles and balls
def reset():
    global rally_counter
    # resetting the ball and preparing to serve the ball to the player with the higher score
    ball.setpos(0, 0)
    y = random.randint(1, 2)
    x = random.randint(1, 2)
    if player_1_score > player_2_score:
        ball.dx = -5
        if y == 1:
            ball.dy = 5
        else:
            ball.dy = -5
    elif player_2_score > player_1_score:
        ball.dx = 5
        if y == 1:
            ball.dy = 5
        else:
            ball.dy = -5
    else:
        if y == 1:
            ball.dy = 5
        else:
            ball.dy = -5
        if x == 1:
            ball.dx = 5
        else:
            ball.dx = -5
    # Resetting the player paddles and the rally_count for bot players
    player_1.setpos(-680, 0)
    player_1.setheading(90)
    player_2.setpos(680, 0)
    player_2.setheading(90)
    rally_counter = 0


# function for the player 2 bot logic
def bot_logic(player_2_y):
    # making it possible to score on the bot
    move_dist = 20
    if rally_counter >= math.ceil(difficulty * 8 + (player_1_score + player_2_score)):
        move_dist -= 1
    # the bot's function to determine what it will do
    if ball_y > player_2_y + 20:
        player_2_y += move_dist
        if player_2_y >= 460:
            player_2_y = 460
    elif ball_y < player_2_y - 20:
        player_2_y -= move_dist
        if player_2_y <= -460:
            player_2_y = -460
    player_2.goto(680, player_2_y)


# functions for controlling player paddles
def move_up():
    y = player_1.ycor()
    y += 20
    player_1.sety(y)


def move_up_2():
    y = player_2.ycor()
    y += 20
    player_2.sety(y)


def move_down():
    y = player_2.ycor()
    y -= 20
    player_2.sety(y)


def move_down_2():
    y = player_2.ycor()
    y -= 20
    player_2.sety(y)


# function to play 1 frame of pong until a player scores, and update the score
def pong():
    global rally_counter, player_1_score, player_2_score
    # getting player and ball locations
    ball_x = ball.xcor()
    ball_y = ball.ycor()
    player_1_y = player_1.ycor()
    player_2_y = player_2.ycor()
    # writing the timer on screen if a timed game is chosen
    if game_type == 't':
        timer_text.clear()
        time_remaining = end - start
        minutes_remaining = int(time_remaining / 60)
        seconds_remaining = (time_remaining - minutes_remaining)
        timer_text.setpos(550, 0)
        timer_text.write(f'{minutes_remaining}:{seconds_remaining}', False, 'center', ('Courier', 20, 'bold'))
    # for a game with 1 player
    if num_players == 1:
        bot_logic(player_2_y)
    # for a game with no players
    elif num_players == 0:
        if ball_y > player_1_y + 40:
            player_1_y += 40
            if player_1_y >= 460:
                player_1_y = 460
        elif ball_y < player_1_y - 40:
            player_1_y -= 40
            if player_1_y <= -460:
                player_1_y = -460
        player_1.goto(680, player_1_y)
        bot_logic(player_2_y)
    # bots move 2 times per ball update when playing against a bot
        if ball_y > player_1_y + 40:
            player_1_y += 40
            if player_1_y >= 460:
                player_1_y = 460
        elif ball_y < player_1_y - 40:
            player_1_y -= 40
            if player_1_y <= -460:
                player_1_y = -460
        player_1.goto(680, player_1_y)
        bot_logic(player_2_y)
    # updating the ball's position
    ball.setx(ball_x + ball.dx)
    ball.sety(ball_y + ball.dy)
    update()
    # detecting collision with player 1's paddle
    if ball_x == -650 and (player_1_y - 40 <= ball_y <= player_1_y + 40):
        ball.setx(-649)
        ball.dx *= -1
    # detecting collision with player 2's paddle
    elif ball_x == 650 and (player_2_y - 40 <= ball_y <= player_2_y + 40):
        ball.setx(649)
        ball.dx *= 1
        if num_players == 2:
            rally_counter += 1
    # detecting collision with the top and bottom wall
    elif ball_y > 500:
        ball.sety(500)
        ball.dy *= -1
    elif ball_y < -500:
        ball.sety(-500)
        ball.dy *= -1
    # detecting goals
    elif ball_x > 700:
        player_1_score += 1
    elif ball_x < -700:
        player_2_score += 1
    # applying goals to the appropriate player
    if player_1_score > player_1_score_counter:
        turtle.textinput('Score',
                         f'{name_1} scored! the score is now\n '
                         f'{name_1}:{player_1_score} to {name_2}:{player_2_score},'
                         f' first to {score_limit} wins!')
        # resetting the paddles and balls
        reset()

    elif player_2_score > player_2_score_counter:
        turtle.textinput('Score',
                         f'{name_2} scored! the score is now\n '
                         f'{name_1}:{player_1_score} to {name_2}:{player_2_score},'
                         f' first to {score_limit} wins!')
        # resetting the paddles and balls
        reset()


# different game ending messages depending on the outcome of the game
def game_endings():
    global play_again, num_games_played, player_1_wins, player_2_wins
    # player 1 victory
    if player_1_score > player_2_score:
        play_again = turtle.textinput('Game',
                                      f'GG, {name_1} won by {player_1_score - player_2_score} points!\n'
                                      f'Play again? (y/n)')
        player_1_wins += 1
        num_games_played += 1
    # player 2 victory
    elif player_2_score > player_1_score:
        play_again = turtle.textinput('Game',
                                      f'GG, {name_2} won by {player_2_score - player_1_score} points!\n'
                                      f'Play again? (y/n)')
        player_2_wins += 1
        num_games_played += 1
    # a tie
    else:
        play_again = turtle.textinput('Game',
                                      f'GG, it was a tie!\n'
                                      f'Play again? (y/n)')
        num_games_played += 1
    # forcing a valid input for play again
    while play_again != 'y' and play_again != 'n':
        play_again = play_again = turtle.textinput('Game',
                                                   f'Invalid input, please try again\n'
                                                   f'Play again? (y/n)')


# setting up variables
player_1_wins = 0
player_2_wins = 0
num_games_played = 0
play_again = 'y'
# allowing multiple games to be played
while play_again == 'y':
    if num_games_played == 0:
        # setting up the game
        # setting up a screen
        wn = turtle.Screen()
        wn.screensize(700, 500)
        wn.bgcolor('black')
        wn.title('Pong')
        wn.setworldcoordinates(-700, -500, 700, 700)
        # setting up a border
        border = turtle.Turtle()
        border.ht()
        border.color('white')
        border.pensize(3)
        border.penup()
        border.speed(40)
        border.goto(700, -500)
        border.pendown()
        border.left(90)
        border.forward(1000)
        border.left(90)
        border.forward(1400)
        border.left(90)
        border.forward(1000)
        border.left(90)
        border.forward(1400)
        # setting up player 1's paddle
        player_1 = turtle.Turtle()
        player_1.speed(0)
        player_1.ht()
        player_1.shape('square')
        player_1.color('white')
        player_1.turtlesize(2, 6)
        player_1.penup()
        player_1.setpos(-680, 0)
        player_1.setheading(90)
        player_1.st()
        # setting up player 2's paddle
        player_2 = turtle.Turtle()
        player_2.speed(0)
        player_2.ht()
        player_2.color('white')
        player_2.shape('square')
        player_2.turtlesize(2, 6)
        player_2.penup()
        player_2.setpos(680, 0)
        player_2.setheading(90)
        player_2.st()
        # setting up the ball to go randomly to either the top or bottom or a random player
        ball = turtle.Turtle()
        ball.shape('circle')
        ball.color('white')
        ball.speed(40)
        ball.penup()
        ball.setpos(0, 0)

        y = random.randint(1, 2)
        x = random.randint(1, 2)
        if player_1_score > player_2_score:
            ball.dx = -5
            if y == 1:
                ball.dy = 5
            else:
                ball.dy = -5
        elif player_2_score > player_1_score:
            ball.dx = 5
            if y == 1:
                ball.dy = 5
            else:
                ball.dy = -5
        else:
            if y == 1:
                ball.dy = 5
            else:
                ball.dy = -5
            if x == 1:
                ball.dx = 5
            else:
                ball.dx = -5
        # getting the number of players
        num_players = turtle.numinput('Game',
                                      'How many players?(up to 2)')
        # forcing a valid input to continue
        while num_players > 2 or num_players < 0:
            num_players = turtle.numinput('Game',
                                          'Invalid input please try again\n'
                                          'How many players?(up to 2)')

        # using input to know how many names to request, and then getting names of the players
        # as well as enabling controls
        # for a 2 player game
        if num_players == 2:
            name_1 = turtle.textinput('Game',
                                      'Name of player 1?')
            name_2 = turtle.textinput('Game',
                                      'Name of player 2?')
            wn.listen()
            wn.onkeypress(move_up, key='w')
            wn.onkeypress(move_down, key='s')
            wn.onkeypress(move_up_2, 'Up')
            wn.onkeypress(move_down_2, 'Down')
        # for a single player game
        elif num_players == 1:
            name_1 = turtle.textinput('Game',
                                      'Name of player 1?')
            name_2 = 'Carl'
            difficulty = turtle.numinput('Game',
                                         'Carl difficulty?'
                                         '(warning numbers above 3 will result in a very difficult,'
                                         ' and very long game, '
                                         ' decimal point values are allowed)')
            wn.listen()
            wn.onkeypress(move_up, key='w')
            wn.onkeypress(move_down, key='s')
        # for a game of just bots
        elif num_players == 0:
            name_1 = 'Fredrick'
            name_2 = 'Carl'

        name_len1 = len(name_1)
        name_len2 = len(name_2)
        while name_len1 < 2 and name_len2 < 2:
            if num_players == 2:
                name_1 = turtle.textinput('Game',
                                          'Error, name too short, please try again'
                                          'Name of player 1?')
                name_2 = turtle.textinput('Game',
                                          'Error, name too short, please try again'
                                          'Name of player 2?')
            elif num_players == 1:
                name_1 = turtle.textinput('Game',
                                          'Error, name too short, please try again'
                                          'Name of player 1?')
                name_2 = 'Carl'
                difficulty = turtle.numinput('Game',
                                             'Carl difficulty?'
                                             '(warning numbers above 3 will result in a very difficult,'
                                             ' and very long game, '
                                             ' decimal point values are allowed)')
        game_type = turtle.textinput('Game',
                                     'Play to score limit or play to time limit?'
                                     '(s for score limit, t for time limit)')
        while game_type != 't' and game_type != 's':
            game_type = turtle.textinput('Game',
                                         'Error, invalid input, please try again'
                                         'Play to score limit or play to time limit?'
                                         '(s for score limit, t for time limit)')
        if game_type == 's':
            score_limit = round(abs(turtle.numinput('Game',
                                                    'How many points to play to?')))
        elif game_type == 't':
            time_limit = float('{:.2f}'.format(abs(turtle.numinput('Game',
                                                                   'How long should the game last?'
                                                                   '(in the form of minutes.seconds'))))
            time_limit_seconds = ((time_limit - int(time_limit)) * 100) + (int(time_limit) * 60)
            timer_text = turtle.Turtle()
            timer_text.ht()
            timer_text.color(white)
    # displaying the number of games the players have played, and the win record of those games
    else:
        turtle.textinput('Game',
                         f'Games played: {num_games_played}\n'
                         f'Win Record: \n'
                         f'{name_1}: {player_1_wins}\n{name_2}: {player_2_wins}')
    player_1_score = 0
    player_2_score = 0
    # playing a first to set score match
    if game_type == 's':
        # Playing looping the pong function to play pong until 1 player reaches the score limit
        while (player_1_score < score_limit) and (player_2_score < score_limit):
            # updating the score on the top of the scene, and player score counts
            score_boi = turtle.Turtle()
            score_boi.clear()
            score_boi.ht()
            score_boi.color('white')
            score_boi.setpos(650, 0)
            score_boi.write(f'{player_1_score} | {player_2_score}', False, 'center', ('Courier', 20, 'bold'))
            player_1_score_count = player_1_score
            player_2_score_count = player_1_score
            # playing pong
            while player_1_score == player_1_score_count and player_2_score == player_2_score_count:
                pong()
        # declaring a winner
        game_endings()
    # playing a timed match
    elif game_type == 't':
        # starting the timer
        start = time.time()
        start = float('{:.2f}'.format(start))
        end = time_limit_seconds + start
        while time_remaining > 0:
            # updating the score on the top of the scene, and player score counts
            score_boi = turtle.Turtle()
            score_boi.clear()
            score_boi.ht()
            score_boi.color('white')
            score_boi.setpos(450, 0)
            score_boi.write(f'{player_1_score} | {player_2_score}', False, 'center', ('Courier', 20, 'bold'))
            player_1_score_count = player_1_score
            player_2_score_count = player_1_score
            # playing pong
            while player_1_score == player_1_score_count and player_2_score == player_2_score_count:
                pong()
        # declaring a winner
        game_endings()
        turtle.exitonclick()