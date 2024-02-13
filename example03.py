from ECS.BuiltInComponents import TransformComponent, LinkComponent, InfoComponent, RenderComponent, MaterialComponent
from ECS.BuiltInSystems import TransformSystem, LinkSystem, RenderingSystem
from ECS.System import System
from ECS.Entity import Entity
from ECS.Registry import Registry
from ECS.Renderer.Renderer2D import Renderer2D
from ECS.Application import Application

from ECS.Utilities.MaterialLib import MaterialLib, MaterialData
from ECS.Utilities.ShaderLib import ShaderLib

from ECS import Math as utils

import numpy as np

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

    vertex_shader_code = """
    #version 330 core
    layout(location = 0) in vec3 aPos;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        gl_Position = vec4(aPos, 1.0) * model * view * projection;
    }
    """

    fragment_shader_code_red = """
    #version 330 core
    out vec4 FragColor;

    uniform vec4 u_Color;

    void main()
    {
        FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
    """

    Application().create('Hello World', 1280, 720, True)

    Renderer2D().initialize()

    ShaderLib().build('default_colored_red', vertex_shader_code, fragment_shader_code_red)
    MaterialLib().build('M_Red', MaterialData('default_colored_red', []))

    vertices = np.array([
        [-0.5, -0.5, 0.0], #0
        [ 0.5, -0.5, 0.0], #1
        [ 0.5,  0.5, 0.0], #2
        [-0.5,  0.5, 0.0]  #3
    ], dtype=np.float32)

    indices = np.array([
        [0, 1, 2],
        [2, 3, 0]
    ], dtype=np.uint32)

    # Register components to entity1
    Registry().add_component(entity1, InfoComponent("e1"))
    Registry().add_component(entity1, TransformComponent(utils.vec(0, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity1, LinkComponent(None))
    Registry().add_component(entity1, RenderComponent([vertices], indices))
    Registry().add_component(entity1, MaterialComponent('M_Red'))

    # Register components to entity2
    Registry().add_component(entity2, InfoComponent("e2"))
    Registry().add_component(entity2, TransformComponent(utils.vec(-1.5, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity2, LinkComponent(entity1))
    Registry().add_component(entity2, RenderComponent([vertices], indices))
    Registry().add_component(entity2, MaterialComponent('M_Red'))

    # Register components to entity3
    Registry().add_component(entity3, InfoComponent("e3"))
    Registry().add_component(entity3, TransformComponent(utils.vec(-0.5, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity3, LinkComponent(entity2))
    Registry().add_component(entity3, RenderComponent([vertices], indices))
    Registry().add_component(entity3, MaterialComponent('M_Red'))
    Registry().add_component(entity3, GravityComponent(5))

    # Register components to entity4
    Registry().add_component(entity4, InfoComponent("e4"))
    Registry().add_component(entity4, TransformComponent(utils.vec(1.5, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity4, LinkComponent(entity1))
    Registry().add_component(entity4, RenderComponent([vertices], indices))
    Registry().add_component(entity4, MaterialComponent('M_Red'))
    Registry().add_component(entity4, GravityComponent(5))

    # Create Register systems
    Registry().register_system(TransformSystem([TransformComponent]))
    Registry().register_system(LinkSystem([LinkComponent, TransformComponent]))
    Registry().register_system(RenderingSystem([RenderComponent, MaterialComponent, TransformComponent]))

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
        Renderer2D().begin_frame()
        Registry().update()
        Renderer2D().end_frame()

    Renderer2D().clean()
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
        Registry().register_system(GravitySystem([GravityComponent, TransformComponent]))

    return selected_entity

if __name__ == "__main__":
    main()