import pathlib

from nbt import nbt


def change_world_owner(path_to_world, new_owner_uuid):
    path_to_world = pathlib.Path(path_to_world)
    new_owner_dat = pathlib.Path(new_owner_uuid).with_suffix('.dat')
    level_dat_path = path_to_world / 'level.dat'
    new_owner_dat_path = path_to_world / 'playerdata' / new_owner_dat
    copy_player_data_to_level_dat(str(level_dat_path), str(new_owner_dat_path))


def copy_player_data_to_level_dat(level_dat: str, uuid_dat: str):
    level_dat_nbt = nbt.NBTFile(level_dat, 'rb')
    new_owner_nbt = nbt.NBTFile(uuid_dat, 'rb')
    level_dat_nbt["Data"]["Player"] = new_owner_nbt
    level_dat_nbt.write_file()
