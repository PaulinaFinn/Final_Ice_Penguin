import pygame

import sys
import random
from settings import Settings
from penguin import Penguin
from scoring import Scoreboard

from ground_ice import GroundIce


class IcePenguin:
    """Overall class for penguin game"""
    def __init__(self):
        pygame.init()

        # This takes from the settings class
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Name we pick to associate game
        pygame.display.set_caption('Ice Penguin')


        # Call itself
        self.penguin = Penguin(self)

        # function after every time it hits the icecube generator trigger
        self.counter = 0



        # make a ground ice block generator trigger, this will trigger the ice cubes for speed and efficiency
        self.make_groundice_trigger = 600
        # Make an empty group to hold ground ice
        self.groundice_group = pygame.sprite.Group()
        self.groundice = GroundIce(self, 10)

        # Initialize the score
        self.scoreboard = Scoreboard(self)

        # Flag to determine if the player has lost or not
        self.game_active = True

    def run_game(self):
        """Initialize the game loop"""
        # Run the main game loop if the game active flag is True
        while True:
            self._check_events()

            # Make a counter to use the % operator, which will act as our timer/ which will trigger the make icecube

            # Increment the counter by one with every pass through the while loop
            self.counter += 1
            if (self.counter % self.make_groundice_trigger) == 0:
                # After every interval of time-set by the iceblock trigger - make an iceblock with a random height
                self._make_groundice()

            # Tell the ice blocks to move
            self.groundice.update()
            self.groundice_group.update()

            # Update the penguin
            self.penguin.update(self.groundice_group)

            # Check if the penguin collided with ice; if it does, set game loop flag to false
            if self.penguin.penguin_ice_collision:
                self.game_active = False
                self._end_game()


            self._update_screen()

    def _end_game(self):
        """Make a loop to run that will make an end game screen"""
        while True:
            self._check_events()
            self._update_screen()


    def _make_groundice(self):
        """Make an instance for the ice block each time it is being called."""
        #Random y position for the ice blocks
        y_pos = random.randint(0, 400)
        # Pick a random height to place a block of ice
        new_groundice = GroundIce(self, y_pos)
        # This will add more iceblocks to the group that's already made
        self.groundice_group.add(new_groundice)
        # Put the score on the screen and make it add by 10
        self.settings.score +=10
        self.scoreboard.prepare_score()


    def _check_events(self):
        """Respond to key presses and mouse events."""
        # This is all the key presses that control the movements of the game, the space bar will have the
        # penguin jump
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Necessary so the penguin will come up rather than stay down when the down key is pressed!
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Using the down key, the penguin will rotate down
        if event.key == pygame.K_UP:
            self.penguin.rotate_left = True
        elif event.key == pygame.K_DOWN:
            self.penguin.rotate_right = True
        elif event.key == pygame.K_SPACE:
            self.penguin.gravity_active = False
            self.penguin.jumping_up = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.penguin.rotate_left = False
        elif event.key == pygame.K_DOWN:
            self.penguin.rotate_right = False
        elif event.key == pygame.K_SPACE:
            self.penguin.gravity_active = True
            self.penguin.jumping_up = False


    def _update_screen(self):
        """update the images"""
        # Add in the penguin & redraw the screen each loop
        # [Trent Parker] helped me split by background on the screen
        self.screen.fill(self.settings.bg_color, pygame.Rect(0,0,1200,500))
        self.screen.fill(self.settings.bg_color2, pygame.Rect(0,425,1200,300))
        self.penguin.blitme()
        # So this references the ice blocks that are being drawn and updates them to the screen
        # Draw the ground ice
        self.groundice_group.draw(self.screen)
        # draw everything in our self.ground_ice_group using self.ground_ice_group.draw(self.scree)
        # Make the most recent screen visible
        if not self.game_active:
            # This loads the image of the end game when a collision occurs and the game is over
            self.endgame_image = pygame.image.load("images/end.png")
            self.engame_image = pygame.transform.scale(self.endgame_image, (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(self.endgame_image, (0, 0))

        # This will display the score on the screen to the most recent screen
        self.scoreboard.show_score()
        pygame.display.update()
        pygame.display.flip()


if __name__=='__main__':
    ip = IcePenguin()
    ip.run_game()

    # Ryan Schumman helped a lot with this class by helping me get the keypresses to actually respond to the space
    # he as well helped me in the overall aspect of the game by getting little components throughout the screen

