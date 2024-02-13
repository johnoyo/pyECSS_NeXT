from ECS.Renderer.OpenGLRenderer import OpenGLRenderer
from ECS.Renderer.WebGPURenderer import WebGPURenderer

from enum import Enum

class RendererAPI(Enum):
    NONE = 0
    OPENGL = 1
    WEBGPU = 2

class RenderCommand:
    API : RendererAPI = RendererAPI.NONE
    RENDERER = None       

    @staticmethod
    def initialize(api):
        RenderCommand.API = api

        if (RenderCommand.API == RendererAPI.OPENGL):
            RenderCommand.RENDERER = OpenGLRenderer()
        elif (RenderCommand.API == RendererAPI.WEBGPU):
            RenderCommand.RENDERER = WebGPURenderer()

        if hasattr(RenderCommand.RENDERER, 'initialize') and callable(getattr(RenderCommand.RENDERER, 'initialize')):
            RenderCommand.RENDERER.initialize()
        else:
            print(f'initialize method not implemented in {RenderCommand.API}')

        ##### WebGPU #####
        # request adapter
        # request device
        # get - configure present context
        ##################

        ### OpenGL ###
        # set settings
        ##############

        pass

    @staticmethod
    def create_bind_group_layout():
        pass

    @staticmethod
    def create_bind_group():
        pass
    
    @staticmethod
    def create_pipeline_layout():
        pass

    @staticmethod
    def create_render_pipeline():
        pass

    @staticmethod
    def begin_frame():
        ##### WebGPU #####
        # get present context texture
        # create command encoder
        # begin renderpass
        ##################

        ### OpenGL ###
        # clear screen
        ##############

        pass

    @staticmethod
    def end_frame():
        ##### WebGPU #####
        # end render pass
        # submit commands
        # request draw
        ##################

        ### OpenGL ###
        # swap buffers
        ##############

        pass

    @staticmethod
    def draw():
        if hasattr(RenderCommand.RENDERER, 'draw') and callable(getattr(RenderCommand.RENDERER, 'draw')):
            RenderCommand.RENDERER.draw()
        else:
            print(f'draw method not implemented in {RenderCommand.API}')

    @staticmethod
    def draw_indexed():
        if hasattr(RenderCommand.RENDERER, 'draw_indexed') and callable(getattr(RenderCommand.RENDERER, 'draw_indexed')):
            RenderCommand.RENDERER.draw_indexed()
        else:
            print(f'draw_indexed method not implemented in {RenderCommand.API}')

    @staticmethod
    def clean():
        pass