from mr_dapa.drawers.drawers import *

def interactive_menu(options):
    while True:
        print("\n" + "-" * 30)
        for idx, option in enumerate(options):
            print(f"[{idx}]: {option['name']}")
        print("[q]: Quit")
        print("[a]: Run All")
        choice = input("Choose an option: ").strip().lower()

        if choice == 'q':
            print("Exiting...")
            break
        elif choice == 'a':
            print("\nRunning all options...\n")
            for option in options:
                print(f"Running: {option['name']}...")
                option['action']()
            print("\nAll tasks completed.")
            break
        elif choice.isdigit() and 0 <= int(choice) < len(options):
            selected = options[int(choice)]
            print(f"\nRunning: {selected['name']}...\n")
            selected['action']()
        else:
            print("Invalid input. Please try again.")


def interactive_selection(options):
    print("Select options:")
    for idx, option in enumerate(options):
        print(f"[{idx}]: {option}")
    choice = input("Choose options (separated by comma): ").strip().lower()
    selected_options = [options[int(choice)] for choice in choice.split(',')]
    return selected_options


def find_files(folder: str, ptn: str, max_num: int = 1):
    files = glob.glob(os.path.join(folder, ptn))
    assert len(files) > 0, "No files found with pattern {}".format(ptn)
    print(f"Directories found: {files}")
    max_num = min(max_num, len(files))
    return [d for d in sorted(files)[:max_num]]


def main_with_interactive_menu():
    files = interactive_selection(find_files('data', 'data_*.json', 10))

    menu_options = [
        {
            'name': 'X & Y, All Robots',
            'action': lambda: StaticGlobalPlotDrawer(files).draw(['x', 'y'])
        },
        {
            'name': 'Yaw Angles, All Robots, First two seconds',
            'action': lambda: StaticGlobalPlotDrawer(files).draw(['yaw'], first_seconds=2)
        },
        {
            'name': 'Battery Level, Robot #1 & #3',
            'action': lambda: StaticGlobalPlotDrawer(files).draw(['batt'], id_list=[1, 3])
        },
        {
            'name': 'Battery Level, All Robots',
            'action': lambda: StaticSeparatePlotDrawer(files).draw(['batt'])
        },
        {
            'name': 'X & Y Value, Per Robot',
            'action': lambda: StaticSeparatePlotDrawer(files).draw(['x', 'y'])
        },
        {
            'name': 'All Values, Grouped',
            'action': lambda: StaticGroupPlotDrawer(files).draw(['x', 'y', 'yaw', 'batt'])
        },
        {
            'name': 'X & Y, Grouped, Last 2 Seconds',
            'action': lambda: StaticGroupPlotDrawer(files).draw(['cvt'])
        },
        {
            'name': 'Battery Level, Grouped',
            'action': lambda: StaticGroupPlotDrawer(files).draw(['batt'])
        },
        {
            'name': 'Animation (Map)',
            'action': lambda: AnimationDrawer(files).draw(['map'])
        },
        {
            'name': 'Animation (Map, Last 3 Seconds)',
            'action': lambda: AnimationDrawer(files).draw(['map'], last_seconds=3)
        },
        {
            'name': 'Animation (Map, Certain Time Range)',
            'action': lambda: AnimationDrawer(files).draw(['map'], time_range=(2, 3))
        },
        {
            'name': 'Animation (Map & Battery)',
            'action': lambda: AnimationDrawer(files).draw(['map', 'batt'])
        },
        {
            'name': 'Animation (Map & Battery, Last 2 Seconds)',
            'action': lambda: AnimationDrawer(files).draw(['map', 'batt'], last_seconds=5)
        },
        {
            'name': 'Animation (Map & Battery, Certain Time Range)',
            'action': lambda: AnimationDrawer(files).draw(['map', 'batt'], time_range=(2, 3))
        },
        {
            'name': 'Animation (Full Set, Certain Time Range, #1 Only)',
            'action': lambda: AnimationDrawer(files).draw(
                ['map', 'x', 'y', 'yaw', 'batt'],
                time_range=(0.2, 0.5),
                id_list=[1]
            )
        },
    ]

    interactive_menu(menu_options)

if __name__ == '__main__':
    main_with_interactive_menu()