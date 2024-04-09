import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import math
import pygetwindow as gw
import pymem
import utility
import webbrowser
import threading
import time
import sys

rapid_int_change_on = False

address_names = {
    "Main-Weapon": "Main-Weapon",
    "Q-Weapon": "Q-Weapon",
    "Q-Down-Weapon": "Q-Down-Weapon",
    "W-Weapon": "W-Weapon",
    "W-Down-Weapon": "W-Down-Weapon",
    "E-Weapon": "E-Weapon",
    "E-Down-Weapon": "E-Down-Weapon",
    "Damage": "Damage",
    "Power-Damage": "Power-Damage",
    "Speed": "Speed",
    "Memoria": "Memoria",
    "Bolts": "Bolts",
    "Titan-Shards": "Titan-Shards"
}

process = pymem.Pymem("30XX.exe")

LocalPlayerOffset = process.base_address + 0x99A260
MainWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x594])
QWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x1FA8])
QDownWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x1FC0])
WWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x1FAC])
WDownWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x1FA8])
EWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x1FB0])
EDownWeaponPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x1FC8])
DamagePointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x610])
PowerDamagePointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x640])
SpeedPointer = utility.FindDMAAddy(process.process_handle, LocalPlayerOffset, [0x5F8])
HealthAddress = process.base_address + 0x43E107
EnergyAddress = process.base_address + 0x4E6D3B
InstantKillAddress = process.base_address + 0x4E6355
InstantKillRAddress = process.base_address + 0x4E635C
ColorCyclePointer = process.base_address + 0x49A037C
BypassColorAddress = process.base_address + 0x408A86
MemoriaAddress = process.base_address + 0x99A078
BoltsAddress = process.base_address + 0x49D6DEC
TitanShardsAddress = process.base_address + 0x997DE8
SeedAddress = process.base_address + 0x49DE511
ComboAddress = process.base_address + 0x5425EB
ComboRAddress = process.base_address + 0x5425EF

addresses = [MainWeaponPointer, QWeaponPointer, QDownWeaponPointer, WWeaponPointer, WDownWeaponPointer,
             EWeaponPointer, EDownWeaponPointer, DamagePointer, PowerDamagePointer, SpeedPointer, MemoriaAddress,
             BoltsAddress, TitanShardsAddress]
original_values = [process.read_int(address) for address in addresses]
values_set_to_zero = [False] * len(addresses)


def init_imgui(window):
    imgui.create_context()
    impl = GlfwRenderer(window)
    imgui.style_colors_dark()
    return impl


bypass_color_flag = False
Unlimited_Energy_Flag = False
God_Mode_Flag = False
Instant_Kill_Flag = False
Unlimited_Combo_Flag = False


def toggle_bypass_color_flag():
    global bypass_color_flag
    bypass_color_flag = not bypass_color_flag


def toggle_unlimited_energy():
    global Unlimited_Energy_Flag
    Unlimited_Energy_Flag = not Unlimited_Energy_Flag


def toggle_god_mode():
    global God_Mode_Flag
    God_Mode_Flag = not God_Mode_Flag


def toggle_instant_kill():
    global Instant_Kill_Flag
    Instant_Kill_Flag = not Instant_Kill_Flag


def toggle_Unlimited_Combo():
    global Unlimited_Combo_Flag
    Unlimited_Combo_Flag = not Unlimited_Combo_Flag


def render_about_window():
    imgui.begin("About")
    if imgui.button("The Mod Menu Maintainer's YouTube Channel"):
        webbrowser.open("https://www.youtube.com/channel/UCAXpJbKZC9G41TRl5yMRawQ?sub_confirmation=1")
    if imgui.button("Learn Everything About Game Hacking."):
        webbrowser.open("https://www.youtube.com/watch?v=9RxJmoHk-y8")
    color2 = [
        math.sin(glfw.get_time() * 2.0) * 0.5 + 0.5,
        math.sin(glfw.get_time() * 3.0) * 0.5 + 0.5,
        math.sin(glfw.get_time() * 1.0) * 0.5 + 0.5,
        1.0
    ]
    imgui.text_colored("Cheat the game because it doesn't mind cheating you. ~ CTG", *color2)
    if imgui.button("Learn Cheat Engine"):
        webbrowser.open("https://www.youtube.com/@ChrisFayte?sub_confirmation=1")
    if imgui.button("Learn More Cheat Engine / Reverse Engineering"):
        webbrowser.open("www.youtube.com/@StephenChapman?sub_confirmation=1")
    imgui.end()


about_window_open = False



def toggle_about_window():
    global about_window_open
    about_window_open = not about_window_open



def show_about_window():
    toggle_about_window()


