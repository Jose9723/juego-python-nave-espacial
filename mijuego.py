import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Carreras con Obstáculos")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (117, 0, 250)
RED = (255, 0, 0)

# FPS
CLOCK = pygame.time.Clock()
FPS = 60

# Cargar imágenes
vehicle_image = pygame.image.load('nave.webp')  # Asegúrate de tener esta imagen
obstacle_image = pygame.image.load('roca.webp')  # Asegúrate de tener esta imagen
ammo_image = pygame.image.load('municion.webp')  # Asegúrate de tener esta imagen
background_image = pygame.image.load('fondo.jpg')  # Asegúrate de tener esta imagen

# Redimensionar imágenes
vehicle_image = pygame.transform.scale(vehicle_image, (100, 60))
obstacle_image = pygame.transform.scale(obstacle_image, (80, 50))
ammo_image = pygame.transform.scale(ammo_image, (50, 50))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Cargar sonidos
pygame.mixer.init()
pygame.mixer.music.load('fondo.mp3')  # Música de fondo
collision_obstacle_sound = pygame.mixer.Sound('choque.mp3')  # Sonido al chocar con un obstáculo
pickup_ammo_sound = pygame.mixer.Sound('municion.mp3')  # Sonido al recoger munición
shooting_sound = pygame.mixer.Sound('disparo.mp3')  # Sonido al disparar

# Clase para el Vehículo
class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = vehicle_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = 8
        self.bullets = pygame.sprite.Group()  # Grupo para las balas
        self.max_bullets = 10  # Número máximo de disparos
        self.current_bullets = self.max_bullets  # Contador de disparos restantes

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

    def shoot(self):
        if self.current_bullets > 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            self.bullets.add(bullet)
            self.current_bullets -= 1  # Disminuir el número de disparos restantes
            shooting_sound.play()  # Reproducir sonido al disparar

    def reload(self):
        # Recargar solo 5 balas, no hasta el máximo
        self.current_bullets += 5
        if self.current_bullets > self.max_bullets:
            self.current_bullets = self.max_bullets  # No superar el máximo de balas

# Clase para los Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Clase para las Balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Clase para la Munición
class Ammo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ammo_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Función para reiniciar el juego
def reset_game():
    global score
    global vehicle
    global all_sprites
    global obstacles
    global ammo_items

    score = 0
    
    # Crear instancias y grupos de sprites
    vehicle = Vehicle()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(vehicle)
    
    obstacles = pygame.sprite.Group()
    ammo_items = pygame.sprite.Group()

    # Reproducir música de fondo en bucle
    pygame.mixer.music.play(-1)  # -1 para repetir en bucle

def spawn_obstacle():
    if random.random() < 0.02:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

def spawn_ammo():
    if random.random() < 0.001:  # Menor frecuencia de aparición
        ammo = Ammo()
        all_sprites.add(ammo)
        ammo_items.add(ammo)

# Función para verificar colisiones
def check_collisions():
    return pygame.sprite.spritecollideany(vehicle, obstacles)

def check_bullet_collisions():
    global score
    collisions = pygame.sprite.groupcollide(obstacles, vehicle.bullets, True, True)
    if collisions:
        score += len(collisions)

def check_ammo_collisions():
    if pygame.sprite.spritecollideany(vehicle, ammo_items):
        vehicle.reload()  # Recargar munición
        pickup_ammo_sound.play()  # Reproducir sonido al recoger munición
        ammo_items.empty()  # Eliminar el ítem de munición

# Función para dibujar la puntuación y el conteo de disparos
def draw_score_and_bullets():
    global score
    font = pygame.font.SysFont(None, 50)
    
    # Dibujar puntuación
    score_text = font.render(f'PUNTAJE: {score}', True, WHITE)
    WIN.blit(score_text, (10, 10))
    
    # Dibujar disparos restantes
    bullets_text = font.render(f'DISPAROS RESTANTES: {vehicle.current_bullets}', True, WHITE)
    WIN.blit(bullets_text, (10, 50))

# Función para mostrar pantalla de finalización
def game_over_screen():
    global restart_button, quit_button

    font = pygame.font.SysFont(None, 80)
    text = font.render('Game Over', True, RED)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    
    # Botones para reiniciar y cerrar
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50)
    
    pygame.draw.rect(WIN, PURPLE, restart_button)
    pygame.draw.rect(WIN, PURPLE, quit_button)
    
    font = pygame.font.SysFont(None, 36)
    restart_text = font.render('REINICIAR', True, WHITE)
    quit_text = font.render('SALIR', True, WHITE)
    
    WIN.blit(restart_text, (restart_button.x + 39, restart_button.y + 10))
    WIN.blit(quit_text, (quit_button.x + 65, quit_button.y + 10))
    
    pygame.display.flip()

# Bucle principal del juego
def main():
    global score
    global vehicle
    global all_sprites
    global obstacles
    global ammo_items
    global restart_button
    global quit_button

    reset_game()  # Inicializa el juego
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(pos):
                        reset_game()  # Reiniciar el juego
                        game_over = False
                    if quit_button.collidepoint(pos):
                        running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        vehicle.shoot()
        
        if not game_over:
            # Actualizar
            all_sprites.update()
            spawn_obstacle()
            spawn_ammo()
            check_bullet_collisions()
            check_ammo_collisions()
    
            # Verificar colisiones
            if check_collisions():
                collision_obstacle_sound.play()  # Reproducir sonido al chocar con un obstáculo
                game_over = True
            else:
                # Incrementar puntuación
                score += 1
    
            # Dibujar
            WIN.blit(background_image, (0, 0))
            all_sprites.draw(WIN)
            draw_score_and_bullets()
        else:
            # Pantalla de finalización
            game_over_screen()

        pygame.display.flip()
        CLOCK.tick(FPS)
    
    pygame.quit()

main()
