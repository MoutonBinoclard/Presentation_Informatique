import sys
import math
import random
import pygame

# Config
WIDTH, HEIGHT = 1000, 600
FPS = 90

PADDLE_W, PADDLE_H = 110, 16
PADDLE_SPEED = 8

BALL_R = 8
BALL_SPEED = 6.0
# Power-up config
POWERUP_CHANCE = 0.18        # probabilité de drop par brique
POWERUP_SPEED = 3.0          # vitesse de chute
PADDLE_GROW_FACTOR = 1.6     # facteur d'agrandissement
PADDLE_GROW_DURATION_MS = 10000
MULTI_BALL_NEW = 10           # nombre de balles supplémentaires
POWERUP_COLORS = {
    "MULTI": (255, 120, 120),
    "GROW": (120, 200, 255),
}

MARGIN = 20
ROWS, COLS = 5, 9
BRICK_GAP = 6
BRICK_W = (WIDTH - 2 * MARGIN - (COLS - 1) * BRICK_GAP) // COLS
BRICK_H = 24
BRICK_TOP = 70

LIVES_START = 3

# Colors
BG = (18, 18, 20)
WHITE = (240, 240, 240)
PADDLE_COLOR = (200, 200, 255)
BALL_COLOR = (255, 230, 120)
BRICK_PALETTE = [
    (255, 99, 99),
    (255, 159, 64),
    (255, 205, 86),
    (75, 192, 192),
    (54, 162, 235),
    (153, 102, 255),
]

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, PADDLE_W, PADDLE_H)
        self.rect.midbottom = (x, y)
        self.vx = 0
        self.base_width = PADDLE_W  # pour revenir à la taille d'origine

    def update(self):
        self.rect.x += self.vx
        self.rect.x = clamp(self.rect.x, 0, WIDTH - self.rect.width)

    def resize(self, new_width: int):
        # conserve le centre en x lors du redimensionnement
        cx = self.rect.centerx
        self.rect.width = int(max(40, min(new_width, WIDTH)))
        self.rect.centerx = cx
        # s'assurer qu'on reste dans l'écran après resize
        self.rect.x = clamp(self.rect.x, 0, WIDTH - self.rect.width)

    def draw(self, surf):
        pygame.draw.rect(surf, PADDLE_COLOR, self.rect, border_radius=6)

class Ball:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(math.radians(30), math.radians(150))
        self.vx = math.cos(angle) * BALL_SPEED
        self.vy = -abs(math.sin(angle) * BALL_SPEED)
        self.r = BALL_R
        self.stuck_to_paddle = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r * 2, self.r * 2)

    def launch_from_paddle(self):
        self.stuck_to_paddle = False
        if abs(self.vy) < 1.0:
            self.vy = -BALL_SPEED * 0.8
        self._normalize_speed(BALL_SPEED)

    def attach_to_paddle(self, paddle_rect):
        self.stuck_to_paddle = True
        self.x = paddle_rect.centerx
        self.y = paddle_rect.top - self.r - 1
        self.vx = 0
        self.vy = -BALL_SPEED

    def _normalize_speed(self, target):
        speed = math.hypot(self.vx, self.vy)
        if speed == 0:
            self.vx, self.vy = target, -target
            return
        scale = target / speed
        self.vx *= scale
        self.vy *= scale

    def update(self):
        if self.stuck_to_paddle:
            return
        self.x += self.vx
        self.y += self.vy

        # Wall collisions
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = abs(self.vx)
        elif self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -abs(self.vx)

        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = abs(self.vy)

        # Add tiny variation to avoid boring loops
        self.vx *= 1.0005
        self.vy *= 1.0005
        self._normalize_speed(BALL_SPEED)

    def draw(self, surf):
        pygame.draw.circle(surf, BALL_COLOR, (int(self.x), int(self.y)), self.r)

def create_bricks():
    bricks = []
    for r in range(ROWS):
        color = BRICK_PALETTE[r % len(BRICK_PALETTE)]
        for c in range(COLS):
            x = MARGIN + c * (BRICK_W + BRICK_GAP)
            y = BRICK_TOP + r * (BRICK_H + BRICK_GAP)
            rect = pygame.Rect(x, y, BRICK_W, BRICK_H)
            bricks.append((rect, color))
    return bricks

