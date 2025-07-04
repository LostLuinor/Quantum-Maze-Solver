import pygame
import time

screen = pygame.display.set_mode((500, 500))
pygame.draw.rect(screen, (0, 255, 0), (300, 400, 1, 1))
pygame.display.flip()
time.sleep(10)