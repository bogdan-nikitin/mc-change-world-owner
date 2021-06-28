import argparse
import contextlib
import enum
import pathlib
import sys
import gettext

from change_world_owner import copy_player_data_to_level_dat
from minecraft_path import minecraft_path
from player_info import get_players_info
from ui.base_ui import BaseUI


gettext.install('tui', './lang')


# def get_input(prompt,
#               correctness_predicates=tuple(),
#               incorrectness_predicates=tuple(), convert=None):
#     while True:
#         value = input(prompt)
#         if convert:
#             value = convert(value)
#         for predicate in predicates:
#             msg = predicate(value)
#             if msg:
#                 print(msg)
#                 break
#         else:
#             return value


# def is_dir_predicate(path):
#     if not path.is_dir():
#         return gettext.gettext('Path must be directory')
#
#
# def is_path_exist_predicate(path):
#     if not path.exists():
#         return gettext.gettext('Path must exist')


class TUI(BaseUI):
    @staticmethod
    def _get_mc_path():
        prompt = gettext.gettext(
            'Enter the path to Minecraft '
            '(leave the field empty to use the default value): '
        )
        while True:
            value = input(prompt)
            if not value:
                return minecraft_path
            value = pathlib.Path(value)
            if not value.is_dir():
                print(gettext.gettext('Path must be existing directory'))
            elif not (value / 'saves').is_dir():
                print(gettext.gettext('Directory must contain "saves" folder'))
            else:
                return value

    @staticmethod
    def _get_worlds(mc_path):
        return list((mc_path / 'saves').iterdir())

    # @staticmethod
    # def _print_world(world):

    @staticmethod
    def _print_worlds(worlds):
        worlds_count = len(worlds)
        padding = len(str(worlds_count)) + 1
        for i in range(worlds_count):
            print(f'{i + 1}.'.ljust(padding, ' '), worlds[i].stem)

    @staticmethod
    def _get_world_path(mc_path):
        worlds = TUI._get_worlds(mc_path)
        if not worlds:
            return None
        TUI._print_worlds(worlds)
        prompt = gettext.gettext('Enter the name of the world or its number: ')
        while True:
            value = input(prompt)
            try:
                index = int(value)
                if 1 <= index <= len(worlds):
                    return worlds[index - 1]
                else:
                    print(gettext.gettext(
                        'World num out of range'
                    ).format(len(worlds)))
            except ValueError:
                for world in worlds:
                    if world.stem == value:
                        return world
                print(gettext.gettext('No world with such name'))

    @staticmethod
    def _print_players_info(players_info):
        players_count = len(players_info)
        padding = len(str(len(players_info))) + 2
        for i in range(players_count):
            print(f'{i + 1}.'.ljust(padding - 1, ' '), 'UUID:    ',
                  players_info[i].uuid.stem)
            print(' ' * padding + 'Nickname:',
                  players_info[i].nickname or '???')
            print(' ' * padding + 'XP:      ', players_info[i].xp)
            print(' ' * padding + 'XYZ:     ',
                  ' '.join(map(str, players_info[i].pos)))

    @staticmethod
    def _get_uuid_dat(world_path):
        players_info = get_players_info(world_path)
        TUI._print_players_info(players_info)
        prompt = gettext.gettext(
            'Enter the UUID or number of the player '
            'you want to make the owner of the world: '
        )
        while True:
            value = input(prompt)
            try:
                index = int(value)
                if 1 <= index <= len(players_info):
                    return players_info[index - 1].uuid
                else:
                    print(gettext.gettext('Player num out of range'))
            except ValueError:
                for info in players_info:
                    if info.uuid.stem == value:
                        return info.uuid
                print(gettext.gettext('No such UUID'))

    @staticmethod
    @contextlib.contextmanager
    def _handle_error():
        try:
            yield
        except Exception as e:
            print(gettext.gettext(
                'An error occurred while the program was running: {}'
            ).format(e))

    def main_loop(self):
        with TUI._handle_error():
            mc_path = TUI._get_mc_path()
            world_path = TUI._get_world_path(mc_path)
            if not world_path:
                print(gettext.gettext('No worlds found'))
                return
            level_dat = world_path / 'level.dat'
            if not level_dat.exists():
                print(gettext.gettext('World must contain level.dat file'))
                return
            print(gettext.gettext('Getting players info...'))
            uuid_dat = TUI._get_uuid_dat(world_path)
            copy_player_data_to_level_dat(level_dat, uuid_dat)
            print(gettext.gettext('World owner changed successfully!'))