def reflect_ball_on_rect(ball, rect):
    # Determine collision side by minimal overlap
    b = ball.rect
    dx_left = b.right - rect.left
    dx_right = rect.right - b.left
    dy_top = b.bottom - rect.top
    dy_bottom = rect.bottom - b.top
    min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

    if min_overlap == dx_left:
        ball.x -= dx_left
        ball.vx = -abs(ball.vx)
    elif min_overlap == dx_right:
        ball.x += dx_right
        ball.vx = abs(ball.vx)
    elif min_overlap == dy_top:
        ball.y -= dy_top
        ball.vy = -abs(ball.vy)
    else:
        ball.y += dy_bottom
        ball.vy = abs(ball.vy)

def handle_ball_paddle_collision(ball, paddle):
    if not ball.rect.colliderect(paddle.rect):
        return
    # Place ball above paddle and reflect
    ball.y = paddle.rect.top - ball.r - 1
    # Angle based on hit position on paddle
    hit_pos = (ball.x - paddle.rect.left) / paddle.rect.width  # 0..1
    angle = math.radians(150) - hit_pos * math.radians(120)    # 150°..30°
    speed = BALL_SPEED
    ball.vx = speed * math.cos(angle)
    ball.vy = -abs(speed * math.sin(angle))

def draw_text(surf, text, size, color, center, bold=False):
    font = pygame.font.SysFont(None, size, bold=bold)
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    surf.blit(render, rect)

class PowerUp:
    def __init__(self, x, y, kind: str):
        self.kind = kind  # "MULTI" ou "GROW"
        size = 24
        self.rect = pygame.Rect(int(x - size / 2), int(y - size / 2), size, size)
        self.vy = POWERUP_SPEED

    def update(self):
        self.rect.y += self.vy

    def draw(self, surf):
        color = POWERUP_COLORS.get(self.kind, (200, 200, 200))
        pygame.draw.rect(surf, color, self.rect, border_radius=6)

