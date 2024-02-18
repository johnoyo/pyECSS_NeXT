from ECS.BuiltInComponents import TransformComponent, LinkComponent, InfoComponent, RenderComponent, MaterialComponent
from ECS.BuiltInSystems import TransformSystem, LinkSystem, RenderingSystem
from ECS.Entity import Entity
from ECS.Registry import Registry
from ECS.Renderer.Renderer2D import Renderer2D
from ECS.Application import Application

from ECS.Utilities.MaterialLib import MaterialLib, MaterialData
from ECS.Utilities.ShaderLib import ShaderLib
from ECS.Utilities.TextureLib import TextureLib

from ECS import Math as utils

import glfw

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
    layout(location = 2) in float a_TexId;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    out vec2 v_TexCoord;
    out float v_TexId;

    void main()
    {
        v_TexCoord = a_TexCoord;
        v_TexId = a_TexId;
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

    in vec2 v_TexCoord;
    in float v_TexId;

    void main()
    {
        int id = int(v_TexId);
        FragColor = texture(u_Textures[id], v_TexCoord) * vec4(0.0, 0.0, 1.0, 0.0);
    }
    """

    textured_fragment_shader_code_red = """
    #version 330 core
    out vec4 FragColor;

    uniform vec4 u_Color;
    uniform sampler2D u_Textures[32];

    in vec2 v_TexCoord;
    in float v_TexId;

    void main()
    {
        int id = int(v_TexId);
        FragColor = texture(u_Textures[id], v_TexCoord) * vec4(1.0, 0.0, 0.0, 0.0);
    }
    """

    Application().create('Hello World', 1280, 720, True)

    Renderer2D().initialize()

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
    MaterialLib().build('M_Red_Textured', MaterialData('textured_colored_red', []))
    MaterialLib().build('M_Blue', MaterialData('textured_colored_blue', []))

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

    texture_ids = np.array([
        [d], #0
        [d], #1
        [d], #2
        [d]  #3
    ], dtype=np.float32)

    texture_ids_alt = np.array([
        [u], #0
        [u], #1
        [u], #2
        [u]  #3
    ], dtype=np.float32)

    indices = np.array([
        [0, 1, 2],
        [2, 3, 0]
    ], dtype=np.uint32)

    # Register components to entity1
    Registry().add_component(entity1, InfoComponent("e1"))
    Registry().add_component(entity1, TransformComponent(utils.vec(0, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity1, LinkComponent(None))
    Registry().add_component(entity1, RenderComponent([vertices, texture_coords, texture_ids], indices))
    Registry().add_component(entity1, MaterialComponent('M_Red_Textured'))

    Registry().add_component(entity2, InfoComponent("e2"))
    Registry().add_component(entity2, TransformComponent(utils.vec(2, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity2, LinkComponent(entity1))
    Registry().add_component(entity2, RenderComponent([vertices], indices))
    Registry().add_component(entity2, MaterialComponent('M_Red_Simple'))

    Registry().add_component(entity3, InfoComponent("e3"))
    Registry().add_component(entity3, TransformComponent(utils.vec(-2, 0, 0), utils.vec(0, 0, 0), utils.vec(1, 1, 1)))
    Registry().add_component(entity3, LinkComponent(entity1))
    Registry().add_component(entity3, RenderComponent([vertices, texture_coords, texture_ids_alt], indices))
    Registry().add_component(entity3, MaterialComponent('M_Blue'))

    # Create Register systems
    Registry().register_system(TransformSystem([TransformComponent]))
    Registry().register_system(LinkSystem([LinkComponent, TransformComponent]))
    Registry().register_system(RenderingSystem([RenderComponent, MaterialComponent, TransformComponent]))

    # Initialize systems
    Registry().start()

    # Define main loop
    def main_loop(ts):
        move_selected_entity(ts, entity1, entity2, entity3, entity4)

        Renderer2D().begin_frame()
        Registry().update(ts)
        Renderer2D().end_frame()

    # Dispatch game loop
    Application().dispatch_main_loop(main_loop)

    Renderer2D().clean()
    Application().clean()

def move_selected_entity(ts, entity1, entity2, entity3, entity4):
    selected_entity = entity1

    if glfw.get_key(Application().get_window(), glfw.KEY_ESCAPE) == glfw.PRESS:
        Application().quit()

    if glfw.get_key(Application().get_window(), glfw.KEY_1) == glfw.PRESS:
        selected_entity = entity1
    elif glfw.get_key(Application().get_window(), glfw.KEY_2) == glfw.PRESS:
        selected_entity = entity2
    elif glfw.get_key(Application().get_window(), glfw.KEY_3) == glfw.PRESS:
        selected_entity = entity3
    elif glfw.get_key(Application().get_window(), glfw.KEY_4) == glfw.PRESS:
        selected_entity = entity4

    if glfw.get_key(Application().get_window(), glfw.KEY_D) == glfw.PRESS:
        Registry().get_component(selected_entity, TransformComponent).translation[0] += 0.5 * ts
    elif glfw.get_key(Application().get_window(), glfw.KEY_A) == glfw.PRESS:
        Registry().get_component(selected_entity, TransformComponent).translation[0] -= 0.5 * ts
    if glfw.get_key(Application().get_window(), glfw.KEY_W) == glfw.PRESS:
        Registry().get_component(selected_entity, TransformComponent).translation[1] += 0.5 * ts
    elif glfw.get_key(Application().get_window(), glfw.KEY_S) == glfw.PRESS:
        Registry().get_component(selected_entity, TransformComponent).translation[1] -= 0.5 * ts

if __name__ == "__main__":
    main()