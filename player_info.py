import asyncio
import contextlib
import dataclasses
import pathlib
import typing

import aiohttp
from nbt import nbt

UUID_TO_NAME_MOJANG_API = 'https://api.mojang.com/user/profiles/{uuid}/names'


@dataclasses.dataclass
class PlayerInfo:
    uuid: pathlib.Path
    nickname: typing.Optional[str]
    xp: int
    pos: typing.Tuple[float, float, float]


def get_players_info(path_to_world: pathlib.Path):
    player_dat_files = list(
        dat for dat in (path_to_world / 'playerdata').iterdir()
        if dat.suffix == '.dat'
    )
    loop = asyncio.get_event_loop()
    nicknames = loop.run_until_complete(asyncio.gather(
        *(get_nickname_from_uuid(dat.stem) for dat in player_dat_files)
    ))
    player_info = []
    for i, player_dat in enumerate(player_dat_files):
        uuid = player_dat
        name = nicknames[i]
        nbt_file = nbt.NBTFile(str(player_dat), 'rb')
        xp = nbt_file['XpLevel'].value
        pos = tuple(tag.value for tag in nbt_file['Pos'].tags)
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
