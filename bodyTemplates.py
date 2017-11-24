WEBPAGETEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>$$title$$</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
  </head>
  <body>
    $$body$$
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
  </body>
</html>
"""
#Requires title,TOPS,
TEMPLATES = { 'JUMBOTRON' : """
<nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <a class="navbar-brand" href="#">$$title$$</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      </div>
    </nav>

    <main role="main">

      $$top$$

      <div class="container marketing">

        $$mid$$

      </div><!-- /.container -->

    </main>

    <footer class="container">
      <p>Created by genetic algorithm designed by Shantanu for CS256</p>
    </footer>
""", 'NARROW_JUMBOTRON' : """
<div class="container">
      <header class="header clearfix">
        <h3 class="text-muted">$$title$$</h3>
      </header>

      <main role="main">

        $$top$$

      <div class="container marketing">

        $$mid$$

      </div><!-- /.container -->

      </main>

      <footer class="footer">
        <p>Created by genetic algorithm designed by Shantanu for CS256</p>
      </footer>

    </div>
""", 'CAROUSEL': """
<header>
      <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="#">$$title$$</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        
      </nav>
    </header>

    <main role="main">
    
        $$top$$
        
      <div class="container marketing">

        $$mid$$

      </div><!-- /.container -->


      <!-- FOOTER -->
      <footer class="container">
        <p class="float-right"><a href="#">Back to top</a></p>
        <p>&copy; Created by genetic algorithm designed by Shantanu for CS256</p>
      </footer>

    </main>
"""}

##Require banner1,2,head1,2
TOPS = {'CAROUSEL2' : """
<div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active" style="max-height: 250px;">
      <center><img class="d-block w-100" src="$$banner1$$" ></center>
    </div>
    <div class="carousel-item" style="max-height: 250px;">
      <center><img class="d-block w-100" src="$$banner2$$" height="250px"></center>
    </div>
  </div>
  <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>
""", 'JUMBOTRON' : """
<div class="jumbotron">
  <h1 class="display-3">$$head1$$</h1>
  <p class="lead">$$head2$$</p>
</div>
"""}

#requires image1,2,3, text1,2,3
MIDS = {'THREE_HEADERS':"""
<!-- Three columns of text below the carousel -->
<div class="row">
  <div class="col-lg-4">
    <img class="rounded-circle" src="$$image1$$" width="140" height="140">
    <p>$$text1$$</p>
  </div><!-- /.col-lg-4 -->
  <div class="col-lg-4">
    <img class="rounded-circle" src="$$image2$$" alt="Generic placeholder image" width="140" height="140">
    <p>$$text2$$</p>
  </div><!-- /.col-lg-4 -->
  <div class="col-lg-4">
    <img class="rounded-circle" src="$$image3$$" alt="Generic placeholder image" width="140" height="140">
    <p>$$text3$$</p>
  </div><!-- /.col-lg-4 -->
</div><!-- /.row -->
""", 'FEATURETTES':"""
<!-- START THE FEATURETTES -->

<hr class="featurette-divider">

<div class="row featurette">
  <div class="col-md-7">
    <p class="lead">$$text1$$</p>
  </div>
  <div class="col-md-5">
    <img class="featurette-image img-fluid mx-auto" src="$$image1$$">
  </div>
</div>

<hr class="featurette-divider">

<div class="row featurette">
  <div class="col-md-7 order-md-2">
    <p class="lead">$$text2$$</p>
  </div>
  <div class="col-md-5 order-md-1">
    <img class="featurette-image img-fluid mx-auto" src="$$image2$$">
  </div>
</div>

<hr class="featurette-divider">

<div class="row featurette">
  <div class="col-md-7 order-md-2">
    <p class="lead">$$text3$$</p>
  </div>
  <div class="col-md-5 order-md-1">
    <img class="featurette-image img-fluid mx-auto" data-src="$$image3$$">
  </div>
</div>

<hr class="featurette-divider">
"""
}


