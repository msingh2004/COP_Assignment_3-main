import unittest
import io, os, sys
import beackendtest as app2
from app import app
from flask import session
class Testapp(unittest.TestCase):

    def setUp(self) :
        self.client = app.test_client()
        self.client.testing = True

    def test_getpost(self):
        post1 = app2.getPost(1)
        post3 = tuple([post1[0],post1[2],post1[3],post1[4]])
        post2 = (1, 'First', 'Neil','Author1')
        self.assertEqual(post3,post2)

    def test_getcomment(self):
        post1 = app2.getComments(1)
        # print(post1)
        post2 = (1, 1, 'I\'ll be fucked up if you can\'t be right here','Author1')
        post3 = tuple([post1[0][0],post1[0][2],post1[0][3],post1[0][4]])
        self.assertEqual(post3,post2)

    def test_getresult(self):
        post1 = app2.getResults("Fi")
        post3 = tuple([post1[0][0],post1[0][2],post1[0][3],post1[0][4]])
        post2 = (1, 'First', 'Neil','Author1')
        self.assertEqual(post3,post2)

    def test_getresult2(self):
        post1 = app2.getResults("1")
        post2 = []
        self.assertEqual(post1,post2)

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    def test_addpost(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code,200)

    def test_trending(self):
        response = self.client.get('/trending')
        self.assertEqual(response.status_code,200)

    def test_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code,200)
    
    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code,302)
    
    def test_following(self):
        response = self.client.get('/following')
        self.assertEqual(response.status_code,200)

    def test_search(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code,200)
    
    def test_authorpage(self):
        response = self.client.get('/Author1')
        self.assertEqual(response.status_code,200)

    def test_loginpage(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code,200)

    def test_addpost2(self):
        with self.client.session_transaction() as session:
            session["username"] = 'Author1'
        data ={'content': 'Some comment'}
        resp = self.client.post('/1', data = data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code,200)

    def test_addcomment2(self):
        with self.client.session_transaction() as session:
            session["username"] = 'Author1'
        data ={'title':'Testposts','content': 'Some content'}
        resp = self.client.post('/create', data = data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code,302)

    def test_login2(self):
        # with self.client.session_transaction() as session:
        #     session["username"] = 'Author1'
        data ={'username':'Testauthor','password': 'Somepass'}
        resp = self.client.post('/login', data = data, content_type='multipart/form-data')
        self.assertEqual(resp.status_code,302)
    
    # def test_signup2(self):
    #     # with self.client.session_transaction() as session:
    #     #     session["username"] = 'Author1'
    #     data ={'username':'Testauthor5','password': 'Somepass2'}
    #     resp = self.client.post('/signup', data = data, content_type='multipart/form-data')
    #     self.assertEqual(resp.status_code,302)
    # def test_addpost2(self):
    #     data ={'title':'Testposts','content': 'Some content'}
    #     with app.test_client() as c:
    #         with c.session_transaction() as sess:
    #             sess['username'] = 'Author1'
    #             sess['_fresh'] = True # https://flask-login.readthedocs.org/en/latest/#fresh-logins
    #     resp = self.client.post('/create', data = data, content_type='multipart/form-data')
    #     # response = self.client('/create', data = data, content_type='multipart/form-data')
    #     self.assertEqual(resp.status_code,200)
    
    def test_postpage(self):
        response = self.client.get('/1')
        self.assertIn(b'First', response.data)
        self.assertEqual(response.status_code,200)

    def test_signup(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code,200)

#     @app.route('/trending')
#     def test_trending(self):
#         post1 = app.trending()
#         post2 = '''
# <!doctype html>
# <html lang="en">
#   <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1">
    
# Trending

#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
#   </head>
#   <body class = bg-dark>
    
#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark" data-bs-theme="dark">
#         <div class="container-fluid">
#             <a class="navbar-brand" href="index.html">
#                 <!-- <img src="logo.png" alt="logo" width="200" height="130" class="d-inline-block align-text-top"> -->
#                 <img src="/static/logo.png" width="200" height="130" class="d-inline-block align-text-top" />
#             </a>
#             <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#             <span class="navbar-toggler-icon"></span>
#             </button>
#             <div class="collapse navbar-collapse" id="navbarSupportedContent">
#             </div>
#         </div>
#         </nav>

