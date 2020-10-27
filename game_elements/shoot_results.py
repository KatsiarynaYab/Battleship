import config


class ShootResult():
    def __init__(self, image):
        self.coordinates = (0, 0)
        self._image = image
        self._rect = self._image.get_rect()

    def set_coordinates(self, x, y):
        self.coordinates = (x, y)

    def update(self, surface):
        self._rect.x, self._rect.y = self.coordinates
        surface.blit(self._image, self._rect)

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __ne__(self, other):
        return self.coordinates != other.coordinates

    def __hash__(self):
        return hash(self.coordinates)


class Fire(ShootResult):
    def __init__(self):
        ShootResult.__init__(self, config.fire_image)


class Missfire(ShootResult):
    def __init__(self):
        ShootResult.__init__(self, config.missfire_image)
