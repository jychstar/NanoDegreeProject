import fresh_tomatoes
import media
zootopia=media.Movie("Zootopia","Animals fight for equal rights","https://upload.wikimedia.org/wikipedia/en/e/ea/Zootopia.jpg","https://www.youtube.com/watch?v=WWFB-zrxn7o")

terminator_2=media.Movie("Terminator 2: Judgment Day", "Future robots time travel to change the world", "https://upload.wikimedia.org/wikipedia/en/8/85/Terminator2poster.jpg", "https://www.youtube.com/watch?v=PZY-5SmjvXg")

#print zootopia.storyline
#terminator_2.show_trailer()

movies=[zootopia, terminator_2]
fresh_tomatoes.open_movies_page(movies)
