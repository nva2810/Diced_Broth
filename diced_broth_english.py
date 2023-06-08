import random
from termcolor import colored
# ctypes for cmd (windows)
import ctypes


def rules():
    while True:
        game_rules = input(f'''Do you want to learn the rules of the game?
    {colored('("yes" or "no"): ', 'green')}''')
        if game_rules == 'yes':
            print(f'''\nThis is a match-3 game! 
You need to collect a combination of identical cubes. 
Points are awarded for each cube. There are also bonuses.
{colored('2 cubes', 'red')} = 200 points. 
{colored('3 cubes', 'red')} = 300 points.
{colored('4 cubes', 'red')} = 500 points and a bonus 'destroy row or column'.
{colored('(bonus activation = 600 points)', 'yellow')}
{colored('5 cubes', 'red')} = 700 points and a bonus 'dynamite'. 
{colored('(bonus activation = 1500 points)', 'yellow')}
{colored('6 cubes and more', 'red')} = 2x points per cube and a bonus 'color destruction'.
{colored('(bonus activation = 2x points per cube)', 'yellow')}
The game ends if you run out of steps, or you have completed the goal. 
{colored('Have a nice game and win!', 'green')}\n''')
            game()
        elif game_rules == 'no':
            print('\nEnter the coordinates first horizontally, then vertically.\n')
            game()
        else:
            print('Invalid data. Please try again!\n')


def restart():
    while True:
        play_again = input(f'''\nDo you want to play again? 
        {colored('("yes" or "no"): ', 'green')}''')
        if play_again == 'yes':
            global a, b, counter, step, figure
            a, b = list(), random.choice(shape)
            counter, step, figure = 0, 20, 30
            for _ in range(36):
                a.append(random.choice(shape))
            game()
        elif play_again == 'no':
            print('Okay. Goodbye!')
            print(input(f"\n{colored('Press Enter to finish...', 'red')}"))
            quit()
        else:
            print('Invalid data. Please try again!\n')


def area():
    print(f'''
      Goal: {b} x {figure}    Score: {counter}
      Steps: {step}       Record: {record} 

6 {outline[0]} {outline[2].join(a[0:6])} {outline[1]}

5 {outline[0]} {outline[2].join(a[6:12])} {outline[1]}

4 {outline[0]} {outline[2].join(a[12:18])} {outline[1]}

3 {outline[0]} {outline[2].join(a[18:24])} {outline[1]}

2 {outline[0]} {outline[2].join(a[24:30])} {outline[1]}

1 {outline[0]} {outline[2].join(a[30:36])} {outline[1]}
    1     2     3     4     5     6 ''')


