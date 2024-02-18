import OpenGL.GL as gl
import glfw

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
            cls.instance.delta_time = 0.0
            cls.instance.last_time = 0.0
            cls.instance.timer = 0.0
            cls.instance.frames = 0.0
        return cls.instance
    
    def get_window(cls):
        return cls.instance.window
    
    def is_running(cls):
        return cls.instance.is_application_running
    
    def set_is_running(cls, is_running):
        cls.instance.is_application_running = is_running
    
    def create(cls, title, width, height, vsync = True):
        # Initialize GLFW
        if not glfw.init():
            print("GLFW could not be initialized!")
            exit(-1)

        # Set GLFW window hints
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

        cls.instance.window_title = title
        cls.instance.window_width = width
        cls.instance.window_height = height

        # Create a windowed mode window and its OpenGL context
        cls.instance.window = glfw.create_window(width, height, title, None, None)
        if not cls.instance.window:
            print("Window could not be created!")
            glfw.terminate()
            exit(-1)

        # Make the window's context current
        glfw.make_context_current(cls.instance.window)

        # Obtain the GL versioning system info
        gVersionLabel = f'OpenGL {gl.glGetString(gl.GL_VERSION).decode()} GLSL {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()} Renderer {gl.glGetString(gl.GL_RENDERER).decode()}'
        print(gVersionLabel)

    def calculate_time_step(cls):
        time = glfw.get_time()
        cls.instance.delta_time = time - cls.instance.last_time
        cls.instance.last_time = time

    def dispatch_main_loop(cls, main_loop):
        while cls.instance.is_application_running:            
            cls.instance.start_frame()
            main_loop(cls.instance.delta_time)
            cls.instance.end_frame()

    def start_frame(cls):
        cls.instance.calculate_time_step()

    def end_frame(cls):
        # Calculate fps
        cls.instance.frames += 1
        if glfw.get_time() - cls.instance.timer > 1.0:
            glfw.set_window_title(cls.instance.window, f'[FPS: {cls.instance.frames}]')
            cls.instance.timer += 1
            cls.instance.frames = 0

        # Swap front and back buffers
        glfw.swap_buffers(cls.instance.window)

        # Poll for and process events
        glfw.poll_events()

    def quit(cls):
        cls.instance.is_application_running = False

    def clean(cls):
        if (cls.instance.window is not None):
            glfw.destroy_window(cls.instance.window)
            glfw.terminate()