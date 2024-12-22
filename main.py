import pygame
from AI import GeneticAI
import c
from classes import Flappy, Bird

pygame.init()
pygame.font.init()

running = True

clock = pygame.time.Clock()
dt = clock.tick(60)

screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Flappy Bird")

FLA = Flappy(screen)
GAI = GeneticAI(FLA)

FLA.birds = GAI.return_birds()

while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1):
                GAI.check_generation(force=1)
                FLA.reset_game()
                FLA.birds = GAI.return_birds()
                
                                       
    screen.fill(c.BACKGROUND_COLOUR) 
    GAI.move_AI(dt)
    if GAI.check_generation():
        FLA.reset_game()
        FLA.birds = GAI.return_birds()

    if FLA.cur_score >= 5:
        GAI.check_generation(force=1)
        FLA.reset_game()
        FLA.birds = GAI.return_birds()

    FLA.move_sprites(dt)
    FLA.draw_sprites()

    pygame.display.flip()

pygame.quit()