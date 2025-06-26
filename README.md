This is a Watchlist for user to create their own movie watch list.

In this web app, user can:
1. Create their user account via "Register" function.
2. User can login to the Watchlist via "Login" function.
3. Once user login, user can create their own movie watchlist, by input the movie name and year. Once the record created, it will auto generate a IMDb link to link up with the Movie by the movie name.
4. User also can manage their watchlist via the "Delete" and "Edit" functions.
5. User can also change their display name via the "Setting" functions.
6. Final, user can logout the system by "Logout" function. And it will re-direct to the landing page.
7. Landing page have the instruction for user to Register or Login, and also there are some example for the movie watchlist.

About the program:
I am writing the code by app.py originally, but after restructure into a package, to facilitate organize the project for better maintainability.
I divided the app.py into:
__init__.py
views.py
errors.py
models.py
commands.py

and move the 400.html, 404.html and 500.html into an errors folder.

The finallized project structure (tree):
'''
├── .flaskenv
├── requirements.txt
├── wsgi.py
├── test_watchlist.py
└── watchlist  # package
    ├── __init__.py
    ├── commands.py
    ├── errors.py
    ├── models.py
    ├── views.py
    ├── static
    │   ├── favicon.ico
    │   ├── images
    │   │   ├── movies-life-is-better-sticker.jpg
    │   │   └── rick-and-morty.gif
    │   └── style.css
    └── templates
        ├── base.html
        ├── edit.html
        ├── errors
        │   ├── 400.html
        │   ├── 404.html
        │   └── 500.html
        ├── index.html
        ├── login.html
        └── settings.html
'''


The original project structure (tree):
'''
├── .flaskenv
├── app.py
├── test_watchlist.py
├── static
│   ├── favicon.ico
│   ├── images
│   │   ├── movies-life-is-better-sticker.jpg
│   │   └── rick-and-morty.gif
│   └── style.css
└── templates
    ├── 400.html
    ├── 404.html
    ├── 500.html
    ├── base.html
    ├── edit.html
    ├── index.html
    ├── login.html
    └── settings.html
'''
