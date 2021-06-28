import abc


# from change_world_owner import copy_player_data_to_level_dat


class BaseUI(abc.ABC):
    # def change_world_owner(self):
    #     # mc_path = self.get_mc_path()
    #     # saves = (mc_path / 'saves').iterdir()
    #     level_dat = self._get_level_dat()
    #     # player_info = get_players_info(save_path)
    #     uuid_dat = self._get_uuid_dat()
    #     copy_player_data_to_level_dat(level_dat, uuid_dat)

    # @abc.abstractmethod
    # def get_mc_path(self) -> pathlib.Path:
    #     pass

    @abc.abstractmethod
    def main_loop(self):
        pass

    # @abc.abstractmethod
    # def _get_level_dat(self) -> str:
    #     pass
    #
    # @abc.abstractmethod
    # def _get_uuid_dat(self) -> str:
    #     pass
