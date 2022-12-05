import pygame.font

class Scoreboard:
    """This class will show the score throughout the game"""
    def __init__(self, ip_game):
        self.screen = ip_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ip_game.settings

        self.text_color = (0,0,0)
        # Font type used for the word score
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.prepare_score()


    def prepare_score(self):
        """Make the score an image so it appears on the screen"""
        # This function calls the score to the screen and the position
        score_str = f" Score: {self.settings.score}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color2)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.y = 50
        self.score_rect.x = 100

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)


    # Trent Parker helped me to make a scoreboard and the parameters to run it at +10 each time a block passes
    # that the penguin can jump off of