#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark sticky-top fs-5"  data-bs-theme="dark">
#     <div class="container-fluid">
#         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#         <span class="navbar-toggler-icon"></span>
#         </button>
#         <div class="collapse navbar-collapse" id="navbarSupportedContent">
#         <ul class="navbar-nav me-auto mb-2 mb-lg-0">
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/">Home</a>
#             </li>
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/search">Search</a>
#             </li>      
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/trending">Trending</a>
#             </li>         
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="#">Following</a>
#             </li>    
#         </ul>
#         </div>
#     </div>
#     </nav>

    

#       <center>
#       <div class = "text-white mt-5">
#         <h2>Trending</h2>
#       </div>
#     </center>

#       <div class="d-grid gap-3">
#         <div class="p-2 bg-dark text-white mx-5 mt-3" data-bs-theme="dark">
#             <div class="card bg-secondary text-white" data-bs-theme = "dark">
      
#                 <div class="card-body">
#                   <h3 class="card-title">Blog Title</h3>
#                   <h6> Author </h6>
#                   <p class="card-text">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum....</p>
#                   <a href="#" class="btn btn-primary">Read full post</a>
#                 </div>
#               </div>
#         </div>
#         <div class="p-2 bg-dark text-white mx-5 mt-3" data-bs-theme="dark">
#             <div class="card bg-secondary text-white" data-bs-theme = "dark">
      
#                 <div class="card-body">
#                   <h3 class="card-title">Blog Title</h3>
#                   <h6> Author </h6>
#                   <p class="card-text">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum....</p>
#                   <a href="#" class="btn btn-primary">Read full post</a>
#                 </div>
#               </div>
#         </div>
#         <div class="p-2 bg-dark text-white mx-5 mt-3" data-bs-theme="dark"><div class="card bg-secondary text-white" data-bs-theme = "dark">
      
#             <div class="card-body">
#               <h3 class="card-title">Blog Title</h3>
#               <h6> Author </h6>
#               <p class="card-text">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum....</p>
#               <a href="#" class="btn btn-primary">Read full post</a>
#             </div>
#           </div></div>
#       </div>



#       <div class="container mt-5">
#         <footer class="py-5 text-white">
#           <div class="row">
#             <div class="col-6 col-md-2 mb-3">
#               <h5><a href="index.html" class = "nav-link p-0"> SONDER</a></h5>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Sonder</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="/" class="nav-link p-0">Home</a></li>
#                 <li class="nav-item mb-2"><a href="/search" class="nav-link p-0">Search</a></li>
#                 <li class="nav-item mb-2"><a href="/trending" class="nav-link p-0">Trending</a></li>
#                 <li class="nav-item mb-2"><a href="#" class="nav-link p-0">Following</a></li>
#               </ul>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Contact</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="mailto:sonder@gmail.com" class="nav-link p-0">Email</a></li>
#                 <li class="nav-item mb-2"><a href="https://twitter.com" class="nav-link p-0">Twitter</a></li>
#                 <li class="nav-item mb-2"><a href="https://linked.com" class="nav-link p-0">LinkedIn</a></li>
#                 <li class="nav-item mb-2"><a href="https://instagram.com" class="nav-link p-0">Instagram</a></li>
#               </ul>
#             </div>
      
#             <div class="col-md-5 offset-md-1 mb-3">
#               <form>
#                 <h5>Subscribe to our newsletter</h5>
#                 <p>Monthly digest of what's new and exciting from us.</p>
#                 <div class="d-flex flex-column flex-sm-row w-100 gap-2">
#                   <label for="newsletter1" class="visually-hidden">Email address</label>
#                   <input id="newsletter1" type="text" class="form-control" placeholder="Email address">
#                   <button class="btn btn-primary" type="button">Subscribe</button>
#                 </div>
#               </form>
#             </div>
#           </div>
#         </footer>
#       </div>

#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
#   </body>
# </html>
# '''
#         self.assertEqual(post1,post2)
    
#     @app.route('/byauthor')
#     def test_author(self):
#         post1 = app.trending()
#         post2 = '''

# <!doctype html>
# <html lang="en">
#   <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1">
    
# <title> By author </title>

#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
#   </head>
#   <body class = bg-dark>
    
