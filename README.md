# mc-change-world-owner

Program for changing Minecraft world owner.

This program is useful when your friend sends you his world in which you played 
together over a LAN, and now you want to continue playing as your character.

The program replaces the player tag from the level.dat file of the world 
with the player tag from the player data file.

The program has CLI (command-line interface) and TUI (terminal user interface). 
TUI is localized in Russian and English.

## CLI

To use the CLI, you must specify at least --action or --uuid parameters

Examples of usage:

```shell script
# get a list of worlds
mc-change-world-owner --action=get-worlds

# get info about players from the "New world" world from Minecraft, located in "~/.minecraft"
mc-change-world-owner --world="New world" --mc-path="~/.minecraft" --action=get-players-info

# transfer the "New world" world to the player with the uuid "0000-0000-0000-0000" (two ways)
mc-change-world-owner --world="New world" --uuid="0000-0000-0000-0000"
mc-change-world-owner --uuid="~/.minecraft/saves/New World/0000-0000-0000-0000.dat"

# transfer the "Old World" world to the player with the uuid "0000-0000-0000-0000" from the "New World" world
mc-change-world-owner --world="~/.minecraft/saves/Old World/level.dat" --uuid="~/.minecraft/saves/New World/0000-0000-0000-0000.dat"
```

## TUI

After starting the program in this mode (it starts by default), a terminal will 
be opened in which the program will ask you to enter some parameters. After 
that, the owner of the world will be changed.

As mentioned earlier, TUI is localized into Russian and English

By specifying the --lang command-line parameter when starting the program, you 
can select the program language. By default, the system language is used.

If you are building the program from source, you need to compile .po files to 
get a translation into Russian.
