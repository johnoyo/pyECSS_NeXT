from ECS.BuiltInComponents import TransformComponent, LinkComponent, InfoComponent, RenderComponent, MaterialComponent
from ECS.BuiltInSystems import TransformSystem, LinkSystem, RenderingSystem
from ECS.Entity import Entity
from ECS.System import System
from ECS.Scene import Scene
from ECS.SceneManager import SceneManager
from ECS.Application import Application

from ECS.OpenGLWindow import OpenGLWindow

from ECS.Utilities.MaterialLib import MaterialLib, MaterialData
from ECS.Utilities.ShaderLib import ShaderLib
from ECS.Utilities.TextureLib import TextureLib

from ECS import Math as utils

import glfw

import numpy as np

"""
Showcase of basic usage and API
"""

class MovementComponent:
    def __init__(self) -> None:
        self.selected = False
        self.speed = 0.5

class MovementSystem(System):
    """
    The system responsible for moving.
    """

    def on_create(self, entity: Entity, components):
        """
        Gets called once in the first frame for every entity that the system operates on.
        """
        movement, transform, info = components

    def on_update(self, ts, entity: Entity, components):
        """
        Gets called every frame for every entity that the system operates on.
        """
        movement, transform, info = components

        movement.selected = False

        if glfw.get_key(Application().get_window().get_handle(), glfw.KEY_1) == glfw.PRESS:
            if info.tag == 'e1': movement.selected = True
        elif glfw.get_key(Application().get_window().get_handle(), glfw.KEY_2) == glfw.PRESS:
            if info.tag == 'e2': movement.selected = True
        elif glfw.get_key(Application().get_window().get_handle(), glfw.KEY_3) == glfw.PRESS:
            if info.tag == 'e3': movement.selected = True

        if movement.selected:
            if glfw.get_key(Application().get_window().get_handle(), glfw.KEY_D) == glfw.PRESS:
                transform.translation[0] += movement.speed * ts
            elif glfw.get_key(Application().get_window().get_handle(), glfw.KEY_A) == glfw.PRESS:
                transform.translation[0] -= movement.speed * ts
            if glfw.get_key(Application().get_window().get_handle(), glfw.KEY_W) == glfw.PRESS:
                transform.translation[1] += movement.speed * ts
            elif glfw.get_key(Application().get_window().get_handle(), glfw.KEY_S) == glfw.PRESS:
                transform.translation[1] -= movement.speed * ts

# Example Usage
def main():
    scene = Scene()

    # Create Enroll entities to registry
    entity1 = scene.enroll_entity()
    entity2 = scene.enroll_entity()
    entity3 = scene.enroll_entity()

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

    textured_vertex_shader_code = """
    #version 330 core
    layout(location = 0) in vec3 a_Pos;
    layout(location = 1) in vec2 a_TexCoord;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    out vec2 v_TexCoord;

    void main()
    {
        v_TexCoord = a_TexCoord;
        gl_Position = vec4(a_Pos, 1.0) * model * view * projection;
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

    fragment_shader_code_blue = """
    #version 330 core
    out vec4 FragColor;

    uniform vec4 u_Color;

    void main()
    {
        FragColor = vec4(0.0, 0.0, 1.0, 1.0);
    }
    """

    textured_fragment_shader_code_blue = """
    #version 330 core
    out vec4 FragColor;

    uniform vec4 u_Color;
    uniform sampler2D u_Textures[32];
    uniform float u_TextureId;

    in vec2 v_TexCoord;

    void main()
    {
        int id = int(u_TextureId);
        FragColor = texture(u_Textures[id], v_TexCoord) * vec4(0.0, 0.0, 1.0, 0.0);
    }
    """

    textured_fragment_shader_code_red = """
    #version 330 core
    out vec4 FragColor;

    uniform vec4 u_Color;
    uniform sampler2D u_Textures[32];
    uniform float u_TextureId;

    in vec2 v_TexCoord;

    void main()
    {
        int id = int(u_TextureId);
        FragColor = texture(u_Textures[id], v_TexCoord) * vec4(1.0, 0.0, 0.0, 0.0);
    }
    """

    Application().create(OpenGLWindow('Hello World', 1280, 720, True))

    # Build textures
    TextureLib().build('dark_wood', 'dark_wood_texture.jpg')
    TextureLib().build('uoc_logo', 'uoc_logo.png')
    TextureLib().build('white_texture', None, [0xffffffff.to_bytes(4, byteorder='big'), 1, 1])

    # Build shaders 
    ShaderLib().build('default_colored_red', vertex_shader_code, fragment_shader_code_red)
    ShaderLib().build('textured_colored_blue', textured_vertex_shader_code, textured_fragment_shader_code_blue)
    ShaderLib().build('textured_colored_red', textured_vertex_shader_code, textured_fragment_shader_code_red)
    
    # Build Materials
    MaterialLib().build('M_Red_Simple', MaterialData('default_colored_red', []))
    MaterialLib().build('M_Red_Textured', MaterialData('textured_colored_red', ['dark_wood']))
    MaterialLib().build('M_Blue', MaterialData('textured_colored_blue', ['uoc_logo']))

    vertices = np.array([
        [-0.5, -0.5, 0.0], #0
        [ 0.5, -0.5, 0.0], #1
        [ 0.5,  0.5, 0.0], #2
        [ 0.5,  0.5, 0.0], #2
        [-0.5,  0.5, 0.0], #3
        [-0.5, -0.5, 0.0]  #0
    ], dtype=np.float32)

    texture_coords = np.array([
        [0.0, 1.0], #0
        [1.0, 1.0], #1
        [1.0, 0.0], #2
        [1.0, 0.0], #2
        [0.0, 0.0], #3
        [0.0, 1.0]  #0
    ], dtype=np.float32)

    # Register components to entity1
    scene.add_component(entity1, InfoComponent("e1"))
    scene.add_component(entity1, TransformComponent(utils.vec(0, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    scene.add_component(entity1, LinkComponent(None))
    scene.add_component(entity1, RenderComponent([vertices, texture_coords], None))
    scene.add_component(entity1, MaterialComponent('M_Red_Textured'))
    scene.add_component(entity1, MovementComponent())

    # Register components to entity2
    scene.add_component(entity2, InfoComponent("e2"))
    scene.add_component(entity2, TransformComponent(utils.vec(2, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    scene.add_component(entity2, LinkComponent(entity1))
    scene.add_component(entity2, RenderComponent([vertices], None))
    scene.add_component(entity2, MaterialComponent('M_Red_Simple'))
    scene.add_component(entity2, MovementComponent())

    # Register components to entity3
    scene.add_component(entity3, InfoComponent("e3"))
    scene.add_component(entity3, TransformComponent(utils.vec(-2, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    scene.add_component(entity3, LinkComponent(entity1))
    scene.add_component(entity3, RenderComponent([vertices, texture_coords], None))
    scene.add_component(entity3, MaterialComponent('M_Blue'))
    scene.add_component(entity3, MovementComponent())

    # Add scene to manager
    SceneManager().add_scene(scene)

    # Create Register systems
    scene.register_system(TransformSystem([TransformComponent]))
    scene.register_system(LinkSystem([LinkComponent, TransformComponent]))
    scene.register_system(RenderingSystem([RenderComponent, MaterialComponent, TransformComponent]))
    scene.register_system(MovementSystem([MovementComponent, TransformComponent, InfoComponent]))

    # Start application
    Application().start()

if __name__ == "__main__":
    main()