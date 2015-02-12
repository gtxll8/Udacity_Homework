__author__ = 'gcalinescu'

import media
import fresh_tomatoes


#toy_story = media.Movie("Toy Story","A story of a boy and his toys that come alive",
                        #"http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                       # "https://www.youtube.com/watch?v=KYz2wyBy3kc")

#avatar = media.Movie("Avatar","A marine on a an alien planet",
                    # "http://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
                    # "https://www.youtube.com/watch?v=cRdxXPV9GNQ")


chapie = media.Movie("Chapie","When one police droid, Chappie, is stolen and given new programming, he becomes the first robot with the ability to think and feel for himself",
                     "http://upload.wikimedia.org/wikipedia/en/7/71/Chappie_poster.jpg",
                    "https://www.youtube.com/watch?v=l6bmTNadhJE")




bighero = media.Movie("Big Hero 6","From Walt Disney Animation Studios comes Big Hero 6, an action comedy adventure about brilliant robotics prodigy Hiro Hamada",
                        "http://upload.wikimedia.org/wikipedia/en/thumb/4/4b/Big_Hero_6_%28film%29_poster.jpg/220px-Big_Hero_6_%28film%29_poster.jpg",
                       "www.youtube.com/watch?v=z3biFxZIJOQ")



intodarkness = media.Movie("Star trek into Drakness","A series of terrorist attacks on Earth places Captain James T. Kirk on a mission to deal with the culprit. Nothing is as it seems, as the Starship Enterprise is entangled in covert machinations to ignite war between the Federation and the Klingon Empire, with an ancient enemy in the mix. With alliances tested, relationships strained and differing motives clashing, how costly will the thirst for vengeance prove?",
                           "http://upload.wikimedia.org/wikipedia/en/5/50/StarTrekIntoDarkness_FinalUSPoster.jpg",
                           "https://www.youtube.com/watch?v=QAEkuVgt6Aw")


#print(toy_story.storyline)

#print avatar.storyline

#avatar.show_trailer()

#chapie.show_trailer()
movies = [chapie, bighero, intodarkness]

fresh_tomatoes.open_movies_page(movies)