# manrit Kaur

# importing needed modules
import math
import random
import turtle
import time
from turtle import *

# making all variables global
global name_1, name_2, game_type, time_limit, time_limit_seconds, score_limit, time_remaining
global rally_counter, player_1_score, player_2_score


# function for resetting the paddles and balls
def reset():
    global rally_counter
    # resetting the ball and preparing to serve the ball to the player with the higher score
    ball.setpos(0, 0)
    rand1 = random.randint(1, 2)
    rand2 = random.randint(1, 2)
    if player_1_score > player_2_score:
        ball.dx = -5
        if rand1 == 1:
            ball.dy = 5
        else:
            ball.dy = -5
    elif player_2_score > player_1_score:
        ball.dx = 5
        if rand1 == 1:
            ball.dy = 5
        else:
            ball.dy = -5
    else:
        if rand1 == 1:
            ball.dy = 5
        else:
            ball.dy = -5
        if rand2 == 1:
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
def bot_logic(player_2_y, rally_counter1):
    # making it possible to score on the bot
    ball_y = ball.ycor()
    move_dist = 20
    rally_counter = rally_counter1
    if rally_counter >= math.ceil(difficulty * 8 + (player_1_score + player_2_score)):
        move_dist -= 1
    # the bot's function to determine what it will do
    if ball_y > player_2_y + 20:
        player_2_y += move_dist
        if player_2_y >= 410:
            player_2_y = 410
    elif ball_y < player_2_y - 20:
        player_2_y -= move_dist
        if player_2_y <= -410:
            player_2_y = -410
    player_2.goto(680, player_2_y)


# functions for controlling player paddles
def move_up():
    y = player_1.ycor()
    y += 20
    if y >= 410:
        y = 410
    player_1.sety(y)


def move_up_2():
    y2 = player_2.ycor()
    y2 += 20
    if y2 >= 410:
        y2 = 410
    player_2.sety(y2)


def move_down():
    y = player_1.ycor()
    y -= 20
    if y <= -410:
        y = -410
    player_1.sety(y)


def move_down_2():
    y2 = player_2.ycor()
    y2 -= 20
    if y2 <= -410:
        y2 = -410
    player_2.sety(y2)


