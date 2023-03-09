import pygame as pg
from settings import Settings
from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
from button import Button
from game_stats import GameStats
from home import Home
import sys 


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="spaceInvaders_start/sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.settings.initialize_speed_settings()

        self.play_button = Button(self.screen, "Play")
        self.stats = GameStats(self)
        self.space_text = Home(self.screen, "SPACE", 8, 1)
        self.invaders_text = Home(self.screen, "INVADERS", 5, 2)

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT: self.game_over()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)


    def check_play_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_speed_settings()

            pg.mouse.set_visible(False)

            self.stats.reset_stats()
            self.stats.game_active = True

            self.scoreboard.prep_score()
            # self.scoreboard.prep_high_score()
            # self.scoreboard.prep_level()
            # self.scoreboard.prep_ships()

            self.aliens.aliens.empty()
            self.alien_lasers.lasers.empty()

            self.aliens.create_fleet()
            self.ship.center_ship()
            print("HI")

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()    # handled by ship for ship_lasers and by aliens for alien_lasers
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:     
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            self.update_screen()

            if self.stats.game_active:
                self.ship.update()
                self.aliens.update()
                self.barriers.update()
                # self.lasers.update()    # handled by ship for ship_lasers and by alien for alien_lasers
                self.scoreboard.update()
            pg.display.flip()

    def update_screen(self):

        self.scoreboard.draw()

        if not self.stats.game_active:
            self.space_text.draw_button()
            self.invaders_text.draw_button()
            self.play_button.draw_button()


def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()