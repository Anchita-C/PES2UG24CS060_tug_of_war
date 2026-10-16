import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label, side=1):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.side = side
        self.font = pygame.font.SysFont(None, 24)

    def render(self, surface, lean=0):
        """Draw avatar and label with a slight lean indicating momentum."""
        lean = max(-24, min(24, lean))
        lean_offset = self.side * lean

        # Body and torso
        body_rect = pygame.Rect(self.x - 20 + int(lean_offset * 0.35), self.y - 35, 40, 70)
        pygame.draw.rect(surface, self.color, body_rect, border_radius=6)

        # Head
        head_x = self.x + int(lean_offset * 0.3)
        pygame.draw.circle(surface, (240, 210, 180), (head_x, self.y - 50), 16)

        # Arms/legs to suggest leaning posture
        arm_offset = int(lean_offset * 0.6)
        pygame.draw.line(surface, (40, 40, 40), (self.x, self.y - 10), (self.x + arm_offset, self.y + 12), 4)
        pygame.draw.line(surface, (40, 40, 40), (self.x, self.y + 28), (self.x - arm_offset, self.y + 52), 4)

        # Name / control tag
        label_surf = self.font.render(self.label, True, (240, 240, 240))
        surface.blit(label_surf, (self.x - label_surf.get_width() // 2, self.y + 45))

