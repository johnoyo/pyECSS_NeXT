from ECS.Entity import Entity
import numpy as np

class TagComponent:
    def __init__(self, name = 'UnnamedEntity'):
        self.tag = name

class TransformComponent:
    def __init__(self, translation, rotation, scale):
        self.translation = translation
        self.rotation = rotation
        self.scale = scale

        self.local_matrix = np.identity(4)
        self.world_matrix = np.identity(4)

        self.is_dirty = True

class LinkComponent:
    def __init__(self, parent: Entity):
        self.parent: Entity = parent

class RenderComponent:
    def __init__(self, color):
        self.color = color