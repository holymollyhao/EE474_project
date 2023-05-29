# playlist_dir = "./playlist_results"
# text_file = open(f"{playlist_dir}/mood-sentimental_genre-jazz_13_20:16:35_result.txt", "r")
# message = text_file.read()
# text_file.close()
# lines = message.split('\n')

# num = 0
# music_list = []
# for line in lines:
#     if f"{num+1}." in line:
#         music_list.append(line[3:])
#         num += 1

# print(f"original response:\n{message}\n")
# print(f"num: {num}\nmusic list:{music_list}")

def parse_playlist(message):
    lines = message.split('\n')
    num = 0
    music_list = []
    for line in lines:
        if f"{num+1}." in line:
            music_list.append(line[3:])
            num += 1

    return music_list

