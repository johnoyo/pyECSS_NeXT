import OpenGL.GL as gl

class Shader:
    def create(self):
        pass

    def bind(self):
        pass

    def unbind(self):
        pass

    def set_int_1(self):
        pass

    def set_int_ptr(self):
        pass

    def set_float_1(self):
        pass

    def set_float_2(self):
        pass

    def set_float_3(self):
        pass

    def set_float_4(self):
        pass

    def set_float_ptr(self):
        pass

    def set_mat_4(self):
        pass

    def set_buffer(self):
        pass

class ShaderLib(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ShaderLib, cls).__new__(cls)
            cls.instance.shaders = {}
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
    
    def build(cls, name: str, vertex_shader_code: str, fragment_shader_code: str):
        if cls.instance.shaders.get(name) != None:
            return cls.instance.shaders.get(name)

        shader_program = cls.instance.create_shader_program(vertex_shader_code, fragment_shader_code)
        cls.instance.shaders[name] = shader_program
        
        return shader_program

    def get(cls, name: str):
        return cls.instance.shaders.get(name)