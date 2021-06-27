from ui.cli import Cli


def main():
    world_changer = Cli()
    world_changer = world_changer.choose_interaction_interface()
    world_changer.main_loop()


if __name__ == '__main__':
    main()
