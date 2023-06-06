from __future__ import unicode_literals
from vision_language_models.dreamlike import DreamLike
from utils import utils, parsing
from datetime import date, datetime
from apiclient.errors import HttpError
import argparse
import sys
import json

def main(args):
    print(args.token)
    playlist_title = f"{args.hours}-h playlist of {args.mood}, {args.genre}"

    print(playlist_title)
    youtube = utils.generate_youtube_credentials(args.token)
    music_list = args.music_array
    title_list = []
    id_list = []
    print(music_list)

    # parse music_list received from args.music_array

    for music in music_list:
        try:
            title, id = utils.youtube_search(youtube, music, 1)
            if (title != 0):
                title_list.append(title)
            if (id != 0):
                id_list.append(id)
            print(f'added with title{title} and id {id}')
        except HttpError as e:
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            raise Exception
    playlist_id = utils.youtube_create_playlist(youtube, playlist_title)
    print(f'playlist_id is : {playlist_id}')
    utils.youtube_insert_music(youtube, playlist_id, id_list)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    ### MANDATORY ###
    parser.add_argument('--hours', type=int, default=1,
                        help='Dataset to use, in []')
    parser.add_argument('--genre', type=str, default='city pop',
                        help='genre')
    parser.add_argument('--mood', type=str, default='sentimental',
                        help='mood')
    parser.add_argument('--music_array', type=str, nargs="+", help='an array of music titles')
    parser.add_argument('--token', type=str, help='token')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    main(args)