#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark" data-bs-theme="dark">
#         <div class="container-fluid">
#             <a class="navbar-brand" href="index.html">
#                 <!-- <img src="logo.png" alt="logo" width="200" height="130" class="d-inline-block align-text-top"> -->
#                 <img src="/static/logo.png" width="200" height="130" class="d-inline-block align-text-top" />
#             </a>
#             <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#             <span class="navbar-toggler-icon"></span>
#             </button>
#             <div class="collapse navbar-collapse" id="navbarSupportedContent">
#             </div>
#         </div>
#         </nav>

#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark sticky-top fs-5"  data-bs-theme="dark">
#     <div class="container-fluid">
#         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#         <span class="navbar-toggler-icon"></span>
#         </button>
#         <div class="collapse navbar-collapse" id="navbarSupportedContent">
#         <ul class="navbar-nav me-auto mb-2 mb-lg-0">
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/">Home</a>
#             </li>
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/search">Search</a>
#             </li>      
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/trending">Trending</a>
#             </li>         
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="#">Following</a>
#             </li>    
#         </ul>
#         </div>
#     </div>
#     </nav>

    

#       <center>
#       <div class = "text-white mt-5">
#         <h2>Blogs by Author</h2>
#       </div>
#     </center>

#       <div class="d-grid gap-3">
#         <div class="p-2 bg-dark text-white mx-5 mt-3" data-bs-theme="dark">
#             <div class="card bg-secondary text-white" data-bs-theme = "dark">
      
#                 <div class="card-body">
#                   <h3 class="card-title">Blog Title</h3>
#                   <h6> Author </h6>
#                   <p class="card-text">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum....</p>
#                   <a href="#" class="btn btn-primary">Read full post</a>
#                 </div>
#               </div>
#         </div>
#         <div class="p-2 bg-dark text-white mx-5 mt-3" data-bs-theme="dark">
#             <div class="card bg-secondary text-white" data-bs-theme = "dark">
      
#                 <div class="card-body">
#                   <h3 class="card-title">Blog Title</h3>
#                   <h6> Author </h6>
#                   <p class="card-text">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum....</p>
#                   <a href="#" class="btn btn-primary">Read full post</a>
#                 </div>
#               </div>
#         </div>
#         <div class="p-2 bg-dark text-white mx-5 mt-3" data-bs-theme="dark"><div class="card bg-secondary text-white" data-bs-theme = "dark">
      
#             <div class="card-body">
#               <h3 class="card-title">Blog Title</h3>
#               <h6> Author </h6>
#               <p class="card-text">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum....</p>
#               <a href="#" class="btn btn-primary">Read full post</a>
#             </div>
#           </div></div>
#       </div>



#       <div class="container mt-5">
#         <footer class="py-5 text-white">
#           <div class="row">
#             <div class="col-6 col-md-2 mb-3">
#               <h5><a href="index.html" class = "nav-link p-0"> SONDER</a></h5>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Sonder</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="/" class="nav-link p-0">Home</a></li>
#                 <li class="nav-item mb-2"><a href="/search" class="nav-link p-0">Search</a></li>
#                 <li class="nav-item mb-2"><a href="/trending" class="nav-link p-0">Trending</a></li>
#                 <li class="nav-item mb-2"><a href="#" class="nav-link p-0">Following</a></li>
#               </ul>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Contact</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="mailto:sonder@gmail.com" class="nav-link p-0">Email</a></li>
#                 <li class="nav-item mb-2"><a href="https://twitter.com" class="nav-link p-0">Twitter</a></li>
#                 <li class="nav-item mb-2"><a href="https://linked.com" class="nav-link p-0">LinkedIn</a></li>
#                 <li class="nav-item mb-2"><a href="https://instagram.com" class="nav-link p-0">Instagram</a></li>
#               </ul>
#             </div>
      
#             <div class="col-md-5 offset-md-1 mb-3">
#               <form>
#                 <h5>Subscribe to our newsletter</h5>
#                 <p>Monthly digest of what's new and exciting from us.</p>
#                 <div class="d-flex flex-column flex-sm-row w-100 gap-2">
#                   <label for="newsletter1" class="visually-hidden">Email address</label>
#                   <input id="newsletter1" type="text" class="form-control" placeholder="Email address">
#                   <button class="btn btn-primary" type="button">Subscribe</button>
#                 </div>
#               </form>
#             </div>
#           </div>
#         </footer>
#       </div>

