# import abc
import argparse
import contextlib
import enum
import pathlib
import sys

from change_world_owner import copy_player_data_to_level_dat
from minecraft_path import minecraft_path
from player_info import get_players_info
from ui.base_ui import BaseUI
from ui.tui import TUI

CLI_DESCRIPTION = '''Program for changing Minecraft world owner.

This program is useful when your friend sends you his world in which you played
together over a LAN, and now you want to continue playing as your character.

The program replaces the player tag from the level.dat file of the world 
with the player tag from the player data file
'''

ACTION_HELP = '''Action to perform.
"change-owner" - change the owner of the world from the --world
parameter to player with the UUID from the --uuid parameter;
the path to the player data file is calculated as *world*/playerdata/*uuid*.dat;
if --uuid is a .dat file, it will be used as the path to the player data file;
if  --uuid is a .dat file and the --world is not specified, then the world in 
which the player's data file is located will be used as the path to the world;
the path to level.dat is calculated as *world*/level.dat;
if --world is a .dat file it will be used as the path to the level.dat.

"get-worlds" - list the worlds.

"get-players-info" - list the UUIDs of the players and their info from the 
world specified in the --world parameter; 
use this to determine the UUID of the new owner
'''
UUID_HELP = '''New owner's UUID or 
path to the new owner's player data file (. dat)'''
WORLD_HELP = '''Name or path to the level.dat of the world whose owner 
you want to change'''
MC_PATH_HELP = 'Path to the Minecraft instance. By default is %(default)s'


class ExitCode(enum.Enum):
    OK = 0
    OTHER_ERROR = 1
    COMMAND_LINE_SYNTAX_ERROR = 2


def print_to_stderr(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


class CommandLineSyntaxError(Exception):
    pass


class BadWorldFormatError(Exception):
    pass


class CLI(BaseUI):
    def __init__(self):
        self.__parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
        self.__args = None
        self.__actions = self._generate_actions()
        self.__default_action = next(iter(self.__actions))
        self.__init_parser()

    @staticmethod
    @contextlib.contextmanager
    def _handle_cli_error():
        try:
            yield
        except CommandLineSyntaxError as e:
            exception = e
            exit_code = ExitCode.COMMAND_LINE_SYNTAX_ERROR
        except Exception as e:
            exception = e
            exit_code = ExitCode.OTHER_ERROR
        else:
            return
        print_to_stderr(exception)
        sys.exit(exit_code.value)

    @staticmethod
    def _print_player_info(player_info):
        print('* UUID:    ', player_info.uuid.stem)
        print('  Nickname:', player_info.nickname or '???')
        print('  XP:      ', player_info.xp)
        print('  XYZ:     ', ' '.join(map(str, player_info.pos)))

    def _get_worlds_action(self):
        for save_path in (self.__args.mc_path / 'saves').iterdir():
            print('*', save_path.stem)

    def _get_players_info_action(self):
        if not self.__args.world:
            raise CommandLineSyntaxError(
                'You must specify the --world argument '
                'if action=get-players-info'
            )
        world_path = self.__args.mc_path / 'saves' / self.__args.world
        for info in get_players_info(world_path):
            self._print_player_info(info)

    def _change_world_owner_action(self):
        # uuid will be specified anyway
        uuid_dat = pathlib.Path(self.__args.uuid)
        if uuid_dat.suffix == '.dat':
            if self.__args.world:
                world_path = pathlib.Path(self.__args.world)
                if world_path.suffix == '.dat':
                    level_dat = world_path
                elif world_path.suffix == '':
                    level_dat = (self.__args.mc_path / 'saves' /
                                 self.__args.world / 'level.dat')
                else:
                    raise BadWorldFormatError(
                        f'World must be dir or .dat, not {world_path.suffix}'
                    )
            else:
                level_dat = uuid_dat.parent.parent / 'level.dat'
        else:
            if not self.__args.world:
                raise CommandLineSyntaxError(
                    'You must specify the --world argument '
                    'if the uuid is not .dat file'
                )
            world_path = self.__args.mc_path / 'saves' / self.__args.world
            uuid_dat = (
                    world_path / 'playerdata' / self.__args.uuid
            ).with_suffix('.dat')
            level_dat = world_path / 'level.dat'

        if not level_dat.exists():
            raise FileNotFoundError(f"{level_dat} does not exist")
        elif not uuid_dat.exists():
            raise FileNotFoundError(f"{uuid_dat} does not exist")

        copy_player_data_to_level_dat(str(level_dat), str(uuid_dat))

    def _generate_actions(self):
        actions = {
            'change-owner': self._change_world_owner_action,  # default
            'get-worlds': self._get_worlds_action,
            'get-players-info': self._get_players_info_action
        }
        return actions

    def __init_parser(self):
        actions = list(self.__actions.keys())
        self.__parser.add_argument(
            '--action', '-a', default=self.__default_action,
            choices=actions, help=ACTION_HELP, dest='action'
        )
        self.__parser.add_argument(
            '--uuid', '-u', help=UUID_HELP, dest='uuid'
        )
        self.__parser.add_argument(
            '--world', '-w', help=WORLD_HELP, dest='world'
        )
        self.__parser.add_argument(
            '--mc-path', default=minecraft_path,
            # this is made because PyCharm creates warnings
            type=lambda s: pathlib.Path(s),
            help=MC_PATH_HELP, dest='mc_path'
        )

    def __parse_args(self):
        self.__args = self.__parser.parse_args()

    def choose_ui(self) -> BaseUI:
        self.__parse_args()
        if self.__args.action != self.__default_action or self.__args.uuid:
            return self
        # TODO: Return GUI
        return TUI()

    def main_loop(self):
        with self._handle_cli_error():
            self.__actions[self.__args.action]()
