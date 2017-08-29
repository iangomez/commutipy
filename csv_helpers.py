import random
import pandas
import datetime

def to_bool(arg):
	"""
	Change the value 1 or 0 to True/False

	Args:
		arg (int): the truth value

	Returns:
		returns a boolean
	"""
	return int(arg) == 1  # interprets the 0 or 1 in heard as True or False


def read_csv(path):
	"""
	Opens a csv and reads the contents into a dataframe.

	Args:
		txtdir (str): the path to the csv

	Returns:
		returns a pandas dataframe of the csv data
	"""
	return pandas.read_csv(path, sep='\t')


def write_csv(txtdir, df):
	"""
	Opens the csv and writes the contents from a dataframe.

	Args:
		txtdir (str): the path to the csv
		df (dataframe): a pandas dataframe

	Returns:
		returns None
	"""
	df.to_csv(txtdir, index=False, sep='\t')


def pick_rand(txtdir, df):
	"""
	Chooses a random number and uses that as an index to find the next album.
	Once chosen, it sets the heard property to True in the csv. If all albums
	are heard, it will return "No unheard albums"

	Args:
		txtdir (str): the path to the csv
		df (dataframe): a pandas dataframe

	Returns:
		returns artist name and album title
	"""
	if 0 in df['Heard']:

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
		df.loc[r, 'Date'] = str(datetime.date.today())

		write_csv(txtdir, df)
		return artist_name, album_title
	else:
		return "No unheard artists", 'No unheard albums'
