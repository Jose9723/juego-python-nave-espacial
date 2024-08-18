import pygame
import random

# Inicializar Pygame http://www.sonidosmp3gratis.com/download.php?id=16927&sonido=%20agarrar%205
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Carreras con Obstáculos")

# Colores
BLACK = (0, 0, 0)
BLUE = (37, 0, 250, 98)
WHITE = (255, 255, 255)

# FPS
CLOCK = pygame.time.Clock()
FPS = 90

# Clase para el Vehículo
class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Limitar el movimiento del vehículo a la ventana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Clase para los Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((255, 0, 0))  # Color rojo para los obstáculos
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Crear instancias y grupos de sprites
vehicle = Vehicle()
all_sprites = pygame.sprite.Group()
all_sprites.add(vehicle)

obstacles = pygame.sprite.Group()

def spawn_obstacle():
    if random.random() < 0.02:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

# Función para verificar colisiones
def check_collisions():
    if pygame.sprite.spritecollideany(vehicle, obstacles):
        return True
    return False

# Función para dibujar la puntuación
score = 0

def draw_score():
    global score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    WIN.blit(text, (10, 10))

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar
    all_sprites.update()
    spawn_obstacle()

    # Verificar colisiones
    if check_collisions():
        running = False

    # Incrementar puntuación
    score += 1

    # Dibujar
    WIN.fill(BLACK)
    all_sprites.draw(WIN)
    draw_score()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
