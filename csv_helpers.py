import random
import pandas

def to_bool(arg):
	return int(arg) == 1  # interprets the 0 or 1 in heard as True or False


def read_csv(txtdir):
	return pandas.read_csv(txtdir, sep='\t')


def write_csv(txtdir, df):
	df.to_csv(txtdir, index=False, sep='\t')


def pick_rand(txtdir, df):
	album_num = len(df['Album'])  # get number of albums in the file

	# pick random entry that hasn't been heard
	r = random.randrange(album_num)
	heard = df['Heard'][r]
	while(to_bool(heard)):
		r = random.randrange(album_num)
		heard = df['Heard'][r]

	# set artist & album and set heard
	artist_name = df['Artist'][r]
	album_title = df['Album'][r]
	df.loc[r, 'Heard'] = 1

	write_csv(txtdir, df)
	return artist_name, album_title
