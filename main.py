# Import necessary libraries
import glfw  # GLFW for window creation and event handling
import OpenGL.GL as gl  # OpenGL for rendering
import imgui  # Dear ImGui for GUI
from imgui.integrations.glfw import GlfwRenderer  # Dear ImGui renderer for GLFW
import pymem  # Pymem for memory manipulation

# Initialize pymem process for "Barony.exe" and calculate address for memory manipulation
process = pymem.Pymem("Barony.exe")
RapidAddress = process.base_address + 0x1C0AE4

# Function to initialize Dear ImGui
def init_imgui(window):
    imgui.create_context()  # Create Dear ImGui context
    impl = GlfwRenderer(window)  # Create Dear ImGui renderer for GLFW
    imgui.style_colors_dark()  # Set dark style for Dear ImGui
    return impl

# Function to render Dear ImGui interface
def render_imgui(impl):
    global Rapid_Melee_Flag  # Declare global flag variable
    imgui.new_frame()  # Start a new Dear ImGui frame
    imgui.begin("IX Menu Barony V0.0.1", True)  # Begin Dear ImGui window
    
    # Check if "Toggle Rapid-Melee" button is clicked
    if imgui.button("Toggle Rapid-Melee"):
        toggle_Rapid_Melee_Flag()  # Toggle the flag when the button is clicked
    
    # Write bytes to RapidAddress based on flag status
    if Rapid_Melee_Flag:
        process.write_bytes(RapidAddress, b"\x90\x90\x90\x90\x90\x90\x90", 7)  # Write bytes when flag is True
    else:
        process.write_bytes(RapidAddress, b"\x44\x89\xA6\xE0\x02\x00\x00", 7)  # Write bytes when flag is False

    imgui.end()  # End Dear ImGui window
    
    imgui.render()  # Render Dear ImGui
    impl.process_inputs()  # Process inputs for Dear ImGui
    impl.render(imgui.get_draw_data())  # Render Dear ImGui draw data

# Global flag variable
Rapid_Melee_Flag = False

# Function to toggle Rapid_Melee_Flag
def toggle_Rapid_Melee_Flag():
    global Rapid_Melee_Flag
    Rapid_Melee_Flag = not Rapid_Melee_Flag  # Toggle the flag value

# Main function
def main():
    if not glfw.init():  # Initialize GLFW
        return -1

    # Set window hints for GLFW
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)

    # Create GLFW window
    window = glfw.create_window(800, 600, "Memory Writer", None, None)
    if not window:  # Check if window creation failed
        glfw.terminate()  # Terminate GLFW
        return -1

    glfw.make_context_current(window)  # Set current context to the window

    # Enable blending for transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # Initialize Dear ImGui
    impl = init_imgui(window)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()  # Poll for events
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # Clear color buffer

        # Render Dear ImGui interface
        render_imgui(impl)

        glfw.swap_buffers(window)  # Swap buffers

    impl.shutdown()  # Shutdown Dear ImGui
    glfw.terminate()  # Terminate GLFW

    return 0

# Entry point
if __name__ == "__main__":
    main()  # Call main function if script is executed directly

