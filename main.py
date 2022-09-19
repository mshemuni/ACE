import random
import pygame
from v3d import Point, Vector


class Ship:
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Ship class
        :param screen: Screen where the ship will be drawn
        """
        self.screen = screen
        self.pos = Vector()
        self.imp = pygame.image.load("assets/ship.png").convert_alpha()
        self.imp = pygame.transform.scale(self.imp, (55, 75))
        self.health = 100

    def update_pos(self) -> None:
        """
        Updates the position of the ship with position of the mouse
        """
        x, y = pygame.mouse.get_pos()
        self.pos = Vector(Point(x - 55 / 2, y - 75 / 2))

    def show(self) -> None:
        """
        Shows the ship on the position
        """
        self.screen.blit(self.imp, (self.pos.point.x, self.pos.point.y))


class Ray:
    def __init__(self, screen: pygame.Surface, pos: Vector) -> None:
        """
        Ray (Bullet) Class
        :param screen: Screen where the ray will be drawn
        :param pos: The initial position of the bullet
        """
        self.screen = screen
        self.pos = pos
        self.vel = Vector(Point(0, -15, 0))
        self.color = (0, 255, 255)

    def move(self) -> None:
        """
        Moves the bullet by `self.vel` value
        """
        self.pos += self.vel

    def show(self) -> None:
        """
        Draws a ray (2 lines)
        """
        pygame.draw.line(
            self.screen, self.color,
            (self.pos.point.x + 55 / 2 - 0.5, self.pos.point.y),
            (self.pos.point.x + 55 / 2 - 0.5, self.pos.point.y - 25)
        )

        pygame.draw.line(
            self.screen, self.color,
            (self.pos.point.x + 55 / 2 + 0.5, self.pos.point.y),
            (self.pos.point.x + 55 / 2 + 0.5, self.pos.point.y - 25)
        )

    def is_gone(self) -> bool:
        """
        Checks if the ray is out of the window
        :return: True if the ray is outside the canvas, False otherwise
        """
        return self.pos.point.y < 0


class EnemyRay(Ray):
    def __init__(self, screen : pygame.Surface, pos: Vector) -> None:
        """
        Enemy Ray Class
        Same as Ray class with small different

        :param screen: Screen where the enemy_ray will be drawn
        :param pos: The initial position of the bullet
        """
        super().__init__(screen, pos)
        self.vel = Vector(Point(0, 15, 0))
        self.color = (255, 255, 0)

    def is_gone(self) -> bool:
        """
        Override the parent `is_gone` method. Because this ray moves on opposite direction
        :return:
        """
        return self.pos.point.y > WIDTH

    def hit(self, ship: Ship) -> None:
        """
        Checks if the current enemy_ray hits the ship
        :param ship: The ship
        """
        if ship.pos.point.dist(self.pos.point) < 20:
            ship.health -= 10
            self.pos.point.y = HEIGHT + 10


class Enemy:
    def __init__(self, screen: pygame.Surface) -> None:
        """
        Enemy Class

        :param screen: Screen where the enemy will be drawn
        """
        self.screen = screen
        self.pos: Vector = Vector(Point(random.randint(57, WIDTH - 57), -35, 0))
        self.vel: Vector = Vector(Point(random.randint(2, 4), random.randint(5, 15)))
        self.imp = pygame.image.load("assets/enemy.png").convert_alpha()
        self.imp = pygame.transform.scale(self.imp, (57, 35))

    def move(self) -> None:
        """
        Moves the enemy by `self.vel`
        """
        self.bounce()
        self.pos += self.vel

    def show(self) -> None:
        """
        Shows the enemy on the given position
        """
        self.screen.blit(self.imp, (self.pos.point.x, self.pos.point.y))

    def bounce(self) -> None:
        """
        Bounces the enemy if it hit a vertical wall
        """
        if not 57 < self.pos.point.x < WIDTH - 57:
            self.vel.point.x *= -1

    def kill(self, rays: list[Ray]) -> bool:
        """
        Checks if any ray hits the enemy.
        :param rays: list of rays to be checked
        :return: True if hit occurs, False otherwise
        """
        for ray in rays:
            if ray.pos.point.dist(self.pos.point) < 30:
                ray.pos.point.y = -10
                return True

    def is_gone(self) -> bool:
        """
        Checks if this enemy is out of the canvas
        :return: True if enemy is outside the canvas, False otherwise
        """
        return self.pos.point.y > HEIGHT

    def hit(self, ship: Ship) -> bool:
        """
        Checks if an enemy collided with the ship
        :param ship: The ship
        :return: True if collision happens, False otherwise
        """
        return ship.pos.point.dist(self.pos.point) < 70


WIDTH = 500
HEIGHT = 750
FPS = 25
BLACK = (52, 52, 52)

if __name__ == '__main__':
    # Keep the score
    SCORE = 0

    # Initialise the pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space")
    clock = pygame.time.Clock()

    running = True
    # To stop drawing
    draw = True

    ship = Ship(screen)
    rays = []
    enemies = []
    enemy_rays = []

    # Main loop
    while running:
        # Check if want to draw
        if draw:
            # Randomly generate enemies
            if random.randint(0, 100) < 5:
                enemies.append(Enemy(screen))

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Create a Ray object upon a click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        rays.append(Ray(screen, ship.pos))

            screen.fill(BLACK)
            # Draw ship
            ship.update_pos()
            ship.show()

            # Check if health is 0.
            if ship.health == 0:
                draw = False
                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(f'Looser', False, (255, 0, 0))
                screen.blit(text_surface, (250, 250))

            # Draw rays
            for i in range(len(rays) - 1, -1, -1):
                rays[i].move()
                rays[i].show()
                if rays[i].is_gone():
                    del rays[i]

            # Draw enemies
            for i in range(len(enemies) - 1, -1, -1):
                # Randomly generate enemy_ray. As if an enemy shot a ray
                if random.randint(0, 100) < 5:
                    enemy_rays.append(EnemyRay(screen, enemies[i].pos))

                enemies[i].move()
                enemies[i].show()

                # Check if enemy collided with the ship and stop the drawing
                if enemies[i].hit(ship):
                    draw = False
                    my_font = pygame.font.SysFont('Comic Sans MS', 30)
                    text_surface = my_font.render(f'Looser', False, (255, 0, 0))
                    screen.blit(text_surface, (250, 250))

                # Check if an enemy got shot and remove it
                if enemies[i].kill(rays):
                    SCORE += 5
                    del enemies[i]

                # Check if an enemy escaped (ran out of the screen) and decrease the score
                elif enemies[i].is_gone():
                    SCORE -= 1
                    del enemies[i]

            # Draw enemy_ray
            for i in range(len(enemy_rays) - 1, -1, -1):
                enemy_rays[i].move()
                enemy_rays[i].show()
                enemy_rays[i].hit(ship)

            # Draw score
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'Score: {SCORE}', False, (0, 255, 0))
            screen.blit(text_surface, (0, 0))

            pygame.display.flip()

    pygame.quit()
