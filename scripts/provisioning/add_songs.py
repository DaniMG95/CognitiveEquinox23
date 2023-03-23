import csv
import glob
import json
import os

from musicvec.model import Song, SongRepository


def add_data():
    song_repository = SongRepository()
    song_repository.create_collection()

    vectorize_files = glob.glob('../../resources/vectorize_music*.csv')
    last_vectorize_file = max(vectorize_files, key=os.path.getctime)

    with open(last_vectorize_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        counter = 0
        songs = []
        for row in csv_reader:
            if counter != 0:
                artist_name = row[0]
                track_name = row[1]
                release_date = row[2]
                genre = row[3]
                lyrics = row[4]
                song_len = row[5]
                topic = row[6]
                age = row[7]
                lyrics_vector = row[8]

                song = Song(
                    id=counter,
                    artist_name=artist_name,
                    track_name=track_name,
                    lyrics=lyrics,
                    release_year=int(release_date),
                    genre=genre,
                    topic=topic,
                    age=float(age),
                    _vector=json.loads(lyrics_vector)[0]
                )
                songs.append(song)
                if len(songs) == 100:
                    song_repository.add_songs(songs)
                    songs = []
            counter = counter + 1

    print(f'songs added {counter}')


if __name__ == '__main__':
    add_data()
