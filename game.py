import importlib
import pkgutil
import sys
import turtle


def get_freegames_list():
    """Return sorted game module names inside the `freegames` package."""
    try:
        import freegames
    except ImportError:
        print("Error: 'freegames' is not installed.")
        print("Install it with: pip install freegames")
        sys.exit(1)

    games = []
    package_path = getattr(freegames, "__path__", None)
    if package_path:
        for _, name, is_pkg in pkgutil.iter_modules(package_path):
            if not is_pkg and not name.startswith("_"):
                games.append(name)

    return sorted(games)


def launch_game(game_name):
    """Import and run a `freegames.<game_name>` module."""
    module_name = f"freegames.{game_name}"
    try:
        # Reset turtle state so re-running games doesn't carry over old windows/handlers
        turtle.TurtleScreen._RUNNING = True
        try:
            turtle.clearscreen()
        except turtle.Terminator:
            pass

        if module_name in sys.modules:
            mod = importlib.reload(sys.modules[module_name])
        else:
            mod = importlib.import_module(module_name)

        # Many freegames modules call `done()` or `mainloop()` on import;
        # if a `main()` function is exposed and wasn't auto-run, invoke it.
        if hasattr(mod, "main") and callable(mod.main):
            try:
                mod.main()
            except turtle.Terminator:
                pass

    except turtle.Terminator:
        print(f"\nClosed '{game_name}'.")
    except Exception as exc:
        print(f"\nCould not launch '{game_name}': {exc}")


def main():
    games = get_freegames_list()
    if not games:
        print("No games found inside 'freegames'.")
        sys.exit(1)

    while True:
        print("\n=== Python FreeGames Launcher ===")
        for idx, name in enumerate(games, start=1):
            label = name.replace("_", " ").title()
            print(f"  {idx:2d}. {label} ({name})")
        print("   q. Quit")

        choice = input("\nSelect a game number (or 'q' to quit): ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Goodbye!")
            break

        if not choice.isdigit():
            print("Please enter a valid number from the list or 'q'.")
            continue

        index = int(choice) - 1
        if 0 <= index < len(games):
            selected = games[index]
            print(f"\nLaunching {selected}...")
            launch_game(selected)
        else:
            print(f"Please choose a number between 1 and {len(games)}.")


if __name__ == "__main__":
    main()
