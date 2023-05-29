from __future__ import unicode_literals
from vision_language_models.dreamlike import DreamLike
from utils import utils, parsing
from datetime import date, datetime
from apiclient.errors import HttpError
import argparse
import sys

def main(args):
    mood = args.mood # "sentimental", "trendy", "chill"
    genre = args.genre # "jazz", "KPOP", "city pop"
    hours = args.hours

    playlist_title = f"{hours}-h playlist of {mood}, {genre}"

    # date for logging
    day = date.today().day
    current_time = datetime.now().strftime("%H:%M:%S")
    date_time = str(day) + '_' + current_time

    # for generating responses
    model = utils.set_openai()

    message_playlist =  utils.construct_message_playlist(hours=hours, mood=mood, genre=genre)
    response_playlist = utils.generate_response(model=model, message=message_playlist)

    message_image =     utils.construct_message_image(mood=mood, genre=genre)
    response_image =    utils.generate_response(model=model, message=message_image)

    print("Response of Playlist:\n", response_playlist)
    print("Response of Image Prompt:\n", response_image)

    # # for image generation
    # model = DreamLike()
    # model.single_image_generation(response_image, mood=mood, genre=genre, date_time=date_time)

    # save playlist respose in to text file
    utils.save_playlist_response(response_playlist, mood=mood, genre=genre, date_time=date_time)

    # parsing playlist
    music_list = parsing.parse_playlist(response_playlist)
    music_list = utils.music_validity_check(music_list)
    # print(music_list)

    # youtube api-playlist
    # authentication
    print(args.token)
    youtube = utils.generate_youtube_credentials(args.token)
    #
    # youtube api-search
    title_list = []
    id_list = []
    for music in music_list:
        try:
            title, id = utils.youtube_search(youtube, music, 1)
            if (title != 0):
                title_list.append(title)
            if (id != 0):
                id_list.append(id)
        except HttpError as e:
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    for i in range(len(title_list)):
        print(f"title: {title_list[i]}, url: www.youtube.com/watch?v={id_list[i]}")


    #
    playlist_id = utils.youtube_create_playlist(youtube, playlist_title)
    print(f'playlist_id is : {playlist_id}')
    utils.youtube_insert_music(youtube, playlist_id, id_list)
    # utils.youtube_video_upload(youtube, title, file)
    # from utils.utils import download_youtube
    # download_youtube()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    ### MANDATORY ###
    parser.add_argument('--hours', type=int, default=1,
                        help='Dataset to use, in []')
    parser.add_argument('--genre', type=str, default='city pop',
                        help='genre')
    parser.add_argument('--mood', type=str, default='sentimental',
                        help='mood')
    parser.add_argument('--token', type=str, help='token')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    main(args)
