import math
import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label, side=1):
        # side: -1 = left-hand puller (pulls left), +1 = right-hand puller
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.side = side
        self.font = pygame.font.SysFont(None, 24)

    def _rotate(self, px, py, pivot, angle):
        """Rotate point (px, py) around pivot by angle (radians, screen coords)."""
        dx, dy = px - pivot[0], py - pivot[1]
        return (
            pivot[0] + dx * math.cos(angle) - dy * math.sin(angle),
            pivot[1] + dx * math.sin(angle) + dy * math.cos(angle),
        )

    def render(self, surface, lean=0.0):
        """Draw avatar and label.

        lean: degrees the puller tilts backwards (away from the rope).
        """
        # Task 3: the body pivots around the feet. For the left puller a
        # negative angle tips the head to the left (backwards); for the right
        # puller a positive angle tips it right, hence angle = side * lean.
        angle = math.radians(lean) * self.side
        pivot = (self.x, self.y + 35)

        # Body (rotated rectangle)
        x0, x1 = self.x - 20, self.x + 20
        y0, y1 = self.y - 35, self.y + 35
        corners = [self._rotate(px, py, pivot, angle)
                   for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        pygame.draw.polygon(surface, self.color, corners)

        # Head (rotates with the body)
        hx, hy = self._rotate(self.x, self.y - 50, pivot, angle)
        pygame.draw.circle(surface, (240, 210, 180), (int(hx), int(hy)), 16)

        # Name / control tag
        label_surf = self.font.render(self.label, True, (240, 240, 240))
        surface.blit(label_surf, (self.x - label_surf.get_width() // 2, self.y + 45))

