from smartmatching.dataparser import read_data
from smartmatching import Matching


def main(names):
    play_dict = read_data('../script/player_data.xlsx')
    play_lst = [play_dict[name] for name in names]
    matching_obj = Matching(play_lst)
    matching_obj()


if __name__ == '__main__':
    g_names = ['SJY', 'LSX', 'WMS', 'JYT', 'JL', 'BRIDGE', 'SNOW', 'YY', 'ZEX', 'WZ']
    main(g_names)