#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
#   </body>
# </html>'''
#         self.assertEqual(post1,post2)

#     @app.route('/signup')
#     def test_signup(self):
#         post1 = app.trending()
#         post2 = '''
        
# <!doctype html>
# <html lang="en">
#   <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1">
    
# Signup

#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
#   </head>
#   <body class = bg-dark>
    
#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark" data-bs-theme="dark">
#         <div class="container-fluid">
#             <a class="navbar-brand" href="index.html">
#                 <!-- <img src="logo.png" alt="logo" width="200" height="130" class="d-inline-block align-text-top"> -->
#                 <img src="/static/logo.png" width="200" height="130" class="d-inline-block align-text-top" />
#             </a>
#             <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#             <span class="navbar-toggler-icon"></span>
#             </button>
#             <div class="collapse navbar-collapse" id="navbarSupportedContent">
#             </div>
#         </div>
#         </nav>

#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark sticky-top fs-5"  data-bs-theme="dark">
#     <div class="container-fluid">
#         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#         <span class="navbar-toggler-icon"></span>
#         </button>
#         <div class="collapse navbar-collapse" id="navbarSupportedContent">
#         <ul class="navbar-nav me-auto mb-2 mb-lg-0">
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/">Home</a>
#             </li>
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/search">Search</a>
#             </li>      
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/trending">Trending</a>
#             </li>         
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="#">Following</a>
#             </li>    
#         </ul>
#         </div>
#     </div>
#     </nav>

    

#     <center>
#       <h3 class="text-white mt-5">Signup to Sonder</h3>
#     <form class = "text-white mt-3" style="width:30%" data-bs-theme="dark">
#         <div class="form-floating mb-3 ">
#             <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
#             <label for="floatingInput">Name</label>
#         </div>

#       <div class="form-floating mb-3 ">
#         <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
#         <label for="floatingInput">Email address</label>
#       </div>
#       <div class="form-floating mb-3">
#         <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
#         <label for="floatingPassword">Password</label>
#       </div>
#       <!-- <button type="submit" class="btn btn-primary">Submit</button> -->
#       <div class="btn-group mr-2" role="group" aria-label="Second group">
#         <button type="submit" class = "btn btn-primary">Submit</button>
#         <!-- <button type="submit" class="btn btn-primary">Login instead</button> -->
#         <a href="/login" class="btn btn-primary">Login instead</a>
#       </div>
#     </form>
#   </center>



#       <div class="container mt-5">
#         <footer class="py-5 text-white">
#           <div class="row">
#             <div class="col-6 col-md-2 mb-3">
#               <h5><a href="index.html" class = "nav-link p-0"> SONDER</a></h5>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Sonder</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="/" class="nav-link p-0">Home</a></li>
#                 <li class="nav-item mb-2"><a href="/search" class="nav-link p-0">Search</a></li>
#                 <li class="nav-item mb-2"><a href="/trending" class="nav-link p-0">Trending</a></li>
#                 <li class="nav-item mb-2"><a href="#" class="nav-link p-0">Following</a></li>
#               </ul>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Contact</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="mailto:sonder@gmail.com" class="nav-link p-0">Email</a></li>
#                 <li class="nav-item mb-2"><a href="https://twitter.com" class="nav-link p-0">Twitter</a></li>
#                 <li class="nav-item mb-2"><a href="https://linked.com" class="nav-link p-0">LinkedIn</a></li>
#                 <li class="nav-item mb-2"><a href="https://instagram.com" class="nav-link p-0">Instagram</a></li>
#               </ul>
#             </div>
      
#             <div class="col-md-5 offset-md-1 mb-3">
#               <form>
#                 <h5>Subscribe to our newsletter</h5>
#                 <p>Monthly digest of what's new and exciting from us.</p>
#                 <div class="d-flex flex-column flex-sm-row w-100 gap-2">
#                   <label for="newsletter1" class="visually-hidden">Email address</label>
#                   <input id="newsletter1" type="text" class="form-control" placeholder="Email address">
#                   <button class="btn btn-primary" type="button">Subscribe</button>
#                 </div>
#               </form>
#             </div>
#           </div>
#         </footer>
#       </div>

#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
#   </body>
# </html>'''
#         self.assertEqual(post1,post2)

#     @app.route('/login')
#     def test_login(self):
#         post1 = app.trending()
#         post2 = '''
    
