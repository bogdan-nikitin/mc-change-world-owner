#mc-friend-world-transfer

```shell script
# get a list of worlds
mc-change-world-owner --action=get-worlds

# get info about players from the "New world" world from Minecraft, located in "~/.minecraft"
mc-change-world-owner --world="New world" --mc-path="~/.minecraft" --action=get-players-info

# transfer the "New world" world to the player with the uuid "0000-0000-0000-0000" (two ways)
mc-change-world-owner --world="New world" --uuid="0000-0000-0000-0000" [--action=change-owner]
mc-change-world-owner --uuid="~/.minecraft/saves/New World/0000-0000-0000-0000.dat" [--action=change-owner]

# transfer the "Old World" world to the player with the uuid "0000-0000-0000-0000" from the "New World" world
mc-change-world-owner --world="~/.minecraft/saves/Old World/level.dat" --uuid="~/.minecraft/saves/New World/0000-0000-0000-0000.dat" [--action=change-owner]
```