import pandas as pd

from smartmatching import Player


def load_data(file_path, data):
    player_data = pd.read_csv(file_path)
    player_data = pd.concat([player_data, data])
    player_data.to_excel(file_path, index=False)


def read_data(file_path):
    player_data = pd.read_excel(file_path)
    player_dict = {}
    for name in player_data.columns:
        player = Player(name)
        player.scores = list(player_data[name].dropna())
        player_dict[name] = player
    return player_dict
