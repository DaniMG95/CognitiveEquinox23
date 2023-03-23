import csv

with open('../../resources/tcc_ceds_music.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_row = True
    for row in csv_reader:
        if not first_row:
            artist_name = row[1]
            track_name = row[2]
            release_date = row[3]
            genre = row[4]
            lyrics = row[5]
            song_len = row[6]
            # get vector
            # save to database
            print(lyrics)
        first_row = False
