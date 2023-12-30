import copy

import pygame
import sys
import time

tableSize = 100
steptime = 0.1


windowSize = 800
cellSize = round(windowSize / tableSize)
table = [[0] * tableSize for _ in range(tableSize)]

pygame.init()
def draw_board(screen):
    for row in range(tableSize):
        for col in range(tableSize):
            color = (255, 255, 255) if table[row][col] == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * cellSize, row * cellSize, cellSize, cellSize))

def changeTable(x, y):
    xTable = round(x / (windowSize / tableSize))
    yTable = round(y / (windowSize / tableSize))
    try: table[yTable][xTable] ^= 1
    except: print("myszka poza aplikacją")

def playStep():
    oldTable = copy.deepcopy(table)
    for linia in range(tableSize):
        for liczba in range(tableSize):
            counter = 0
            neighbors_coordinates = [
                (linia - 1, liczba - 1), (linia - 1, liczba), (linia - 1, liczba + 1),
                (linia, liczba - 1), (linia, liczba + 1),
                (linia + 1, liczba - 1), (linia + 1, liczba), (linia + 1, liczba + 1)
            ]
            for nlinia, nliczba in neighbors_coordinates:
                try:
                    if oldTable[nlinia][nliczba] == 1:
                        counter += 1
                except IndexError:
                    pass
            if table[linia][liczba] == 0 and counter == 3:
                table[linia][liczba] = 1
            elif table[linia][liczba] == 1 and (counter == 2 or counter == 3):
                table[linia][liczba] = 1
            else:
                table[linia][liczba] = 0

playing = False
mousePressed = False
def main():
    global playing
    global mousePressed
    screen = pygame.display.set_mode((windowSize, windowSize))
    pygame.display.set_caption("Game of Life")
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            #start simulation
            if keys[pygame.K_SPACE]:
                playing = not playing

            #mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePressed = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    changeTable(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEMOTION:
                if mousePressed:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    changeTable(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mousePressed = False


            #quit app
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if playing:
            playStep()
            time.sleep(steptime)

        draw_board(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()

