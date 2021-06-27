import argparse
import abc
import pathlib

from ui.base_ui import BaseUi
from minecraft_path import minecraft_path
from change_world_owner import copy_player_data_to_level_dat

CLI_DESCRIPTION = '''Program for changing Minecraft World Owner

This program is useful when your friend sends you his world in which you played
together over a LAN, and now you want to continue playing your character
'''


class Cli(BaseUi):
    def __init__(self):
        self.__parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
        self.__args = None
        self.__actions = self._generate_actions()
        self.__default_action = next(iter(self.__actions))
        self.__init_parser()

    def get_worlds(self):
        pass

    def get_players_info(self):
        pass

    def change_world_owner(self):
        # uuid will be specified anyway
        uuid_dat = pathlib.Path(self.__args.uuid)
        if uuid_dat.suffix == '.dat':
            if self.__args.world:
                world_path = pathlib.Path(self.__args.world)
                if world_path.suffix == '.dat':
                    level_dat = world_path
                elif world_path.suffix == '':
                    level_dat = (self.__args.mc_path / self.__args.world /
                                 'level.dat')
                else:
                    # TODO: Custom exception
                    raise Exception('World must be dir or .dat')
            else:
                level_dat = uuid_dat.parent.parent / 'level.dat'
        else:
            if not self.__args.world:
                raise Exception(
                    'You must specify the --world argument '
                    'if the uuid is not .dat file'
                )
            world_path = self.__args.mc_path / self.__args.world
            uuid_dat = world_path / self.__args.uuid
            level_dat = world_path / 'level.dat'

        copy_player_data_to_level_dat(str(level_dat), str(uuid_dat))

    def _generate_actions(self):
        actions = {
            'change-owner': self.change_world_owner,  # default
            'get-worlds': self.get_worlds,
            'get-players-info': self.get_players_info
        }
        return actions

    def __init_parser(self):
        actions = list(self.__actions.keys())
        self.__parser.add_argument(
            '--action', '-a', default=self.__default_action,
            choices=actions, dest='action'
        )
        self.__parser.add_argument(
            '--mc-path', default=minecraft_path,
            # this is made because PyCharm creates warnings
            type=lambda s: pathlib.Path(s),
            dest='mc_path'
        )
        self.__parser.add_argument(
            '--world', '-w', dest='world'
        )
        self.__parser.add_argument(
            '--uuid', '-u', dest='uuid'
        )

    def __parse_args(self):
        self.__args = self.__parser.parse_args()

    def choose_interaction_interface(self):
        self.__parse_args()
        return self

    def main_loop(self):
        self.__actions[self.__args.action]()