# <!doctype html>
# <html lang="en">
#   <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1">
    
# Login

#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
#   </head>
#   <body class = bg-dark>
    
#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark" data-bs-theme="dark">
#         <div class="container-fluid">
#             <a class="navbar-brand" href="index.html">
#                 <!-- <img src="logo.png" alt="logo" width="200" height="130" class="d-inline-block align-text-top"> -->
#                 <img src="/static/logo.png" width="200" height="130" class="d-inline-block align-text-top" />
#             </a>
#             <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#             <span class="navbar-toggler-icon"></span>
#             </button>
#             <div class="collapse navbar-collapse" id="navbarSupportedContent">
#             </div>
#         </div>
#         </nav>

#     <nav class="navbar navbar-expand-lg bg-body-tertiary bg-dark sticky-top fs-5"  data-bs-theme="dark">
#     <div class="container-fluid">
#         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#         <span class="navbar-toggler-icon"></span>
#         </button>
#         <div class="collapse navbar-collapse" id="navbarSupportedContent">
#         <ul class="navbar-nav me-auto mb-2 mb-lg-0">
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/">Home</a>
#             </li>
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/search">Search</a>
#             </li>      
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="/trending">Trending</a>
#             </li>         
#             <li class="nav-item">
#             <a class="nav-link active" aria-current="page" href="#">Following</a>
#             </li>    
#         </ul>
#         </div>
#     </div>
#     </nav>

    

#     <center>
#       <h3 class="text-white mt-5">Login to Sonder</h3>
#     <form class = "text-white mt-3" style="width:30%" data-bs-theme="dark">
#       <div class="form-floating mb-3 ">
#         <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
#         <label for="floatingInput">Email address</label>
#       </div>
#       <div class="form-floating mb-3">
#         <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
#         <label for="floatingPassword">Password</label>
#       </div>
#       <!-- <button type="submit" class="btn btn-primary">Submit</button> -->
#       <div class="btn-group mr-2" role="group" aria-label="Second group">
#         <button type="submit" class = "btn btn-primary">Submit</button>
#         <!-- <button type="submit" class="btn btn-primary">Signup instead</button> -->
#         <a href="/signup" class="btn btn-primary">Signup instead</a>
#       </div>
#     </form>
#   </center>



#       <div class="container mt-5">
#         <footer class="py-5 text-white">
#           <div class="row">
#             <div class="col-6 col-md-2 mb-3">
#               <h5><a href="index.html" class = "nav-link p-0"> SONDER</a></h5>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Sonder</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="/" class="nav-link p-0">Home</a></li>
#                 <li class="nav-item mb-2"><a href="/search" class="nav-link p-0">Search</a></li>
#                 <li class="nav-item mb-2"><a href="/trending" class="nav-link p-0">Trending</a></li>
#                 <li class="nav-item mb-2"><a href="#" class="nav-link p-0">Following</a></li>
#               </ul>
#             </div>
      
#             <div class="col-6 col-md-2 mb-3">
#               <h5>Contact</h5>
#               <ul class="nav flex-column">
#                 <li class="nav-item mb-2"><a href="mailto:sonder@gmail.com" class="nav-link p-0">Email</a></li>
#                 <li class="nav-item mb-2"><a href="https://twitter.com" class="nav-link p-0">Twitter</a></li>
#                 <li class="nav-item mb-2"><a href="https://linked.com" class="nav-link p-0">LinkedIn</a></li>
#                 <li class="nav-item mb-2"><a href="https://instagram.com" class="nav-link p-0">Instagram</a></li>
#               </ul>
#             </div>
      
#             <div class="col-md-5 offset-md-1 mb-3">
#               <form>
#                 <h5>Subscribe to our newsletter</h5>
#                 <p>Monthly digest of what's new and exciting from us.</p>
#                 <div class="d-flex flex-column flex-sm-row w-100 gap-2">
#                   <label for="newsletter1" class="visually-hidden">Email address</label>
#                   <input id="newsletter1" type="text" class="form-control" placeholder="Email address">
#                   <button class="btn btn-primary" type="button">Subscribe</button>
#                 </div>
#               </form>
#             </div>
#           </div>
#         </footer>
#       </div>

#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
#   </body>
# </html>'''
#         self.assertEqual(post1,post2)

if __name__ == '__main__':
    unittest.main()