# function to play 1 frame of pong until a player scores, and update the score
def pong():
    global rally_counter, player_1_score, player_2_score, player_1_score_count, player_2_score_count
    global minutes_remaining, seconds_remaining, current_time, time_remaining_seconds, time_remaining
    ball_x = ball.xcor()
    ball_y = ball.ycor()
    player_1_y = player_1.ycor()
    player_2_y = player_2.ycor()
    rally_counter = 0
    # writing the timer on screen if a timed game is chosen
    if game_type == 't':
        time_remaining = end - time.time()

        minutes_remaining = int(time_remaining / 60)
        seconds_remaining = int(float('{:.2f}'.format((time_remaining - (minutes_remaining*60)))))
        if seconds_remaining != current_time:
            timer_text.clear()
            if seconds_remaining + minutes_remaining >= 0:
                timer_text.write(f'{minutes_remaining}:{seconds_remaining}', False, 'center', ('Courier', 20, 'bold'))
            else:
                player_1_score_count += 1
                player_2_score_count += 1
            current_time = seconds_remaining
    # for a game with 1 player
    if num_players == 1:
        bot_logic(player_2_y, rally_counter)
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
        bot_logic(player_2_y, rally_counter)
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
        bot_logic(player_2_y, rally_counter)
    # updating the ball's position
    ball.setx(ball_x + ball.dx)
    ball.sety(ball_y + ball.dy)
    update()
    # getting player and ball locations
    ball_x = ball.xcor()
    ball_y = ball.ycor()
    player_1_y = player_1.ycor()
    player_2_y = player_2.ycor()
    # detecting collision with player 1's paddle
    if -690 <= ball_x <= -650 and (player_1_y - 90 <= ball_y <= player_1_y + 90):
        ball.setx(-649)
        ball.dx *= -1
    # detecting collision with player 2's paddle
    if 650 <= ball_x <= 690 and (player_2_y - 90 <= ball_y <= player_2_y + 90):
        ball.setx(649)
        ball.dx *= -1
        if num_players == 2:
            rally_counter += 1
    # detecting collision with the top and bottom wall
    if ball_y > 495:
        ball.sety(495)
        ball.dy *= -1
    if ball_y < -495:
        ball.sety(-495)
        ball.dy *= -1
    # detecting goals
    if ball_x > 700:
        player_1_score += 1
    if ball_x < -700:
        player_2_score += 1
    # applying goals to the appropriate player
    if player_1_score > player_1_score_count:
        turtle.textinput('Score',
                         f'{name_1} scored! the score is now\n '
                         f'{name_1}: {player_1_score}\n'
                         f'{name_2}: {player_2_score}')
        # resetting the paddles and balls
        score_boi.clear()
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

    elif player_2_score > player_2_score_count:
        turtle.textinput('Score',
                         f'{name_1} scored! the score is now\n '
                         f'{name_1}: {player_1_score}\n'
                         f'{name_2}: {player_2_score}')
        # resetting the paddles and balls
        score_boi.clear()
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
        wn.setworldcoordinates(-705, -505, 705, 705)
        # setting up a border
        border = turtle.Turtle()
        border.ht()
        border.penup()
        border.color('white')
        border.pensize(5)
        border.speed(40)
        border.setpos(700, -500)
        border.pendown()
        border.left(90)
        border.forward(1000)
        border.left(90)
        border.forward(1400)
        border.left(90)
        border.forward(1000)
        border.left(90)
        border.forward(1400)
        border.penup()
        border.pensize(1)
        border.setpos(0, -500)
        border.pendown()
        border.setheading(90)
        border.forward(1005)
        border.penup()
        border.color('black')
        border.pendown()
        border.forward(300)
        # setting up player 1's paddle
        player_1 = turtle.Turtle()
        player_1.speed(0)
        player_1.ht()
        player_1.penup()
        player_1.shape('square')
        player_1.color('white')
        player_1.turtlesize(2, 6)
        player_1.setpos(-670, 0)
        player_1.setheading(90)
        player_1.st()
        # setting up player 2's paddle
        player_2 = turtle.Turtle()
        player_2.speed(0)
        player_2.ht()
        player_2.penup()
        player_2.color('white')
        player_2.shape('square')
        player_2.turtlesize(2, 6)
        player_2.setpos(670, 0)
        player_2.setheading(90)
        player_2.st()
        # setting up the ball to go randomly to either the top or bottom or a random player
        ball = turtle.Turtle()
        ball.penup()
        ball.shape('circle')
        ball.color('white')
        ball.speed(40)
        ball.setpos(0, 0)

        y = random.randint(1, 2)
        x = random.randint(1, 2)
        if player_1_wins > player_2_wins:
            ball.dx = -5
            if y == 1:
                ball.dy = 5
            else:
                ball.dy = -5
        elif player_2_wins > player_1_wins:
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
                                      'How many players? (up to 2)')
        # forcing a valid input to continue
        while num_players > 2 or num_players < 0:
            num_players = turtle.numinput('Game',
                                          'Invalid input please try again\n'
                                          'How many players? (up to 2)')

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
                                         'Bot difficulty?\n'
                                         '(warning numbers above 3 will result in a very difficult and long game)\n'
                                         '(decimal point values are allowed)')
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
                                          'Error, name too short, please try again\n'
                                          'Name of player 1?')
                name_2 = turtle.textinput('Game',
                                          'Error, name too short, please try again\n'
                                          'Name of player 2?')
            elif num_players == 1:
                name_1 = turtle.textinput('Game',
                                          'Error, name too short, please try again\n'
                                          'Name of player 1?')
                name_2 = 'Carl'
                difficulty = turtle.numinput('Game',
                                             'Bot difficulty?\n'
                                             '(warning numbers above 3 will result in a very difficult and long game)\n'
                                             '(decimal point values are allowed)')
            name_len1 = len(name_1)
            name_len2 = len(name_2)
        game_type = turtle.textinput('Game',
                                     'Play to score limit or play to time limit?\n'
                                     '(s for score limit, t for time limit)')
        while game_type != 't' and game_type != 's':
            game_type = turtle.textinput('Game',
                                         'Error, invalid input, please try again\n'
                                         'Play to score limit or play to time limit?\n'
                                         '(s for score limit, t for time limit)')
        if game_type == 's':
            score_limit = round(abs(turtle.numinput('Game',
                                                    'How many points to play to?')))
        elif game_type == 't':
            time_limit = float('{:.2f}'.format(abs(turtle.numinput('Game',
                                                                   'How long should the game last?\n'
                                                                   '(in the form of minutes.seconds)'))))
            time_limit_seconds = ((time_limit - int(time_limit)) * 100) + (int(time_limit) * 60)
            timer_text = turtle.Turtle()
            timer_text.ht()
            timer_text.penup()
            timer_text.color('white')
            timer_text.goto(0, 550)
    # displaying the number of games the players have played, and the win record of those games
    else:
        turtle.textinput('Game',
                         f'Games played: {num_games_played}\n'
                         f'Win Record: \n'
                         f'{name_1}: {player_1_wins}\n'
                         f'{name_2}: {player_2_wins}')
        if player_1_wins > player_2_wins:
            ball.dx = -5
            if y == 1:
                ball.dy = 5
            else:
                ball.dy = -5
        elif player_2_wins > player_1_wins:
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
    player_1_score = 0
    player_2_score = 0
    if num_players == 2:
        wn.listen()
        wn.onkeypress(move_up, key='W')
        wn.onkeypress(move_down, key='S')
        wn.onkeypress(move_up_2, 'Up')
        wn.onkeypress(move_down_2, 'Down')
    # for a single player game
    elif num_players == 1:
        wn.listen()
        wn.onkeypress(move_up, key='W')
        wn.onkeypress(move_down, key='S')
    # playing a first to set score match
    if game_type == 's':
        # Playing looping the pong function to play pong until 1 player reaches the score limit
        while (player_1_score < score_limit) and (player_2_score < score_limit):
            if num_players == 2:
                wn.listen()
                wn.onkeypress(move_up, key='W')
                wn.onkeypress(move_down, key='S')
                wn.onkeypress(move_up_2, 'Up')
                wn.onkeypress(move_down_2, 'Down')
            # for a single player game
            elif num_players == 1:
                wn.listen()
                wn.onkeypress(move_up, key='W')
                wn.onkeypress(move_down, key='S')
            # updating the score on the top of the scene, and player score counts
            score_boi = turtle.Turtle()
            score_boi.clear()
            score_boi.ht()
            penup()
            score_boi.color('white')
            score_boi.goto(0, 650)
            score_boi.write(f'{player_1_score} | {player_2_score}', False, 'center', ('Courier', 20, 'bold'))
            border.penup()
            border.pensize(1)
            border.color('white')
            border.setpos(0, -500)
            border.pendown()
            border.setheading(90)
            border.forward(1005)
            border.penup()
            border.color('black')
            border.pendown()
            border.forward(300)
            player_1_score_count = player_1_score
            player_2_score_count = player_2_score
            # playing pong
            while player_1_score == player_1_score_count and player_2_score == player_2_score_count:
                pong()
            score_boi.clear()
        # declaring a winner
        score_boi.write(f'{player_1_score} | {player_2_score}', False, 'center', ('Courier', 20, 'bold'))
        game_endings()
    # playing a timed match
    elif game_type == 't':
        # starting the timer
        start = time.time()
        start = float('{:.2f}'.format(start))
        end = time_limit_seconds + start
        time_remaining_seconds = int(float(end - time.time()))
        time_remaining = end - time.time()
        minutes_remaining = int(time_remaining / 60)
        seconds_remaining = int(float('{:.2f}'.format((time_remaining - (minutes_remaining * 60)))))
        while seconds_remaining + minutes_remaining > 0:
            if num_players == 2:
                wn.listen()
                wn.onkeypress(move_up, key='W')
                wn.onkeypress(move_down, key='S')
                wn.onkeypress(move_up_2, 'Up')
                wn.onkeypress(move_down_2, 'Down')
            # for a single player game
            elif num_players == 1:
                wn.listen()
                wn.onkeypress(move_up, key='W')
                wn.onkeypress(move_down, key='S')
            # updating the score on the top of the scene, and player score counts
            current_time = 0
            score_boi = turtle.Turtle()
            score_boi.ht()
            penup()
            score_boi.color('white')
            score_boi.goto(0, 650)
            score_boi.write(f'{player_1_score} | {player_2_score}', False, 'center', ('Courier', 20, 'bold'))
            border.penup()
            border.pensize(1)
            border.color('white')
            border.setpos(0, -500)
            border.pendown()
            border.setheading(90)
            border.forward(1005)
            border.penup()
            border.color('black')
            border.pendown()
            border.forward(300)
            border.penup()
            border.color('white')
            border.setpos(0, -500)
            border.pendown()
            player_1_score_count = player_1_score
            player_2_score_count = player_2_score
            # playing pong
            while player_1_score == player_1_score_count and player_2_score == player_2_score_count:
                pong()
            score_boi.clear()
        # declaring a winner
        score_boi.write(f'{player_1_score} | {player_2_score}', False, 'center', ('Courier', 20, 'bold'))
        game_endings()
turtle.exitonclick()
© 2022 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
