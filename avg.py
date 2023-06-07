import ast

def calculate_average(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sum_danceability = 0
    sum_energy = 0
    sum_key = 0
    sum_loudness = 0
    sum_mode = 0
    sum_speechiness = 0
    sum_acousticness = 0
    sum_instrumentalness = 0
    sum_liveness = 0
    sum_valence = 0
    sum_tempo = 0

    for line in lines:
        features = ast.literal_eval(line.strip())
        danceability = features['danceability']
        energy = features['energy']
        key = features['key']
        loudness = features['loudness']
        mode = features['mode']
        speechiness = features['speechiness']
        acousticness = features['acousticness']
        instrumentalness = features['instrumentalness']
        liveness = features['liveness']
        valence = features['valence']
        tempo = features['tempo']

        sum_danceability += danceability
        sum_energy += energy
        sum_key += key
        sum_loudness += loudness
        sum_mode += mode
        sum_speechiness += speechiness
        sum_acousticness += acousticness
        sum_instrumentalness += instrumentalness
        sum_liveness += liveness
        sum_valence += valence
        sum_tempo += tempo

    num_lines = len(lines)
    avg_danceability = sum_danceability / num_lines
    avg_energy = sum_energy / num_lines
    avg_key = sum_key / num_lines
    avg_loudness = sum_loudness / num_lines
    avg_mode = sum_mode / num_lines
    avg_speechiness = sum_speechiness / num_lines
    avg_acousticness = sum_acousticness / num_lines
    avg_instrumentalness = sum_instrumentalness / num_lines
    avg_liveness = sum_liveness / num_lines
    avg_valence = sum_valence / num_lines
    avg_tempo = sum_tempo / num_lines

    return {
        'danceability': avg_danceability,
        'energy': avg_energy,
        'key': avg_key,
        'loudness': avg_loudness,
        'mode': avg_mode,
        'speechiness': avg_speechiness,
        'acousticness': avg_acousticness,
        'instrumentalness': avg_instrumentalness,
        'liveness': avg_liveness,
        'valence': avg_valence,
        'tempo': avg_tempo
    }

# input: text file name, after musicEval.py execution, which is in the "music_features_result" directory ##
print(calculate_average("./music_features_result/audio_features_mood-dancing_genre-hiphop.txt"))
#print(calculate_average("music_features_result/audio_features_mood-humanmade_soft_genre-Lullaby.txt"))