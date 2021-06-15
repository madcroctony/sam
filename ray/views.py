from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
# Create your views here.

class Games:
    def __init__(shelf):
        shelf.H = 8
        shelf.W = 8
       
        shelf.name = 'Number_Count'
        shelf.count = 0
        shelf.turn = 0
        shelf.who = {}

        shelf.mass_spell = '＊'
        shelf.board = [[shelf.mass_spell] * shelf.W for i in range(shelf.H)]

        shelf.black_spell ='ｂ'
        shelf.white_spell ='ｗ'

        shelf.board[4][3] = shelf.black_spell
        shelf.board[3][4] = shelf.black_spell
        shelf.board[4][4] = shelf.white_spell
        shelf.board[3][3] = shelf.white_spell

        shelf.black = 2
        shelf.white = 2

        shelf.black_box = [[3, 2], [2, 3], [5, 4], [4, 5]]

        for put in shelf.black_box:
            y = put[0]
            x = put[1]
            shelf.board[y][x] = '＋'

        shelf.white_box = [[4, 2], [5, 3], [2, 4], [3, 5]]

        shelf.params = {
        'title':shelf.name,
        'user':[],
        'board':shelf.board,
        'black':{},
        'white':{},
        'black_box':{},
        'white_box':{},
        'entry':0,
        'turn':{},
        'color':{},
        'enemy':{},
        'acount':{},
    }

    #ひっくり返す石を探す
    def search_black(shelf, user_check, enemy):
        shelf.params['black_box'][enemy] = []

        for board_height in range(shelf.H):
            for board_width in range(shelf.W):
                check = 0

                sy = board_height
                sx = board_width+1
                color_num = []
                color_check = 0

                #横右
                if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                    if sx != shelf.W:
                        while sx < shelf.W:

                            if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                color_num.append(sx)

                            elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                color_check = 1
                                break

                            else:
                                break

                            sx += 1

                if color_check == 1:
                    if color_num != []:
                        shelf.params['black_box'][enemy].append([board_height, board_width])
                        shelf.params['acount'][enemy][board_height][board_width] = '＋'
                        check = 1

                #横左
                if check == 0:
                    sy = board_height
                    sx = board_width-1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:
                        if 0 <= sx:
                            while 0 <= sx:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append(sx)

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sx -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #縦下
                if check == 0:
                    sy = board_height + 1
                    sx = board_width
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if sy < shelf.H:

                            while sy < shelf.H:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append(sy)

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy += 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1

                #縦上
                if check == 0:
                    sy = board_height - 1
                    sx = board_width
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if 0 <= sy:
                            while 0 <= sy:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append(sy)

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜め左上
                if check == 0:
                    sy = board_height - 1
                    sx = board_width - 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:
                        if 0 <= sy and 0 <=sx:

                            while 0 <= sy and 0 <= sx:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy -= 1
                                sx -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜めみぎ上
                if check == 0:
                    sy = board_height - 1
                    sx = board_width + 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if 0 <= sy and sx < shelf.W:

                            while 0 <= sy and sx < shelf.W:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy -= 1
                                sx += 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜めみぎ下
                if check == 0:
                    sy = board_height + 1
                    sx = board_width + 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if sy < shelf.H and sx < shelf.W:

                            while sy < shelf.H and sx < shelf.W:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy += 1
                                sx += 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜め左下
                if check == 0:
                    sy = board_height + 1
                    sx = board_width - 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if sy < shelf.H and 0 <= sx:
                            while sy < shelf.H and sx < shelf.W:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy += 1
                                sx -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['black_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1

        shelf.params['acount'][user_check] = shelf.params['acount'][enemy].copy()



    def search_white(shelf, user_check, enemy):
        shelf.params['white_box'][enemy] = []

        for board_height in range(shelf.H):
            for board_width in range(shelf.W):
                check = 0

                sy = board_height
                sx = board_width+1
                color_num = []
                color_check = 0

                #横右
                if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                    if sx != shelf.W:
                        while sx < shelf.W:

                            if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                color_num.append(sx)

                            elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                color_check = 1
                                break

                            else:
                                break

                            sx += 1

                if color_check == 1:
                    if color_num != []:
                        shelf.params['white_box'][enemy].append([board_height, board_width])
                        shelf.params['acount'][enemy][board_height][board_width] = '＋'
                        check = 1

                #横左
                if check == 0:
                    sy = board_height
                    sx = board_width-1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:
                        if 0 <= sx:
                            while 0 <= sx:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append(sx)

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sx -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #縦下
                if check == 0:
                    sy = board_height + 1
                    sx = board_width
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if sy < shelf.H:

                            while sy < shelf.H:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append(sy)

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy += 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1

                #縦上
                if check == 0:
                    sy = board_height - 1
                    sx = board_width
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if 0 <= sy:
                            while 0 <= sy:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append(sy)

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜め左上
                if check == 0:
                    sy = board_height - 1
                    sx = board_width - 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:
                        if 0 <= sy and 0 <=sx:

                            while 0 <= sy and 0 <= sx:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy -= 1
                                sx -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜めみぎ上
                if check == 0:
                    sy = board_height - 1
                    sx = board_width + 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if 0 <= sy and sx < shelf.W:

                            while 0 <= sy and sx < shelf.W:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy -= 1
                                sx += 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜めみぎ下
                if check == 0:
                    sy = board_height + 1
                    sx = board_width + 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if sy < shelf.H and sx < shelf.W:

                            while sy < shelf.H and sx < shelf.W:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy += 1
                                sx += 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1


                #斜め左下
                if check == 0:
                    sy = board_height + 1
                    sx = board_width - 1
                    color_num = []
                    color_check = 0

                    if shelf.params['acount'][user_check][board_height][board_width] == shelf.mass_spell:

                        if sy < shelf.H and 0 <= sx:
                            while sy < shelf.H and sx < shelf.W:
                                if shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                                    color_num.append([sy, sx])

                                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                                    color_check = 1
                                    break

                                else:
                                    break

                                sy += 1
                                sx -= 1

                    if color_check == 1:
                        if color_num != []:
                            shelf.params['white_box'][enemy].append([board_height, board_width])
                            shelf.params['acount'][enemy][board_height][board_width] = '＋'
                            check = 1

        shelf.params['acount'][user_check] = shelf.params['acount'][enemy].copy()


    #石をひっくり返す
    def check_black(shelf, user_check, enemy, board_height, board_width):

        shelf.turn_black = 0

        #横右
        sy = board_height
        sx = board_width+1
        color_num = []
        color_check = 0

        if sx < shelf.W:
            while sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append(sx)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sx += 1

        if color_check == 1:
            for x in color_num:
                shelf.params['acount'][enemy][sy][x] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1


        #横左
        sy = board_height
        sx = board_width-1
        color_num = []
        color_check = 0

        if 0 <= sx:
            while 0 <= sx:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append(sx)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sx -= 1

        if color_check == 1:
            for x in color_num:
                shelf.params['acount'][enemy][sy][x] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1


        #縦下
        sy = board_height + 1
        sx = board_width
        color_num = []
        color_check = 0

        if sy < shelf.H:
            while sy < shelf.H:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append(sy)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sy += 1

        if color_check == 1:
            for y in color_num:
                shelf.params['acount'][enemy][y][sx] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1



        #縦上
        sy = board_height - 1
        sx = board_width
        color_num = []
        color_check = 0

        if 0 <= sy:
            while 0 <= sy:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append(sy)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sy -= 1

        if color_check == 1:
            for y in color_num:
                shelf.params['acount'][enemy][y][sx] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1


        #斜め左上
        sy = board_height - 1
        sx = board_width - 1
        color_num = []
        color_check = 0

        if 0 <= sy and 0 <=sx:
            while 0 <= sy and 0 <= sx:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sy -= 1
                sx -= 1


        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1


        #斜めみぎ上
        sy = board_height - 1
        sx = board_width + 1
        color_num = []
        color_check = 0

        if 0 <= sy and sx < shelf.W:
            while 0 <= sy and sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sy -= 1
                sx += 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1


        #斜めみぎ下
        sy = board_height + 1
        sx = board_width + 1
        color_num = []
        color_check = 0

        if sy < shelf.H and sx < shelf.W:
            while sy < shelf.H and sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sy += 1
                sx += 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1


        #斜め左下
        sy = board_height + 1
        sx = board_width - 1
        color_num = []
        color_check = 0

        if sy < shelf.H and 0 <= sx:
            while sy < shelf.H and sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_check = 1
                    break

                sy += 1
                sx -= 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.black_spell

                shelf.params['black'][user_check] += 1
                shelf.params['white'][enemy] -= 1

            shelf.turn_black = 1

        shelf.params['acount'][user_check] = shelf.params['acount'][enemy].copy()


    def check_white(shelf, user_check, enemy, board_height, board_width):

        shelf.turn_white = 0

        sy = board_height
        sx = board_width+1
        color_num = []
        color_check = 0

        #横右
        if sx != shelf.W:
            while sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append(sx)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sx += 1

        if color_check == 1:
            for x in color_num:
                shelf.params['acount'][enemy][sy][x] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1

        #横左
        sy = board_height
        sx = board_width-1
        color_num = []
        color_check = 0

        if 0 <= sx:
            while 0 <= sx:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append(sx)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sx -= 1

        if color_check == 1:
            for x in color_num:
                shelf.params['acount'][enemy][sy][x] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1


        #縦下
        sy = board_height + 1
        sx = board_width
        color_num = []
        color_check = 0

        if sy < shelf.H:
            while sy < shelf.H:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append(sy)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sy += 1

        if color_check == 1:
            for y in color_num:
                shelf.params['acount'][enemy][y][sx] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1


        #縦上
        sy = board_height - 1
        sx = board_width
        color_num = []
        color_check = 0

        if 0 <= sy:
            while 0 <= sy:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append(sy)

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sy -= 1

        if color_check == 1:
            for y in color_num:
                shelf.params['acount'][enemy][y][sx] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1


        #斜め左上
        sy = board_height - 1
        sx = board_width - 1
        color_num = []
        color_check = 0

        if 0 <= sy and 0 <=sx:
            while 0 <= sy and 0 <= sx:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sy -= 1
                sx -= 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1


        #斜めみぎ上
        sy = board_height - 1
        sx = board_width + 1
        color_num = []
        color_check = 0

        if 0 <= sy and sx < shelf.W:
            while 0 <= sy and sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sy -= 1
                sx += 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1


        #斜めみぎ下
        sy = board_height + 1
        sx = board_width + 1
        color_num = []
        color_check = 0

        if sy < shelf.H and sx < shelf.W:
            while sy < shelf.H and sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sy += 1
                sx += 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1


        #斜め左下
        sy = board_height + 1
        sx = board_width - 1
        color_num = []
        color_check = 0

        if sy < shelf.H and 0 <= sx:
            while sy < shelf.H and sx < shelf.W:
                if shelf.params['acount'][user_check][sy][sx] == shelf.mass_spell:
                    break

                elif shelf.params['acount'][user_check][sy][sx] == shelf.black_spell:
                    color_num.append([sy, sx])

                elif shelf.params['acount'][user_check][sy][sx] == shelf.white_spell:
                    color_check = 1
                    break

                sy += 1
                sx -= 1

        if color_check == 1:
            for grid in color_num:
                y = grid[0]
                x = grid[1]
                shelf.params['acount'][enemy][y][x] = shelf.white_spell

                shelf.params['white'][user_check] += 1
                shelf.params['black'][enemy] -= 1

            shelf.turn_white = 1

        shelf.params['acount'][user_check] = shelf.params['acount'][enemy].copy()


    def cot(shelf, req):
        user_check = str(req.user)
        #shelf.params['user_check'] = user_check

        try:
            enemy = str(shelf.params['enemy'][user_check])

            if req.method == 'POST':

                if 'hit' in req.POST:
                    hw = str(req.POST['hit']).split('/')
                    height = int(hw[0])
                    width = int(hw[1])

                    if shelf.params['turn'][user_check] == 1:

                        if shelf.params['acount'][user_check][height][width] == '＋':

                            if shelf.params['color'][user_check] == 'black':

                                for put in shelf.params['black_box'][user_check]:
                                    y = put[0]
                                    x = put[1]
                                    shelf.params['acount'][user_check][y][x] = shelf.mass_spell
                                    shelf.params['acount'][enemy][y][x] = shelf.mass_spell


                                shelf.check_black(user_check, enemy, height, width)

                                if shelf.turn_black == 1:
                                    shelf.params['acount'][user_check][height][width] = shelf.black_spell
                                    shelf.params['acount'][enemy][height][width] = shelf.black_spell
                                    shelf.params['black'][user_check] += 1
                                    shelf.turn += 1

                                    shelf.search_white(user_check, enemy)

                                    shelf.params['turn'][user_check] = 0
                                    shelf.params['turn'][enemy] = 1

                            else:
                                for put in shelf.params['white_box'][user_check]:
                                    y = put[0]
                                    x = put[1]
                                    shelf.params['acount'][user_check][y][x] = shelf.mass_spell
                                    shelf.params['acount'][enemy][y][x] = shelf.mass_spell

                                shelf.check_white(user_check, enemy, height, width)


                                if shelf.turn_white == 1:

                                    shelf.params['acount'][user_check][height][width] = shelf.white_spell
                                    shelf.params['acount'][enemy][height][width] = shelf.white_spell

                                    shelf.params['white'][user_check] += 1
                                    shelf.turn += 1
                                    shelf.params['turn'][user_check] = 0
                                    shelf.params['turn'][enemy] = 1

                                    shelf.search_black(user_check, enemy)



                else:
                    shelf.params['none']='None'
                    return render(req, 'ray/cot.html', shelf.params)

        except:
            return render(req, 'ray/cot.html', shelf.params)

        return render(req, 'ray/cot.html', shelf.params)

    def ans(shelf, req):
        return render(req, 'ray/ans.html', shelf.params)


    def all_logout(shelf, req):
        user_check = str(req.user)
        shelf.board = [[shelf.mass_spell]*shelf.W for i in range(shelf.H)]
        shelf.board[4][3] = shelf.black_spell
        shelf.board[3][4] = shelf.black_spell
        shelf.board[4][4] = shelf.white_spell
        shelf.board[3][3] = shelf.white_spell
        shelf.black_box = [[3, 2], [2, 3], [5, 4], [4, 5]]

        for put in shelf.black_box:
            y = put[0]
            x = put[1]
            shelf.board[y][x] = '＋'

        shelf.white_box = [[4, 2], [5, 3], [2, 4], [3, 5]]

        if shelf.params['color'][user_check] == 'black':
            shelf.params['black_box'].pop(user_check)
            shelf.params['black'].pop(user_check)

        else:
            shelf.params['white_box'].pop(user_check)
            shelf.params['white'].pop(user_check)

        shelf.params['entry'] -= 1

        shelf.params['acount'][user_check] = shelf.board.copy()
        shelf.params['turn'].pop(user_check)
        shelf.params['user'].remove(user_check)

        try:
            shelf.params['enemy'].pop(user_check)

        except:
            return redirect(to='/ray/login')

        return redirect(to='/ray/login')
        return render(req, 'ray/login.html', shelf.params)


    def signup(shelf, req):
        #user_check = req.user
        shelf.params['username'] = 'ray'
        if req.method == 'POST':
            username = req.POST['username_data']
            password = req.POST['password_data']
            print('username=', username, 'password=', password)
            try:
                user = User.objects.create_user(username, '', password)
                shelf.params['username'] = 'just recomend'

            except IntegrityError:
                shelf.params['username'] = 'already'

        return render(req, 'ray/signup.html', shelf.params)

    def login(shelf, req):
        shelf.board = [[shelf.mass_spell]*shelf.W for i in range(shelf.H)]
        shelf.board[4][3] = shelf.black_spell
        shelf.board[3][4] = shelf.black_spell
        shelf.board[4][4] = shelf.white_spell
        shelf.board[3][3] = shelf.white_spell
        shelf.black_box = [[3, 2], [2, 3], [5, 4], [4, 5]]

        for put in shelf.black_box:
            y = put[0]
            x = put[1]
            shelf.board[y][x] = '＋'

        shelf.white_box = [[4, 2], [5, 3], [2, 4], [3, 5]]

        if req.method == 'POST':
            username_data = req.POST['username_data']
            password_data = req.POST['password_data']
            print('username=', username_data, 'password=', password_data)
            user = authenticate(req, username=username_data, password=password_data)

            if user is not None:
                shelf.params['user'].append(username_data)
                login(req, user)

                shelf.params['acount'][str(username_data)] = shelf.board.copy()

                if shelf.params['entry'] == 0 or shelf.params['entry'] %2 == 0:
                    shelf.params['turn'][str(username_data)] = 1
                    shelf.params['color'][str(username_data)] = 'black'
                    shelf.params['black_box'][str(username_data)] = shelf.black_box
                    shelf.params['black'][str(username_data)] = shelf.black

                else:
                    shelf.params['turn'][str(username_data)] = 0
                    shelf.params['color'][str(username_data)] = 'white'
                    shelf.params['white_box'][str(username_data)] = shelf.white_box
                    shelf.params['white'][str(username_data)] = shelf.white

                shelf.params['entry']+=1

                if shelf.params['entry'] %2 == 0:
                    entry_a = str(shelf.params['user'][shelf.params['entry']-2])
                    entry_b = str(shelf.params['user'][shelf.params['entry']-1])
                    shelf.params['enemy'][entry_a] = entry_b
                    shelf.params['enemy'][entry_b] = entry_a

                    shelf.params['acount'][entry_b] = shelf.params['acount'][entry_a].copy()

                return redirect(to='/ray/cot')

        return render(req, 'ray/login.html', shelf.params)


