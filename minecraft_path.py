import pathlib
import platform


def get_minecraft_path():
    system = platform.system()
    if system == 'Windows':
        return pathlib.Path.home() / 'AppData' / 'Roaming' / '.minecraft'
    elif system == 'Darwin':
        return (
                pathlib.Path.home() / 'Library' / 'Application Support' /
                'minecraft'
        )
    elif system == 'Linux':
        return pathlib.Path.home() / '.minecraft'
    return None


minecraft_path = get_minecraft_path()
