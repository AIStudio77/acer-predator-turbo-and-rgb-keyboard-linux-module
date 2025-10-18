import os
from typing import List, Optional, Tuple

from time import sleep as sleep

mode_choice: Optional[int] = None
zone_list: List[int] = []
speed_choice: Optional[int] = None
bright_choice: Optional[int] = None
direction_choice: Optional[int] = None
color_choice: Optional[Tuple[int, int, int]] = None
final_command: List[str] = []


def reset_state() -> None:
    global mode_choice, zone_list, speed_choice, bright_choice, direction_choice, color_choice, final_command
    mode_choice = None
    zone_list = []
    speed_choice = None
    bright_choice = None
    direction_choice = None
    color_choice = None
    final_command = []


def setup() -> None:
    if not os.path.exists(".keyboard_cache"):
        os.system("touch .keyboard_cache")


def prep() -> None:
    global final_command
    final_command.clear()
    command_parts: List[str] = ["./facer_rgb.py"]
    if mode_choice is not None:
        command_parts.extend(["-m", str(mode_choice)])
    if speed_choice is not None:
        command_parts.extend(["-s", str(speed_choice)])
    if bright_choice is not None:
        command_parts.extend(["-b", str(bright_choice)])
    if direction_choice is not None:
        command_parts.extend(["-d", str(direction_choice)])
    if color_choice is not None:
        red, green, blue = color_choice
        command_parts.extend(
            [
                "-cR",
                str(red),
                "-cG",
                str(green),
                "-cB",
                str(blue),
            ]
        )
    base_command = " ".join(command_parts)
    if zone_list:
        for zone in zone_list:
            final_command.append(f"{base_command} -z {zone}")
    else:
        final_command.append(base_command)


def speed() -> None:
    global speed_choice
    try:
        choice = int(
            input(
                "Enter the Value of Speed [0-9] \n0 -> Static\n1 -> Slowest\n9 -> Fastest\nJust Press Enter to use the Default Value:"
            )
        )
    except ValueError:
        os.system("clear")
        return None
    if choice < 0 or choice > 9:
        print("Invalid Choice. Try again")
        sleep(1.5)
        os.system("clear")
        speed()
    else:
        speed_choice = choice
        os.system("clear")


def bright() -> None:
    global bright_choice
    try:
        choice = int(
            input(
                "Enter the Value of Brightness [0-100]\n0 -> Switched Off\n100 -> Brightest\nJust Press Enter to use the Default Value:"
            )
        )
    except ValueError:
        os.system("clear")
        return None
    if choice < 0 or choice > 100:
        print("Invalid Choice. Try again")
        sleep(1.5)
        os.system("clear")
        bright()
    else:
        bright_choice = choice
        os.system("clear")


def direction() -> None:
    global direction_choice
    try:
        choice = int(
            input(
                "Enter the Direction of Animation [1/2]"
                "\n1 -> Right to Left"
                "\n2 -> Left to Right"
                "\nJust Press Enter to use the Default Value:"
            )
        )
    except ValueError:
        os.system("clear")
        return None
    if choice not in [1, 2]:
        print("Invalid Choice. Try again")
        sleep(1.5)
        os.system("clear")
        direction()
    else:
        direction_choice = choice
        os.system("clear")


def zone() -> None:
    global zone_list
    zones = input(
        "Enter the Zone ID(s) you want to select (1-4) seperated by space"
        "\nIf you want to select all the zones just press Enter:"
    )
    if len(zones) == 0:
        os.system("clear")
        zone_list = [1, 2, 3, 4]
        return None
    z_list = list(map(lambda x: int(x), zones.split()))
    if len(z_list) < 5 and set(z_list).issubset({1, 2, 3, 4}):
        zone_list = z_list
        os.system("clear")
    else:
        print("Invalid Selection, Choose Again")
        sleep(1.5)
        os.system("clear")
        zone()


def color() -> None:
    global color_choice
    raw = input(
        "Enter a Valid RGB code with all the channels seperated by space"
        "\nExample: 255 255 255"
        "\nJust Press Enter to use the Default Color (White):"
    )
    if len(raw) == 0:
        color_choice = (255, 255, 255)
        os.system("clear")
        return None
    inter = raw.split(" ")
    values = []
    try:
        for i in inter:
            if i == "":
                continue
            elif i != "" and (int(i) < 0 or int(i) > 255):
                print("RGB values should be between 0 - 255")
                sleep(1.5)
                os.system("clear")
                color()
            else:
                values.append(int(i))
    except ValueError:
        print("Invalid Values. Try Again!")
        sleep(1.5)
        os.system("clear")
        color()
    if len(values) != 3:
        print("There are 3 channels")
        sleep(1.5)
        os.system("clear")
        color()
    color_choice = (values[0], values[1], values[2])
    os.system("clear")


def rerun() -> Optional[bool]:
    # This is different from the refresh.sh and should not be considered redundant
    # If we are using the Zones Function, then the current script will run multiple commands to match
    # all the zones the user has specifies but in this case the refresh will only run the last command.
    if not os.path.exists(".keyboard_cache"):
        print("No cached commands found.")
        sleep(1.5)
        os.system("clear")
        return False
    with open(".keyboard_cache", "r", encoding="utf-8") as file:
        cached_commands = [command for command in file.read().split(",") if command]
    for command in cached_commands:
        os.system(command)
    exit()


def run() -> None:
    global final_command
    if not final_command:
        return None
    for i in final_command:
        os.system(i)
    with open(".keyboard_cache", "w", encoding="utf-8") as file:
        file.write(",".join(final_command))


def mode() -> None:
    global mode_choice
    print("Choose the RGB Mode")
    print("1. Static")
    print("2. Breathing")
    print("3. Neon")
    print("4. Wave")
    print("5. Shifting")
    print("6. Zoom")
    print("7. Re-Run the Last Command")
    print("0. Exit")
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            os.system("clear")
            mode_choice = 0
            zone()
            color()
        elif choice == 2:
            os.system("clear")
            mode_choice = 1
            speed()
            bright()
            color()
        elif choice == 3:
            os.system("clear")
            mode_choice = 2
            speed()
            bright()
        elif choice == 4:
            os.system("clear")
            mode_choice = 3
            speed()
            bright()
            direction()
        elif choice == 5:
            os.system("clear")
            mode_choice = 4
            speed()
            bright()
            color()
            direction()
        elif choice == 6:
            os.system("clear")
            mode_choice = 5
            speed()
            bright()
            color()
        elif choice == 7:
            os.system("clear")
            if rerun() is False:
                mode()
                return None
        elif choice == 0:
            os.system("clear")
            exit()
        else:
            print("Invalid Choice")
            sleep(2)
            os.system("clear")
            mode()
    except ValueError:
        print("Invalid Values. Try Again")
        sleep(1.5)
        os.system("clear")
        mode()


def start() -> None:
    try:
        os.system("clear")
        reset_state()
        setup()
        mode()
        prep()
        run()
    except KeyboardInterrupt:
        print("\nExiting the Program")
        exit()


if __name__ == "__main__":
    start()
