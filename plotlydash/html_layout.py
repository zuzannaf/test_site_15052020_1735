html_layout = '''<!DOCTYPE html>
                <html lang="en">
<head>
        <link rel="shortcut icon" href="assets/logo.png">
        {%metas%}
	<title>zuzaflow</title>
        {%css%}
    
</head>
<body>

<header>
        <nav class="navbar navbar-default navbar-expand-lg navbar-fixed-top" role="navigation">
    <div class="container">
		<div class="navbar-header">
		<a href="/">
	<img src="assets/logo.png" height="43" width="43">
		</a>

		</div>

		<ul class="nav justify-content-center">
		  <li class="nav-item hoverChange">
			<a class="nav-link active" href="/">Home</a>
		  </li>
		  <li class="nav-item hoverChange">
			<a class="nav-link" href="/contact">Contact</a>
		  </li>
		</ul>	
 
	</div>
	</nav>
</header>

                {%app_entry%}
                {%config%}
                {%scripts%}
                {%renderer%}

  <footer class="page-footer">

         <div class="container-fluid mb-0 hoverChange2">

         <!-- Add icon library -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <!-- Add font awesome icons -->
        <a href="https://instagram.com" class="fa fa-instagram"></a>

        <a href="https://twitter.com" class="fa fa-twitter"></a>
            

          </div>
          
   </footer>

                <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</body>
</html>
'''
