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
    date_time = args.datetime
    print("running generate music list")

    # for generating responses
    model = utils.set_openai()

    # prerequisite for playlist generation
    message_playlist =  utils.construct_message_playlist(hours=hours, mood=mood, genre=genre)
    response_playlist = utils.generate_response(model=model, message=message_playlist)
    utils.save_playlist_response(response_playlist, mood=mood, genre=genre, date_time=date_time)

    # prerequisite for image generation
    message_image = utils.construct_message_image(mood=mood, genre=genre)
    response_image = utils.generate_response(model=model, message=message_image)
    
    # generate image
    model = DreamLike(args.datetime)
    model.single_image_generation(response_image, mood=mood, genre=genre)
    output_path = model.generate_savepath(mood=mood, genre=genre)
    print(f"generated_image_output_path: {output_path}")

    # parsing playlist
    music_list = parsing.parse_playlist(response_playlist)
    print(music_list)
    music_list = utils.music_validity_check(music_list)

    for i in range(len(music_list)):
        print(f"title: {music_list[i]}")

    return {'music_title': music_list}



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
    parser.add_argument('--datetime', type=str, help='datetime', default='sibaljom')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    main(args)