def render_imgui(impl, values):
    global about_window_open
    imgui.new_frame()
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("IX v0.0.1 SynX Edition, Made By YT_SyntaXError305, @SyntaxError305 On YouTube. Last Updated: 4/9/2024.",  True):
            clicked_quit, selected_quit = imgui.menu_item("Quit", 'Cmd+Q', False, True)
            if clicked_quit:
                sys.exit()
            imgui.end_menu()
        imgui.end_main_menu_bar()

    imgui.begin("Main Menu", True)

    for i, address_key in enumerate(address_names.keys()):
        changed, value = imgui.input_int(f"{address_key}", values[i])
        if changed:
            values[i] = value
            if value == 0 and not values_set_to_zero[i]:
                process.write_int(addresses[i], original_values[i])
                values_set_to_zero[i] = True
            elif value != 0 and values_set_to_zero[i]:
                values_set_to_zero[i] = False

            if value != 0:
                process.write_int(addresses[i], value)

    for i, value in enumerate(values):
        color = [math.sin(glfw.get_time() * 2.0) * 0.5 + 0.5,
                 math.sin(glfw.get_time() * 3.0) * 0.5 + 0.5,
                 math.sin(glfw.get_time() * 1.0) * 0.5 + 0.5, 1.0]
        imgui.text_colored(f"{list(address_names.values())[i]}: {value}", *color)

    if rapid_int_change_on:
        imgui.text_colored("RainBow-Character: ON", *color)
    else:
        imgui.text("RainBow-Character: OFF")

    if imgui.button("Toggle-Rainbow-Character"):
        toggle_rapid_int_change()

    if imgui.button("Bypass Color"):
        toggle_bypass_color_flag()

    if imgui.button("Unlimited Power"):
        toggle_unlimited_energy()

    if imgui.button("God-Mode"):
        toggle_god_mode()

    if imgui.button("Instant-Kill"):
        toggle_instant_kill()

    if imgui.button("Unlimited-Combo"):
        toggle_Unlimited_Combo()

    if imgui.button("Fly-Hack"):
        print("Fly-Hack-Place-Holder")


    if imgui.button("About"):
        toggle_about_window()


    if about_window_open:
        render_about_window()

    if Instant_Kill_Flag:
        process.write_bytes(InstantKillAddress, b"\x48\xB8\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", 10)
    else:
        process.write_bytes(InstantKillAddress, b"\x48\x8B\x83\xB8\x01\x00\x00", 7)
        process.write_bytes(InstantKillRAddress, b"\x48\x2B\xC5", 3)

    if bypass_color_flag:
        process.write_bytes(BypassColorAddress, b"\x75\x1A", 2)
    else:
        process.write_bytes(BypassColorAddress, b"\x74\x1A", 2)

    if Unlimited_Energy_Flag:
        process.write_bytes(EnergyAddress, b"\x90\x90\x90\x90\x90\x90\x90", 7)
    else:
        process.write_bytes(EnergyAddress, b"\x48\x29\x9F\xE8\x01\x00\xf0", 7)

    if God_Mode_Flag:
        process.write_bytes(HealthAddress, b"\x90\x90\x90", 3)
    else:
        process.write_bytes(HealthAddress, b"\x48\x2B\xCF", 3)

    if Unlimited_Combo_Flag:
        process.write_bytes(ComboAddress, b"\xC7\x43\x1C\x35\x82\x00\x00", 7)
    else:
        process.write_bytes(ComboAddress, b"\x44\x8B\x7B\x1C", 4)
        process.write_bytes(ComboRAddress, b"\xC6\x05\xF1", 3)

    imgui.end()

    imgui.render()
    impl.process_inputs()
    impl.render(imgui.get_draw_data())


def toggle_rapid_int_change():
    global rapid_int_change_on
    rapid_int_change_on = not rapid_int_change_on
    if rapid_int_change_on:
        threading.Thread(target=rapid_int_change_thread).start()


def rapid_int_change_thread():
    value = 0
    while rapid_int_change_on:
        process.write_int(ColorCyclePointer, value)
        value = (value + 1) % 13
        if value == 0:
            value = 1
        time.sleep(0.1)


def main():
    menu_visible = True

    if not glfw.init():
        return -1

    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.FOCUSED, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)  
    window = glfw.create_window(1920, 1080, "Python Developer Menu", None, None)#Change This To Your Display / Monitor Resolution
    if not window:
        glfw.terminate()
        return -1

    glfw.make_context_current(window)

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    impl = init_imgui(window)

    values = [0] * len(address_names)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if glfw.get_key(window, glfw.KEY_INSERT) == glfw.PRESS:
            menu_visible = not menu_visible
            if menu_visible:
                pywindow = gw.getWindowsWithTitle("Python Developer Menu")[0]
                pywindow.activate()

        if menu_visible:
            render_imgui(impl, values)

        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

    return 0


if __name__ == "__main__":
    main()

