import random
import pygame
from game.rope import Rope
from game.player import Puller

# --- Task 4: sudden death ---------------------------------------------------
SUDDEN_DEATH_MS = 45_000
SUDDEN_DEATH_MULT = 2.0

# --- Task 2: computer difficulty surge --------------------------------------
BASE_COOLDOWN_MS = 180
SURGE_TRIGGER = 0.40
SURGE_COOLDOWN_MS = 140
SURGE_DURATION_MS = 1500
SURGE_REST_MS = 4000


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)
        self.player = Puller(90, height // 2, (50, 120, 220), "PLAYER (A/D)", side=-1)
        self.computer = Puller(width - 90, height // 2, (220, 80, 50), "COMPUTER", side=1)

        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        self.computer_pull_cooldown = BASE_COOLDOWN_MS
        self.last_computer_pull = pygame.time.get_ticks()

        self.surge_until = 0
        self.surge_ready_at = 0

        self.player_energy = 0.0
        self.computer_energy = 0.0

        self.start_time = pygame.time.get_ticks()
        self.elapsed_ms = 0
        self.sudden_death = False

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                if event.key != self.last_key:
                    self.rope.pull_left(self._pull_multiplier())
                    self.last_key = event.key
                    self.player_energy = min(1.0, self.player_energy + 0.3)

    def _pull_multiplier(self):
        return SUDDEN_DEATH_MULT if self.sudden_death else 1.0

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()
        self.elapsed_ms = now - self.start_time

        if not self.sudden_death and self.elapsed_ms >= SUDDEN_DEATH_MS:
            self.sudden_death = True

        if (now >= self.surge_until and now >= self.surge_ready_at
                and self.rope.player_progress() >= SURGE_TRIGGER):
            self.surge_until = now + SURGE_DURATION_MS
            self.surge_ready_at = self.surge_until + SURGE_REST_MS
        self.surging = now < self.surge_until
        cooldown = SURGE_COOLDOWN_MS if self.surging else BASE_COOLDOWN_MS

        if now - self.last_computer_pull >= cooldown:
            computer_variance = random.uniform(0.7, 1.2)
            self.rope.pull_right(computer_variance * self._pull_multiplier())
            self.last_computer_pull = now
            self.computer_energy = min(1.0, self.computer_energy + 0.3)

        self.player_energy *= 0.95
        self.computer_energy *= 0.95

        result = self.rope.check_winner()
        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    surging = False

    def reset(self):
        self.rope.reset()
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"
        self.last_computer_pull = pygame.time.get_ticks()
        self.surge_until = 0
        self.surge_ready_at = 0
        self.surging = False
        self.player_energy = 0.0
        self.computer_energy = 0.0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_ms = 0
        self.sudden_death = False

    def render(self, screen):
        screen.fill((30, 32, 36))

        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        tension = min(1.0, (self.player_energy + self.computer_energy) * 0.6
                      + self.rope.offset_ratio() * 0.4)
        time_s = pygame.time.get_ticks() / 1000.0
        self.rope.render(screen, tension, time_s)

        player_lean = 6 + 24 * max(0.0, min(1.0, self.player_energy - self.computer_energy * 0.5))
        computer_lean = 6 + 24 * max(0.0, min(1.0, self.computer_energy - self.player_energy * 0.5))
        self.player.render(screen, player_lean)
        self.computer.render(screen, computer_lean)

        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!", True, (210, 210, 210)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 40))

        total_s = self.elapsed_ms // 1000
        timer_surf = self.font_small.render(
            f"Time: {total_s // 60:02d}:{total_s % 60:02d}", True, (240, 240, 240)
        )
        screen.blit(timer_surf, (self.width // 2 - timer_surf.get_width() // 2, 10))
        if self.sudden_death:
            sd_surf = self.font_small.render(
                "SUDDEN DEATH - double pull!", True, (255, 90, 90)
            )
            screen.blit(sd_surf, (self.width // 2 - sd_surf.get_width() // 2, 70))
        elif self.surging and self.game_state == "PLAYING":
            sg_surf = self.font_small.render("Computer surge!", True, (255, 170, 60))
            screen.blit(sg_surf, (self.width // 2 - sg_surf.get_width() // 2, 70))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50)
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )

