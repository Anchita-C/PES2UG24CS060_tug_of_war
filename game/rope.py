import math
import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = float(screen_width // 2)

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

    def pull_left(self, strength=1.0):
        self.marker_x -= self.pull_step * strength

    def pull_right(self, strength=1.0):
        self.marker_x += self.pull_step * strength

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def player_progress(self):
        """0.0 = center, 1.0 = player's goal line."""
        total = self.screen_width // 2 - self.left_win_x
        if total <= 0:
            return 0.0
        return max(0.0, min(1.0, (self.screen_width // 2 - self.marker_x) / total))

    def offset_ratio(self):
        """0.0 = center, 1.0 = either goal line."""
        center = self.screen_width // 2
        span = max(1.0, (self.right_win_x - self.left_win_x) / 2)
        return min(1.0, abs(self.marker_x - center) / span)

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.velocity = 0.0

    def _wave_y(self, x, tension, time_s):
        x_start, x_end = 60, self.screen_width - 60
        t = (x - x_start) / (x_end - x_start)
        t = max(0.0, min(1.0, t))
        envelope = math.sin(math.pi * t)
        sag = (1.0 - tension) * 10 * envelope
        vibration = tension * 3.5 * math.sin(t * 24 + time_s * 40) * envelope
        return sag + vibration

    def render(self, surface, tension=0.0, time_s=0.0):
        points = []
        steps = 60
        for i in range(steps + 1):
            x = 60 + (self.screen_width - 120) * i / steps
            points.append((x, self.center_y + self._wave_y(x, tension, time_s)))
        pygame.draw.lines(surface, (180, 140, 90), False, points, 10)

        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        flag_y = self.center_y + self._wave_y(self.marker_x, tension, time_s)
        flag_rect = pygame.Rect(0, 0, 24, 48)
        flag_rect.center = (int(self.marker_x), int(flag_y))
        pygame.draw.rect(surface, (230, 40, 40), flag_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), flag_rect, width=2, border_radius=4)

