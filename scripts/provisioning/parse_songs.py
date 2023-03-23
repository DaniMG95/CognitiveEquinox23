import csv
import datetime
from scripts.datatovector import DataToVector


def parse_data():
    data_to_vector = DataToVector()

    with open(f'../../resources/vectorize_music{int(datetime.datetime.now().timestamp())}.csv', mode='w') as output_csv_file:
        with open('../../resources/tcc_ceds_music.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(output_csv_file, delimiter=';')
            counter = 0

            for row in csv_reader:
                if counter == 0:
                    csv_writer.writerow(['artist_name', 'track_name', 'release_date', 'genre', 'lyrics', 'song_len',
                                         'topic', 'age', 'lyrics_vector'])
                else:
                    artist_name = row[1]
                    track_name = row[2]
                    release_date = row[3]
                    genre = row[4]
                    lyrics = row[5]
                    song_len = row[6]
                    topic = row[-2]
                    age = row[-1]
                    lyrics_vector = data_to_vector.prepare_input(input_string=lyrics)

                    csv_writer.writerow([artist_name, track_name, release_date, genre, lyrics, song_len, topic, age,
                                         lyrics_vector.tolist()])

                counter = counter + 1
    print(f'lyrics added {counter}')


if __name__ == '__main__':
    parse_data()
