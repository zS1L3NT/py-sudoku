import time
import pygame
from pygame import Surface

sqcoor = [28, 79, 130, 182, 232, 283, 335, 386, 437]
linecoor = [1, 53, 104, 155, 207, 258, 309, 361, 412, 465]
linethick = [3, 1, 1, 2, 1, 1, 2, 1, 1, 3]
black = (0, 0, 0)


def good_board():
    good_board = [
        [0, 0, 4, 0, 5, 0, 0, 0, 0],
        [9, 0, 0, 7, 3, 4, 6, 0, 2],
        [0, 0, 3, 6, 2, 1, 0, 4, 9],
        [0, 3, 5, 0, 9, 7, 4, 8, 0],
        [8, 9, 0, 5, 0, 0, 7, 3, 0],
        [0, 7, 6, 0, 1, 8, 9, 2, 0],
        [3, 1, 0, 9, 7, 0, 2, 6, 0],
        [0, 0, 9, 1, 8, 2, 5, 0, 3],
        [0, 2, 0, 0, 6, 0, 1, 0, 0]
    ]
    return good_board


def bad_board():
    bad_board = [
        [7, 7, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    return bad_board


def empty_board():
    empty_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    return empty_board


def valid(bo: list[list[int]], num: int, pos: tuple[int]):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def dump(bo: list[list[int]]):
    print()
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")
    print()
    return True


def find_empty(bo: list[list[int]]):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None


def echo(pygame: pygame, wn: Surface, text: str, pos: tuple[int], color=(0, 0, 0), bgcolor=(255, 255, 255), size=46):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color, bgcolor)
    textRect = text.get_rect()
    textRect.center = pos
    wn.blit(text, textRect)
    pygame.display.update()


def init_lines(pygame: pygame, wn: Surface):
    # Across Lines
    for i in range(len(linecoor)):
        pygame.draw.line(
            wn, black, (0, linecoor[i]), (466, linecoor[i]), linethick[i])
    # Down lines
    for i in range(len(linecoor)):
        pygame.draw.line(
            wn, black, (linecoor[i], 0), (linecoor[i], 466), linethick[i])


def init_numbers(pygame: pygame, wn: Surface, bo: list[list[int]]):
    for i in range(0, 9):  # row
        for j in range(0, 9):  # col
            if bo[j][i] != 0:
                echo(pygame, wn, str(bo[j][i]),
                     (sqcoor[i], sqcoor[j]), color=(0, 0, 0))
            else:
                echo(pygame, wn, "  ", (sqcoor[i], sqcoor[j]))
    return True


def gui_print(pygame: pygame, wn: Surface, bo: list[list[int]], index: int):
    if index == 0:
        const = good_board()
    if index == 1:
        const = bad_board()
    if index == 2:
        const = empty_board()

    for i in range(0, 9):  # row
        for j in range(0, 9):  # col
            if bo[j][i] == 0:
                echo(pygame, wn, "  ", (sqcoor[i], sqcoor[j]))
            elif bo[j][i] == const[j][i]:
                continue
            elif bo[j][i] != 0:
                echo(pygame, wn, str(
                    bo[j][i]), (sqcoor[i], sqcoor[j]), color=(150, 150, 150))
    return True


def solve(pygame: pygame, wn: Surface, bo: list[list[int]], fast: bool, startTime: float, index: int):
    if not fast:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return '0'
        echo(pygame, wn, 'Time: '+str(round(time.time()-startTime)) +
             's', (385, 493), size=40)
    find = find_empty(bo)
    if not find:
        gui_print(pygame, wn, bo, index)
        for i in range(0, 9):
            for j in range(0, 9):
                if not valid(bo, bo[i][j], (i, j)):
                    return False
        return True
    else:
        if not fast:
            gui_print(pygame, wn, bo, index)
        row, col = find
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(pygame, wn, bo, fast, startTime, index):
                return True
            bo[row][col] = 0
            if not fast:
                gui_print(pygame, wn, bo, index)
    return False


def loop(fast=False, index=0):
    pygame.init()
    if index == 0:
        board = good_board()
    if index == 1:
        board = bad_board()
    if index == 2:
        board = empty_board()

    wn: Surface = pygame.display.set_mode((466, 519))
    pygame.display.set_caption("Sudoku")

    running = True
    wn.fill((255, 255, 255))
    init_lines(pygame, wn)
    init_numbers(pygame, wn, board)
    while running:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startTime = time.time()
                    echo(pygame, wn, 'Solving...', (115, 493), color=(
                        200, 200, 200), bgcolor=(225, 160, 0), size=75)
                    if solve(pygame, wn, board, fast, startTime, index):
                        echo(pygame, wn, '                 ', (119, 493),
                             color=(0, 0, 0), bgcolor=(255, 255, 255), size=75)
                        echo(pygame, wn, ' Done ', (77, 493), color=(
                            200, 200, 200), bgcolor=(0, 255, 0), size=75)
                    else:
                        init_numbers(pygame, wn, board)
                        echo(pygame, wn, '                 ', (119, 493),
                             color=(0, 0, 0), bgcolor=(255, 255, 255), size=75)
                        echo(pygame, wn, 'No solutions', (158, 493), color=(
                            200, 200, 200), bgcolor=(255, 0, 0), size=75)

        pygame.display.update()

    pygame.quit()


loop(fast=True, index=0)