def game():
    def direction():
        up = index - 6
        while True:
            if 0 <= up < 36 and a[up] == pin:
                a[up] = ' '
                a[index] = ' '
                up -= 6
            else:
                break

        down = index + 6
        while True:
            if 0 <= down < 36 and a[down] == pin:
                a[down] = ' '
                a[index] = ' '
                down += 6
            else:
                break

        left = index - 1
        while True:
            if 0 <= left < 36 and left != 5 and left != 11 and left != 17 \
                    and left != 23 and left != 29 and left != 35 \
                    and a[left] == pin:
                a[left] = ' '
                a[index] = ' '
                left -= 1
            else:
                break

        right = index + 1
        while True:
            if right < 36 and right != 0 and right != 6 and right != 12 \
                    and right != 18 and right != 24 and right != 30 \
                    and a[right] == pin:
                a[right] = ' '
                a[index] = ' '
                right += 1
            else:
                break

    def cycle():
        for i in range(36):

            one = i - 6
            if 0 <= one < 36 and a[i] == ' ' and a[one] == pin:
                a[one] = ' '

            two = i + 6
            if 0 <= two < 36 and a[i] == ' ' and a[two] == pin:
                a[two] = ' '

            three = i - 1
            if a[i] == ' ' and a[three] == pin and i != 0 and i != 6 \
                    and i != 12 and i != 18 and i != 24 and i != 30:
                a[three] = ' '

            four = i + 1
            if four < 36 and a[i] == ' ' and a[four] == pin and \
                    i != 5 and i != 11 and i != 17 and i != 23 \
                    and i != 29 and i != 35:
                a[four] = ' '

    def space():
        for k in range(6):
            for _ in range(6):
                if a[30 + k] == ' ':
                    a[30 + k], a[24 + k] = a[24 + k], a[30 + k]
                if a[24 + k] == ' ':
                    a[24 + k], a[18 + k] = a[18 + k], a[24 + k]
                if a[18 + k] == ' ':
                    a[18 + k], a[12 + k] = a[12 + k], a[18 + k]
                if a[12 + k] == ' ':
                    a[12 + k], a[6 + k] = a[6 + k], a[12 + k]
                if a[6 + k] == ' ':
                    a[6 + k], a[0 + k] = a[0 + k], a[6 + k]

    def bonuses():
        def left_right():
            global counter
            global figure
            bonus_left = index - 1
            while True:
                if bonus_left != 5 and bonus_left != 11 and bonus_left != 17\
                        and bonus_left != 23 and bonus_left != 29 \
                        and bonus_left != 35:
                    if a[bonus_left] == b:
                        figure -= 1
                    a[bonus_left] = ' '
                    a[index] = ' '
                    bonus_left -= 1
                else:
                    break

            bonus_right = index + 1
            while True:
                if bonus_right < 36 and bonus_right != 0 and \
                        bonus_right != 6 and bonus_right != 12\
                        and bonus_right != 18 and bonus_right != 24 \
                        and bonus_right != 30:
                    if a[bonus_right] == b:
                        figure -= 1
                    a[bonus_right] = ' '
                    a[index] = ' '
                    bonus_right += 1
                else:
                    break
            counter += 100 * a.count(' ')

        def up_down():
            global counter
            global figure
            bonus_up = index - 6
            while True:
                if 0 <= bonus_up < 36:
                    if a[bonus_up] == b:
                        figure -= 1
                    a[bonus_up] = ' '
                    a[index] = ' '
                    bonus_up -= 6
                else:
                    break

            bonus_down = index + 6
            while True:
                if 0 <= bonus_down < 36:
                    if a[bonus_down] == b:
                        figure -= 1
                    a[bonus_down] = ' '
                    a[index] = ' '
                    bonus_down += 6
                else:
                    break
            counter += 100 * a.count(' ')

        def tnt():
            global counter
            global figure
            a[index] = ' '
            if index == 0:
                for i in [1, 6, 7]:
                    if a[index + i] == b:
                        figure -= 1
                a[index + 1], a[index + 6], a[index + 7] = ' ', ' ', ' '
            elif index == 5:
                if a[index - 1] == b:
                    figure -= 1
                for i in [5, 6]:
                    if a[index + i] == b:
                        figure -= 1
                a[index - 1], a[index + 5], a[index + 6] = ' ', ' ', ' '
            elif index == 30:
                for i in [5, 6]:
                    if a[index - i] == b:
                        figure -= 1
                if a[index + 1] == b:
                    figure -= 1
                a[index - 6], a[index - 5], a[index + 1] = ' ', ' ', ' '
            elif index == 35:
                for i in [1, 6, 7]:
                    if a[index - i] == b:
                        figure -= 1
                a[index - 1], a[index - 6], a[index - 7] = ' ', ' ', ' '
            elif (index != 0 or index != 30) and index % 6 == 0:
                for i in [5, 6]:
                    if a[index - i] == b:
                        figure -= 1
                for i in [1, 6, 7]:
                    if a[index + i] == b:
                        figure -= 1
                a[index - 6], a[index - 5], a[index + 1] = ' ', ' ', ' '
                a[index + 6], a[index + 7] = ' ', ' '
            elif (index != 5 or index != 35) and (index + 1) % 6 == 0:
                for i in [1, 6, 7]:
                    if a[index - i] == b:
                        figure -= 1
                for i in [5, 6]:
                    if a[index + i] == b:
                        figure -= 1
                a[index - 6], a[index - 7], a[index - 1] = ' ', ' ', ' '
                a[index + 6], a[index + 5] = ' ', ' '
            elif 0 < index < 5:
                if a[index - 1] == b:
                    figure -= 1
                for i in [1, 5, 6, 7]:
                    if a[index + i] == b:
                        figure -= 1
                a[index - 1], a[index + 1], a[index + 5] = ' ', ' ', ' '
                a[index + 6], a[index + 7] = ' ', ' '
            elif 30 < index < 35:
                if a[index + 1] == b:
                    figure -= 1
                for i in [1, 5, 6, 7]:
                    if a[index - i] == b:
                        figure -= 1
                a[index - 1], a[index + 1], a[index - 5] = ' ', ' ', ' '
                a[index - 6], a[index - 7] = ' ', ' '
            else:
                for i in [1, 5, 6, 7]:
                    if a[index - i] == b:
                        figure -= 1
                    if a[index + i] == b:
                        figure -= 1
                a[index - 6], a[index + 6] = ' ', ' '
                a[index - 1], a[index + 1] = ' ', ' '
                a[index - 7], a[index + 7] = ' ', ' '
                a[index - 5], a[index + 5] = ' ', ' '
            counter += 1500

        def delete_color():
            global counter
            global figure
            if a[index] == color[0]:
                for x in range(36):
                    if a[x] == shape[0]:
                        if a[x] == b:
                            figure -= 1
                        a[x] = ' '
            elif a[index] == color[1]:
                for x in range(36):
                    if a[x] == shape[1]:
                        if a[x] == b:
                            figure -= 1
                        a[x] = ' '
            elif a[index] == color[2]:
                for x in range(36):
                    if a[x] == shape[2]:
                        if a[x] == b:
                            figure -= 1
                        a[x] = ' '
            elif a[index] == color[3]:
                for x in range(36):
                    if a[x] == shape[3]:
                        if a[x] == b:
                            figure -= 1
                        a[x] = ' '
            a[index] = ' '
            counter += 100 * (a.count(' ') * 2)

        global counter
        # bonus includes 'left-right', 'up-down', 'TNT', 'delete color'
        bonus = ['<', '^', '0']
        # color includes the same color of the square
        color = [colored('X', 'red'), colored('X', 'green'),
                 colored('X', 'blue'), colored('X', 'yellow')]
        if a[index] == bonus[0]:
            left_right()
        elif a[index] == bonus[1]:
            up_down()
        elif a[index] == bonus[2]:
            tnt()
        elif a[index] in color:
            delete_color()
        elif a.count(' ') < 4:
            counter += 100 * a.count(' ')
        elif a.count(' ') == 4:
            a[index] = random.choice(bonus[0:2])
            counter += 500
        elif a.count(' ') == 5:
            a[index] = bonus[2]
            counter += 700
        elif a.count(' ') >= 6:
            counter += 100 * (a.count(' ') * 2)
            if pin == shape[0]:
                a[index] = color[0]
            elif pin == shape[1]:
                a[index] = color[1]
            elif pin == shape[2]:
                a[index] = color[2]
            elif pin == shape[3]:
                a[index] = color[3]

    global figure, step, counter, record
    while True:
        area()
        n = input('\nEnter the coordinates: ').split()
        if ''.join(n).isdigit() and len(n) == 2 and \
                0 < int(n[0]) < 7 and 0 < int(n[1]) < 7:
            index = (int(n[0]) - 1) + (36 - (6 * int(n[1])))
            pin = a[index]
            direction()
            for _ in range(36):
                cycle()
            if pin == b:
                figure -= a.count(' ')
            bonuses()
            space()
            for ran in range(36):
                if a[ran] == ' ':
                    a[ran] = random.choice(shape)
            step -= 1

            if step == 0:
                area()
                print("\nOh, no... You've run out of steps!")
                break
            elif figure <= 0:
                figure = 0
                area()
                print("\nCongratulations! You've reached your goal!")
                break
        else:
            print('You should enter two numbers from 1 to 6!')
    if counter > record:
        record = counter
        print(f'Your new high score is {record} points!')
    restart()


# two lines below for cmd (windows)
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
# shape includes a circle, a triangle, a rhombus, a square
# shape = [colored('\u25CF', 'red'), colored('\u25B2', 'green'),
# colored('\u25C6', 'blue'), colored('\u25A0', 'yellow'),
# colored('X', 'white')]
shape = [colored('\u25A0', 'red'), colored('\u25A0', 'green'),
         colored('\u25A0', 'blue'), colored('\u25A0', 'yellow')]
outline = [colored('{', 'cyan'),
           colored('}', 'cyan'),
           colored(' } { ', 'cyan')]
a, b = list(), random.choice(shape)
counter, record, step, figure = 0, 0, 20, 30
for _ in range(36):
    a.append(random.choice(shape))
print(f'''-----------------------
{colored('DICED BROTH', 'red')} | (match-3)
-----------------------
            {colored('v1.0 by NVA', 'yellow')}\n''')
rules()
