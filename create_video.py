from __future__ import unicode_literals
from vision_language_models.dreamlike import DreamLike
from utils import utils, parsing
from datetime import date, datetime
from apiclient.errors import HttpError
import argparse
import sys
import json

def main(args):
    mood = args.mood  # "sentimental", "trendy", "chill"
    genre = args.genre  # "jazz", "KPOP", "city pop"
    hours = args.hours

    print("running generate music list")
    # date for logging
    day = date.today().day
    current_time = datetime.now().strftime("%H:%M:%S")
    date_time = str(day) + '_' + current_time

    # for generating responses
    model = utils.set_openai()
    message_image = utils.construct_message_image(mood=mood, genre=genre)
    response_image = utils.generate_response(model=model, message=message_image)

    # for image generation
    model = DreamLike()
    model.single_image_generation(response_image, mood=mood, genre=genre)

    # # for generating youtube url list
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
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            raise Exception

    # id_list = ['nuU2YHtxMik']

    # for video generation
    from utils.utils import PlayslistVideoGenerator, youtube_video_upload
    url_list = [f'www.youtube.com/watch?v={id}' for id in id_list]
    cover_imgpath = model.generate_savepath(mood=mood, genre=genre)
    video_generator = PlayslistVideoGenerator(url_list, cover_imgpath)
    video_path = video_generator.return_single_video()
    print(video_path)

    playlist_title = f"{args.hours}-h playlist of {args.mood}, {args.genre}"
    youtube_video_upload(youtube, playlist_title, video_path)

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
    parser.add_argument('--token', type=str, help='token', default='ya29.a0AWY7Ckn9Llxa_c86ghrLL4QOSMrxsHIjxm24A9KvTnA-Hsl3agF_WUZbd_lVn_oFy1-UBXJ55KgJA61AW879w-l_7wyDGYfkZFGIcYQFnaz6RtmGPp8O0x4JD2ehy8gIzkxgRNrpy5P_TKycrClFZAm9qKQrNQaCgYKATASARMSFQG1tDrpLfyUKDnNcXjyERGTZzIH5w0165')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    main(args)
