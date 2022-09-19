import random
import pygame
from v3d import Point, Vector


class Ship:
    def __init__(self, screen):
        self.screen = screen
        self.pos = Vector()
        self.imp = pygame.image.load("assets/ship.png").convert_alpha()
        self.imp = pygame.transform.scale(self.imp, (55, 75))
        self.health = 100

    def update_pos(self):
        x, y = pygame.mouse.get_pos()
        self.pos = Vector(Point(x - 55 / 2, y - 75 / 2))

    def show(self):
        self.screen.blit(self.imp, (self.pos.point.x, self.pos.point.y))


class Ray:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.vel = Vector(Point(0, -15, 0))
        self.color = (0, 255, 255)

    def move(self):
        self.pos += self.vel

    def show(self):
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

    def is_gone(self):
        return self.pos.point.y < 0


class EnemyRay(Ray):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.vel = Vector(Point(0, 15, 0))
        self.color = (255, 255, 0)

    def is_gone(self):
        return self.pos.point.y > WIDTH

    def hit(self, ship):
        if ship.pos.point.dist(self.pos.point) < 20:
            ship.health -= 10
            self.pos.point.y = HEIGHT + 10


class Enemy:
    def __init__(self, screen):
        self.screen = screen
        self.pos: Vector = Vector(Point(random.randint(57, WIDTH - 57), -35, 0))
        self.vel: Vector = Vector(Point(random.randint(2, 4), random.randint(5, 15)))
        self.imp = pygame.image.load("assets/enemy.png").convert_alpha()
        self.imp = pygame.transform.scale(self.imp, (57, 35))

    def move(self):
        self.bounce()
        self.pos += self.vel

    def show(self):
        self.screen.blit(self.imp, (self.pos.point.x, self.pos.point.y))

    def bounce(self):
        if not 57 < self.pos.point.x < WIDTH - 57:
            self.vel.point.x *= -1

    def kill(self, rays: list[Ray]):
        for ray in rays:
            if ray.pos.point.dist(self.pos.point) < 30:
                ray.pos.point.y = -10
                return True

    def is_gone(self):
        return self.pos.point.y > HEIGHT

    def hit(self, ship):
        return ship.pos.point.dist(self.pos.point) < 70


WIDTH = 500
HEIGHT = 750
FPS = 25
BLACK = (52, 52, 52)

if __name__ == '__main__':
    SCORE = 0

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space")
    clock = pygame.time.Clock()

    running = True
    draw = True

    ship = Ship(screen)
    rays = []
    enemies = []
    enemy_rays = []

    while running:
        if draw:
            if random.randint(0, 100) < 5:
                enemies.append(Enemy(screen))

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        rays.append(Ray(screen, ship.pos))

            screen.fill(BLACK)
            ship.update_pos()
            ship.show()

            if ship.health == 0:
                draw = False
                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(f'Looser', False, (255, 0, 0))
                screen.blit(text_surface, (250, 250))

            for i in range(len(rays) - 1, -1, -1):
                rays[i].move()
                rays[i].show()
                if rays[i].is_gone():
                    del rays[i]

            for i in range(len(enemies) - 1, -1, -1):
                if random.randint(0, 100) < 5:
                    enemy_rays.append(EnemyRay(screen, enemies[i].pos))
                enemies[i].move()
                enemies[i].show()
                if enemies[i].hit(ship):
                    draw = False
                    my_font = pygame.font.SysFont('Comic Sans MS', 30)
                    text_surface = my_font.render(f'Looser', False, (255, 0, 0))
                    screen.blit(text_surface, (250, 250))

                if enemies[i].kill(rays):
                    SCORE += 5
                    del enemies[i]
                elif enemies[i].is_gone():
                    SCORE -= 1
                    del enemies[i]

            for i in range(len(enemy_rays) - 1, -1, -1):
                enemy_rays[i].move()
                enemy_rays[i].show()
                enemy_rays[i].hit(ship)

            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'Score: {SCORE}', False, (0, 255, 0))
            screen.blit(text_surface, (0, 0))

            pygame.display.flip()

    pygame.quit()
