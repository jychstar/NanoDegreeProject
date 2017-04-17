import webbrowser
class Movie():
	""" a class to store the structured data of movie"""
	def __init__(self, movie_title,movie_storyline,poster_image_url, trailer_youtube_url):
		""" define constructor, which takes 4 inputs """
		self.title=movie_title
		self.storyline=movie_storyline
		self.poster_image_url=poster_image_url
		self.trailer_youtube_url=trailer_youtube_url

	def show_trailer(self):
		""" open trailer link using webbrowser module """
		webbrowser.open(self.trailer_youtube_url)