def main():
    pygame.init()
    pygame.display.set_caption("Casse-brique")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    paddle = Paddle(WIDTH // 2, HEIGHT - 30)

    # Utiliser une liste de balles et une liste de power-ups
    balls = [Ball(paddle.rect.centerx, paddle.rect.top - BALL_R - 1)]
    balls[0].attach_to_paddle(paddle.rect)
    powerups = []

    bricks = create_bricks()
    score = 0
    lives = LIVES_START
    running = True
    won = False
    lost = False

    move_left = False
    move_right = False

    # timer d'effet pour la raquette agrandie
    grow_timer_ms = 0

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    move_left = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_right = True
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    # lancer une balle si l'une d'elles est collée
                    for b in balls:
                        if b.stuck_to_paddle and not (won or lost):
                            b.launch_from_paddle()
                            break
                elif event.key == pygame.K_r:
                    # Restart
                    bricks = create_bricks()
                    score = 0
                    lives = LIVES_START
                    won = False
                    lost = False
                    paddle = Paddle(WIDTH // 2, HEIGHT - 30)
                    balls = [Ball(paddle.rect.centerx, paddle.rect.top - BALL_R - 1)]
                    balls[0].attach_to_paddle(paddle.rect)
                    powerups = []
                    grow_timer_ms = 0
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_left = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_right = False

        if not (won or lost):
            # Update paddle
            paddle.vx = (-PADDLE_SPEED if move_left else 0) + (PADDLE_SPEED if move_right else 0)
            paddle.update()

            # Mettre à jour les effets temporaires (GROW)
            if grow_timer_ms > 0:
                grow_timer_ms -= dt
                if grow_timer_ms <= 0:
                    # fin de l'effet -> revenir à la taille de base
                    paddle.resize(paddle.base_width)

            # Mettre à jour les balles
            for b in balls:
                if b.stuck_to_paddle:
                    b.attach_to_paddle(paddle.rect)
                else:
                    b.update()

            # Collisions balle/raquette
            for b in balls:
                if not b.stuck_to_paddle:
                    handle_ball_paddle_collision(b, paddle)

            # Collisions balle/briques (et drop de power-up)
            removed_brick_index = None
            for bi, (brect, color) in enumerate(bricks):
                hit = False
                for b in balls:
                    if b.rect.colliderect(brect):
                        reflect_ball_on_rect(b, brect)
                        hit = True
                        break
                if hit:
                    removed_brick_index = bi
                    break
            if removed_brick_index is not None:
                # supprimer la brique, augmenter le score, et potentiellement lâcher un power-up
                brect, _ = bricks.pop(removed_brick_index)
                score += 10
                if random.random() < POWERUP_CHANCE:
                    kind = random.choice(["MULTI", "GROW"])
                    powerups.append(PowerUp(brect.centerx, brect.centery, kind))

            # Gérer les balles qui tombent
            balls = [b for b in balls if (b.y - b.r) <= HEIGHT]
            if not balls:
                lives -= 1
                if lives > 0:
                    # ré-apparition d'une seule balle collée à la raquette
                    balls = [Ball(paddle.rect.centerx, paddle.rect.top - BALL_R - 1)]
                    balls[0].attach_to_paddle(paddle.rect)
                else:
                    lost = True

            # Win condition
            if not bricks:
                won = True

            # Update power-ups
            for pu in powerups:
                pu.update()
            # Collision power-up / raquette
            collected = []
            for pu in powerups:
                if pu.rect.colliderect(paddle.rect):
                    if pu.kind == "GROW":
                        paddle.resize(int(paddle.base_width * PADDLE_GROW_FACTOR))
                        grow_timer_ms = PADDLE_GROW_DURATION_MS
                    elif pu.kind == "MULTI":
                        # choisir une balle source (de préférence en mouvement)
                        source = None
                        for b in balls:
                            if not b.stuck_to_paddle:
                                source = b
                                break
                        if source is None and balls:
                            source = balls[0]
                            if source.stuck_to_paddle:
                                # lancer si elle était collée pour éviter des clones immobiles
                                source.launch_from_paddle()
                        if source is not None:
                            base_angle = math.atan2(source.vy, source.vx)
                            # Génère un éventail de MULTI_BALL_NEW angles entre -60° et +60°
                            angles = [math.radians(-60 + (120 * (i / max(1, MULTI_BALL_NEW - 1)))) for i in range(MULTI_BALL_NEW)]
                            for off in angles:
                                nb = Ball(source.x, source.y)
                                nb.stuck_to_paddle = False
                                ang = base_angle + off
                                speed = BALL_SPEED
                                nb.vx = math.cos(ang) * speed
                                nb.vy = math.sin(ang) * speed
                                # forcer un départ vers le haut
                                if nb.vy > 0:
                                    nb.vy = -abs(nb.vy)
                                balls.append(nb)
                    collected.append(pu)
                elif pu.rect.top > HEIGHT:
                    collected.append(pu)
            # retirer les power-ups collectés/sortis de l'écran
            if collected:
                powerups = [pu for pu in powerups if pu not in collected]

        # Draw
        screen.fill(BG)
        for brect, color in bricks:
            pygame.draw.rect(screen, color, brect, border_radius=6)
        paddle.draw(screen)
        for b in balls:
            b.draw(screen)
        # dessiner les power-ups
        for pu in powerups:
            pu.draw(screen)

        # HUD
        draw_text(screen, f"Score: {score}", 28, WHITE, (80, 20))
        draw_text(screen, f"Vies: {lives}", 28, WHITE, (WIDTH - 80, 20))
        if grow_timer_ms > 0:
            draw_text(screen, "Bonus: Grande raquette", 22, WHITE, (WIDTH // 2, 20))
        if won:
            draw_text(screen, "Bravo ! Vous avez gagné", 40, WHITE, (WIDTH // 2, HEIGHT // 2 - 10), bold=True)
            draw_text(screen, "Appuyez sur R pour rejouer", 28, WHITE, (WIDTH // 2, HEIGHT // 2 + 30))
        elif lost:
            draw_text(screen, "Perdu !", 40, WHITE, (WIDTH // 2, HEIGHT // 2 - 10), bold=True)
            draw_text(screen, "Appuyez sur R pour rejouer", 28, WHITE, (WIDTH // 2, HEIGHT // 2 + 30))
        else:
            # message de lancement si une balle est collée
            if any(b.stuck_to_paddle for b in balls):
                draw_text(screen, "Espace pour lancer la balle", 24, (200, 200, 200), (WIDTH // 2, HEIGHT - 60))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Erreur:", e)
        pygame.quit()
        sys.exit(1)
    except Exception as e:
        print("Erreur:", e)
        pygame.quit()
        sys.exit(1)
