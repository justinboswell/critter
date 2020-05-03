import glfw
import ctypes
import OpenGL.GL as gl
import screeninfo

import imgui
from imgui.integrations.glfw import GlfwRenderer


def impl_glfw_init(width, height, window_name):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window

class Window:
    def __init__(self):
        self.window = None
        self.width, self.height = 1280, 720
        try:
            screen = screeninfo.get_monitors()[0]
            width, height = screen.width, screen.height
        except:
            pass
        self.name = "CRiTter Log Analyzer"

    def run(self):
        self.window = impl_glfw_init(self.width, self.height, self.name)
        imgui.create_context()
        impl = GlfwRenderer(self.window)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File", True):

                    clicked_quit, selected_quit = imgui.menu_item(
                        "Quit", 'Cmd+Q', False, True
                    )

                    if clicked_quit:
                        break

                    imgui.end_menu()
                imgui.end_main_menu_bar()

            imgui.show_test_window()

            imgui.begin("Custom window", True)
            imgui.text("Bar")
            imgui.text_colored("Eggs", 0.2, 1., 0.)
            imgui.end()

            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        impl.shutdown()
        glfw.terminate()
