from ECS.Application import Application
from ECS.Math import *

import sdl2
import OpenGL.GL as gl

import ctypes

class Renderer(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Renderer, cls).__new__(cls)
            cls.instance.vbo = 0
            cls.instance.ebo = 0
            cls.instance.vao = 0
            cls.instance.shader_program = 0
            cls.instance.vertices = []
            cls.instance.indices = []
        return cls.instance
    
    def compile_shader(cls, source, shader_type):
        shader = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)

        if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
            raise RuntimeError(gl.glGetShaderInfoLog(shader).decode('utf-8'))

        return shader

    def create_shader_program(cls, vertex_shader_code, fragment_shader_code):
        vertex_shader = cls.instance.compile_shader(vertex_shader_code, gl.GL_VERTEX_SHADER)
        fragment_shader = cls.instance.compile_shader(fragment_shader_code, gl.GL_FRAGMENT_SHADER)

        shader_program = gl.glCreateProgram()
        gl.glAttachShader(shader_program, vertex_shader)
        gl.glAttachShader(shader_program, fragment_shader)
        gl.glLinkProgram(shader_program)

        if not gl.glGetProgramiv(shader_program, gl.GL_LINK_STATUS):
            raise RuntimeError(gl.glGetProgramInfoLog(shader_program).decode('utf-8'))

        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        return shader_program
    
    def initialize(cls):
        # Vertex data for the cube
        cls.instance.vertices = [
            -0.5, -0.5, 0.0, #0
             0.5, -0.5, 0.0, #1
             0.5,  0.5, 0.0, #2
            -0.5,  0.5, 0.0 #3
        ]

        # Convert the vertices list to a NumPy array
        vertices_array = np.array(cls.instance.vertices, dtype=np.float32)

        # Get a pointer to the NumPy array data
        vertices_pointer = vertices_array.ctypes.data_as(ctypes.POINTER(gl.GLfloat))

        # Indices to form the cube faces
        cls.instance.indices = [
            0, 1, 2,
            2, 3, 0
        ]

        # Convert the indices list to a NumPy array
        indices_array = np.array(cls.instance.indices, dtype=np.uint32)

        # Get a pointer to the NumPy array data
        indices_pointer = indices_array.ctypes.data_as(ctypes.POINTER(gl.GLuint))

        # Shader programs
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

        fragment_shader_code = """
        #version 330 core
        out vec4 FragColor;

        uniform vec4 u_Color;

        void main()
        {
            FragColor = u_Color;
        }
        """

        # Initialize OpenGL
        gl.glEnable(gl.GL_DEPTH_TEST)

        # Compile and link shaders
        cls.instance.shader_program = cls.instance.create_shader_program(vertex_shader_code, fragment_shader_code)

        # Vertex Array Object (VAO)
        cls.instance.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(cls.instance.vao)

        # Vertex Buffer Object (VBO) and Element Buffer Object (EBO)
        cls.instance.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cls.instance.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(cls.instance.vertices) * 4, vertices_pointer, gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        
        cls.instance.ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, cls.instance.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(cls.instance.indices) * 4, indices_pointer, gl.GL_STATIC_DRAW)

        # Use the shader program
        gl.glUseProgram(cls.instance.shader_program)

        # Set up matrices for projection and view
        projection = perspective(45.0, 1920 / 1080, 0.1, 100.0)
        view = translate(0.0, 0.0, -5.0)
        model = identity()

        gl.glUniformMatrix4fv(gl.glGetUniformLocation(cls.instance.shader_program, "projection"), 1, gl.GL_FALSE, projection)
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(cls.instance.shader_program, "view"), 1, gl.GL_FALSE, view)
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(cls.instance.shader_program, "model"), 1, gl.GL_FALSE, model)

    def begin_frame(cls):
        gl.glClearColor(0.8, 0.5, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def end_frame(cls):
        sdl2.SDL_GL_SwapWindow(Application().get_window())

    def draw(cls, model, color):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(cls.instance.shader_program, "model"), 1, gl.GL_FALSE, model)
        gl.glUniform4f(gl.glGetUniformLocation(cls.instance.shader_program, "u_Color"), color[0], color[1], color[2], color[3])
        gl.glBindVertexArray(cls.instance.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(cls.instance.indices), gl.GL_UNSIGNED_INT, None)

    def clean(cls):
        gl.glDeleteVertexArrays(1, (cls.instance.vao,))
        gl.glDeleteBuffers(1, (cls.instance.vbo,))
        gl.glDeleteBuffers(1, (cls.instance.ebo,))
        gl.glDeleteProgram(cls.instance.shader_program)

