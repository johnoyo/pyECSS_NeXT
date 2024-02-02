import OpenGL.GL as gl
import sdl2
import sdl2.ext

class Application(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Application, cls).__new__(cls)
            cls.instance.window = None
            cls.instance.window_title = 'Title'
            cls.instance.window_width = 1920
            cls.instance.window_height = 1080
            cls.instance.context = None
            cls.instance.is_application_running = False
        return cls.instance
    
    def get_window(cls):
        return cls.instance.window
    
    def is_running(cls):
        return cls.instance.is_application_running
    
    def create(cls, title, width, height, vsync = True):
        sdl_not_initialised = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_TIMER)
        if sdl_not_initialised !=0:
            print("SDL2 could not be initialised! SDL Error: ", sdl2.SDL_GetError())
            exit(1)
        
        #setting OpenGL attributes for the GL state
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)

        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)

        cls.instance.window_title = title
        cls.instance.window_width = width
        cls.instance.window_height = height

        cls.instance.window = sdl2.SDL_CreateWindow(cls.instance.window_title.encode(), sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, cls.instance.window_width, cls.instance.window_height, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_SHOWN)

        if cls.instance.window is None:
            print("Window could not be created! SDL Error: ", sdl2.SDL_GetError())
            exit(1)

        cls.instance.context = sdl2.SDL_GL_CreateContext(cls.instance.window)
        if cls.instance.context is None:
            print("OpenGL Context could not be created! SDL Error: ", sdl2.SDL_GetError())
            exit(1)

        sdl2.SDL_GL_MakeCurrent(cls.instance.window, cls.instance.context)
        if sdl2.SDL_GL_SetSwapInterval(1) < 0:
            print("Warning: Unable to set VSync! SDL Error: ", sdl2.SDL_GetError())
            exit(1)

        #obtain the GL versioning system info
        gVersionLabel = f'OpenGL {gl.glGetString(gl.GL_VERSION).decode()} GLSL {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()} Renderer {gl.glGetString(gl.GL_RENDERER).decode()}'
        print(gVersionLabel)

        cls.instance.is_application_running = True

    def quit(cls):
        cls.instance.is_application_running = False

    def clean(cls):
        if (cls.instance.context and cls.instance.window is not None):
            sdl2.SDL_GL_DeleteContext(cls.instance.context)
            sdl2.SDL_DestroyWindow(cls.instance.window)
            sdl2.SDL_Quit()