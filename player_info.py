import asyncio
import contextlib
import pathlib
import typing
from dataclasses import dataclass

import aiohttp

import nbt_py.fileio
from nbt_utils import walk_path_nbt

UUID_TO_NAME_MOJANG_API = 'https://api.mojang.com/user/profiles/{uuid}/names'


@dataclass
class PlayerInfo:
    uuid: str
    name: typing.Optional[str]
    xp: int
    pos: typing.Tuple[float, float, float]


def get_players_info(path_to_world):
    path_to_world = pathlib.Path(path_to_world)
    player_dat_files = list((path_to_world / 'playerdata').iterdir())
    loop = asyncio.get_event_loop()
    nicknames = loop.run_until_complete(asyncio.gather(
        *(get_nickname_from_uuid(dat.stem) for dat in player_dat_files)
    ))
    player_info = []
    for i, player_dat in enumerate(player_dat_files):
        uuid = player_dat.stem
        name = nicknames[i]
        nbt = nbt_py.fileio.load_and_parse_nbt_file(str(player_dat))
        xp = walk_path_nbt(nbt, 'XpLevel')
        pos = tuple(walk_path_nbt(nbt, 'Pos').payload)
        player_info += [PlayerInfo(uuid, name, xp, pos)]

    return player_info


async def get_nickname_from_uuid(uuid):
    await asyncio.sleep(5)
    with contextlib.suppress(Exception):
        async with aiohttp.ClientSession() as session:
            url = UUID_TO_NAME_MOJANG_API.format(uuid=uuid)
            async with session.get(url) as response:
                json = await response.json()
                return json[0]['name']
    return None
