from ECS.BuiltInComponents import TransformComponent, LinkComponent, TagComponent, RenderComponent
from ECS.BuiltInSystems import TransformSystem, LinkSystem, RenderingSystem
from ECS.System import System
from ECS.Entity import Entity
from ECS.Registry import Registry
from ECS.Renderer import Renderer
from ECS.Application import Application

from ECS import Math as utils

import sdl2
import sdl2.ext

"""
Showcase of user defined system and component and runtime addition of components
"""

class GravityComponent:
    def __init__(self, strength):
        self.strength = strength

class GravitySystem(System):
    """
    The system responsible for rendering.
    """

    def on_create(self, entity: Entity, components):
        """
        Gets called once in the first frame for every entity that the system operates on.
        """
        gravity, transform = components
        transform.translation[1] -= gravity.strength * 0.0001

    def on_update(self, entity: Entity, components):
        """
        Gets called every frame for every entity that the system operates on.
        """
        gravity, transform = components
        transform.translation[1] -= gravity.strength * 0.0001

# Example Usage
def main():
    # Create Enroll entities to registry
    entity1 = Registry().enroll_entity()
    entity2 = Registry().enroll_entity()
    entity3 = Registry().enroll_entity()
    entity4 = Registry().enroll_entity()

    # Register components to entity1
    Registry().add_component(entity1, TagComponent("e1"))
    Registry().add_component(entity1, TransformComponent(utils.vec(0, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity1, LinkComponent(None))
    Registry().add_component(entity1, RenderComponent(utils.vec(1,1,1,1)))

    # Register components to entity2
    Registry().add_component(entity2, TagComponent("e2"))
    Registry().add_component(entity2, TransformComponent(utils.vec(-1.5, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity2, LinkComponent(entity1))
    Registry().add_component(entity2, RenderComponent(utils.vec(1,0,0,1)))

    # Register components to entity3
    Registry().add_component(entity3, TagComponent("e3"))
    Registry().add_component(entity3, TransformComponent(utils.vec(-0.5, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity3, LinkComponent(entity2))
    Registry().add_component(entity3, RenderComponent(utils.vec(0,0,1,1)))
    Registry().add_component(entity3, GravityComponent(5))

    # Register components to entity4
    Registry().add_component(entity4, TagComponent("e4"))
    Registry().add_component(entity4, TransformComponent(utils.vec(1.5, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity4, LinkComponent(entity1))
    Registry().add_component(entity4, RenderComponent(utils.vec(0,1,0,1)))

    # Create Register systems
    Registry().register_system(TransformSystem([TransformComponent]))
    Registry().register_system(LinkSystem([LinkComponent, TransformComponent]))
    Registry().register_system(RenderingSystem([RenderComponent, TransformComponent]))
    Registry().register_system(GravitySystem([GravityComponent, TransformComponent]))

    Application().create('Hello World', 1280, 720, True)

    Renderer().initialize()

    # Initialize system2
    Registry().start()

    selected_entity: Entity = entity4

    # Game loop
    while Application().is_running():
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                selected_entity = move_selected_entity(event, selected_entity, entity1, entity2, entity3, entity4)
            if event.type == sdl2.SDL_QUIT:
                Application().quit()

        # Update systems
        Renderer().begin_frame()
        Registry().update()
        Renderer().end_frame()

    Renderer().clean()
    Application().clean()

def move_selected_entity(event, selected_entity, entity1, entity2, entity3, entity4):
    if event.key.keysym.sym == sdl2.SDLK_1:
        selected_entity = entity1
    elif event.key.keysym.sym == sdl2.SDLK_2:
        selected_entity = entity2
    elif event.key.keysym.sym == sdl2.SDLK_3:
        selected_entity = entity3
    elif event.key.keysym.sym == sdl2.SDLK_4:
        selected_entity = entity4

    if event.key.keysym.sym == sdl2.SDLK_d:
        Registry().get_component(selected_entity, TransformComponent).translation[0] += 0.025
    elif event.key.keysym.sym == sdl2.SDLK_a:
        Registry().get_component(selected_entity, TransformComponent).translation[0] -= 0.025
    if event.key.keysym.sym == sdl2.SDLK_w:
        Registry().get_component(selected_entity, TransformComponent).translation[1] += 0.025
    elif event.key.keysym.sym == sdl2.SDLK_s:
        Registry().get_component(selected_entity, TransformComponent).translation[1] -= 0.025

    if event.key.keysym.sym == sdl2.SDLK_g:
        Registry().add_component(selected_entity, GravityComponent(5))

    return selected_entity

if __name__ == "__main__":
    main()