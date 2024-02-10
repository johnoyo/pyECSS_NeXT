from ECS.BuiltInComponents import TransformComponent, LinkComponent, InfoComponent, RenderComponent, MaterialComponent
from ECS.BuiltInSystems import TransformSystem, LinkSystem, RenderingSystem
from ECS.Entity import Entity
from ECS.Registry import Registry
from ECS.Renderer import Renderer
from ECS.Application import Application

from ECS.Utilities.MaterialLib import MaterialLib, MaterialData
from ECS.Utilities.ShaderLib import ShaderLib
from ECS.Utilities.TextureLib import TextureLib

from ECS import Math as utils

import sdl2
import sdl2.ext

import OpenGL.GL as gl

import numpy as np

"""
Showcase of basic usage and API
"""

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

    Application().create('Hello World', 1280, 720, True)

    Renderer().initialize()

    # Build textures
    d = TextureLib().build('dark_wood', 'dark_wood_texture.jpg')
    u = TextureLib().build('uoc_logo', 'uoc_logo.png')
    w = TextureLib().build('white_texture', None, [0xffffffff.to_bytes(4, byteorder='big'), 1, 1])

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
        [-0.5,  0.5, 0.0]  #3
    ], dtype=np.float32)

    texture_coords = np.array([
        [0.0, 1.0], #0
        [1.0, 1.0], #1
        [1.0, 0.0], #2
        [0.0, 0.0]  #3
    ], dtype=np.float32)

    indices = np.array([
        [0, 1, 2],
        [2, 3, 0]
    ], dtype=np.uint32)

    # Register components to entity1
    Registry().add_component(entity1, InfoComponent("e1"))
    Registry().add_component(entity1, TransformComponent(utils.vec(0, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity1, LinkComponent(None))
    Registry().add_component(entity1, RenderComponent([vertices, texture_coords], indices))
    Registry().add_component(entity1, MaterialComponent('M_Red_Textured'))

    Registry().add_component(entity2, InfoComponent("e2"))
    Registry().add_component(entity2, TransformComponent(utils.vec(2, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity2, LinkComponent(entity1))
    Registry().add_component(entity2, RenderComponent([vertices], indices))
    Registry().add_component(entity2, MaterialComponent('M_Red_Simple'))

    Registry().add_component(entity3, InfoComponent("e3"))
    Registry().add_component(entity3, TransformComponent(utils.vec(-2, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity3, LinkComponent(entity1))
    Registry().add_component(entity3, RenderComponent([vertices, texture_coords], indices))
    Registry().add_component(entity3, MaterialComponent('M_Blue'))

    # Create Register systems
    Registry().register_system(TransformSystem([TransformComponent]))
    Registry().register_system(LinkSystem([LinkComponent, TransformComponent]))
    Registry().register_system(RenderingSystem([RenderComponent, MaterialComponent, TransformComponent]))

    # Initialize systems
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

    return selected_entity

if __name__ == "__main__":
    main()