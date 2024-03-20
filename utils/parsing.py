def parse_playlist(message):
    lines = message.split('\n')
    num = 0
    music_list = []
    for line in lines:
        if f"{num+1}." in line:
            music_list.append(line[3:])
            num += 1

    return music_list

