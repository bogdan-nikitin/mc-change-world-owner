from ui.cli import CLI


def main():
    world_changer = CLI()
    world_changer = world_changer.choose_ui()
    world_changer.main_loop()


if __name__ == '__main__':
    main()
