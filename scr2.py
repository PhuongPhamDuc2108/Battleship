import pygame
import scr1


backImage = pygame.image.load("back_arrow.png")
backImage = pygame.transform.scale(backImage, (50, 40))



def selectMode(screen):
    screen.fill([255, 255, 255])
    screen.blit(backImage, (25, 25))
    mouseClk = pygame.mouse.get_pos()
    if 15 <= mouseClk[0] < 75 and 15 <= mouseClk[1] <= 75:
        pygame.quit()
        scr1.showMainMenu()
    
    
    pygame.display.flip()
     
    
