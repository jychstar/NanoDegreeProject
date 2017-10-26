import fresh_tomatoes
import media
zootopia=media.Movie("Zootopia",
								"Animals fight for equal rights",
								"https://upload.wikimedia.org/wikipedia/en/e/ea/Zootopia.jpg",
								"https://www.youtube.com/watch?v=WWFB-zrxn7o")
								# the prefix https:// can't be omitted, otherwise cause errors

terminator_2=media.Movie("Terminator 2: Judgment Day",
									"Future robots time travel to change the world", 
									"https://upload.wikimedia.org/wikipedia/en/8/85/Terminator2poster.jpg",
									 "https://www.youtube.com/watch?v=PZY-5SmjvXg")
amelie = media.Movie("Amelie",
                     "A fanciful comedy about a young woman who discretely \
                         orchestrates the lives of the people around her, \
                         creating a world exclusively of her own making.",
                     "https://upload.wikimedia.org/wikipedia/en/5/53/Amelie_poster.jpg",
                     "https://www.youtube.com/watch?v=6Q537310azE")
movies=[zootopia, terminator_2, amelie]  # create a list of moives
fresh_tomatoes.open_movies_page(movies) # fresh_tomatoes module create a static page to display movie
