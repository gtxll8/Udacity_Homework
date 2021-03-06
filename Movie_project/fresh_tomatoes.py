import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>

   <script>$(function ()
   // Share button pop-over
      { $("[data-toggle='popover']").popover();
      });
    </script>
    <script>
    // Hover over image tooltip - play trailer
   $(function () { $("[data-toggle='tooltip']").tooltip(); });
</script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>

    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
 <div class="navbar-wrapper">
       <div class="navbar-header">
        <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">George's recommended movies</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li class="active"><a href="#">Home</a></li>
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Contact<span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                  <li><a href="mailto:george@chessborg.com">Send me an email</a></li>
                  </ul>
                </li>
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Review websites<span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a href="http://www.rottentomatoes.com/">Rottentomatoes</a></li>
                    <li><a href="http://www.metacritic.com/movie">Metacritic</a></li>
                    <li><a href="http://www.jinni.com/">Jinni</a></li>
                    <li class="divider"></li>
                    <li class="dropdown-header">Official movie database</li>
                    <li><a href="www.imdb.com">Imdb</a></li>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>
  <div class="container">
      {movie_tiles}
  </div>


      <!-- FOOTER -->
      <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>
        <p>&copy; 2014 Chessborg, Inc. &middot; <a href="#">Privacy</a> &middot; <a href="#">Terms</a></p>
      </footer>

    </div><!-- /.container -->
     </body>

</html>
'''

# A single movie entry html template
movie_tile_content = '''

        <div class="col-md-7">
          <h2 class="featurette-heading">{movie_title}</h2>
          <h4 class="lead">{storyline}</h4>
          <p>
        <a href="#"
        id="target"
        class="btn btn-primary popover-link"
        data-placement="right"
        data-toggle="popover"
        data-html="true"
        data-content="
            <a href='https://en-gb.facebook.com'>Facebook</a><br/>
            <a href='https://twitter.com'>Twitter</a><br/>
        "
        data-title="Share this movie title"
        >Share</a>
        </p>
        </div>
        <div class="movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
          <img class="tooltip-test" src="{poster_image_url}" width="220" height="342" data-toggle="tooltip" title="Click to see the trailer">
        </div>

'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            storyline=movie.storyline
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible