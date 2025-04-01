# mso-website

This is the new iteration of the website for [Medisinernes seksualopplysning](https://mso.uib.no).

It's built using [Django](https://www.djangoproject.com) and the Content Management System (CMS) [Wagtail](https://wagtail.org/).

## Running it locally

### Installing Python and Poetry

You specifically need Python 3.12. If you don't have this version installed, head over to [python.org/downloads](https://python.org/downloads)

You also need Poetry, a Python package manager. Instructions for installation are [available here](https://python-poetry.org/docs/#installing-with-pipx).

### (Recommendation, optional) install the PyCharm IDE

If you're inexperienced with Django or Python specific tooling, the easiest way of developing the project locally will be using PyCharm. This is due to its integrated features for Django, and automated management of the Poetry environment.

PyCharm is available for free, as long as you sign up for the [GitHub student developer pack](https://education.github.com/pack). It is important that you get this because we *need* PyCharm Professional edition, [available here](https://www.jetbrains.com/pycharm/download).

### Fork this repository on GitHub

Use the 'fork' button on [fribyte-code/mso-website](https://github.com/fribyte-code/mso-website). Fork it to your own development version as we've done on other projects :D

Your fork can be private if you'd like it to. If you want quick help then having it public might be more convenient.

### Create a PyCharm project cloning your fork of this repository

- On the welcome screen, select 'Get from VCS'.
- You'll get prompts asking if you trust the code. Select 'yes'
- You'll get a prompt asking you if you'd like to set up a Poetry environment. Select 'OK'
- Hopefully, you now have the project on your computer!

#### Making PyCharm run your project

- Near the Top-Right of PyCharm, you should see a menu called 'Current File' to the left of a Play button.
- Click this menu, and select 'Edit Configurations'
- In the window that appears, click the 'Add New Run Configuration' link
- Select 'Django'
- Name the configuration whatever you'd like, maybe 'Run MSO'
- Click 'OK' in the bottom of this window.
    - If this doesn't work, ask for help!
- 'Run MSO' should now be an option next to the Play button in the top of PyCharm
- Click the Play button. The application should now be running.
  - In the future, clicking the play button is all you'd have to do.
- Visit [localhost:8000](http://localhost:8000). This is the website running on your computer.
- Here, you should expect an 'OperationalError at /'. We will fix this in later steps.

### (If you don't use PyCharm)

Clone your fork using your preferred solution. In the project directory:

- Run `poetry install` to get dependencies
- Run `poetry env activate` to activate the virtual env
- Run `python manage.py runserver` to start the application
- Visit [localhost:8000](http://localhost:8000). This is the website running on your computer.
- Here, you should expect an 'OperationalError at /'. We will fix this in the next step.

### Running migrations and creating a user 

The project depends on a SQLite database. This is not yet initialized and is the reason why we saw the 'OperationalError' earlier. We need to create this database and a user for accessing the management panel.

- Open up a terminal. This should be the forth option in the bottom left corner of PyCharm. 
- Run: `python manage.py migrate`. This can take a couple of seconds and you should see a lot of text fly by.
- Run: `python manage.py createsuperuser`
  - Type your preferred username, then click enter.
  - Type your email address (nobody needs this; you can enter a fake one...), then click enter.
  - Type a password, click enter. Type the same password again and click enter.
    - It may yell at you if the password is not sufficiently complex. You can type `y` and override this protection. This login only applies to your local version of the website.

### Profit.

The website should now be in working order on your computer. On running the website with the Play button in PyCharm (or command if not using PyCharm), you should no longer see an error message.

### Creating new pages.

New pages can be created by going to [localhost:8000/admin/](http://localhost:8000/admin/) -> Pages -> click on the pencil next to the title -> click on the triple dots on the top of the page -> Add child page.

You can navigate to the page that you created by using the title of your page like this:  
For example if we made a page with the title "testpage", navigate to [localhost:8000/testpage/](http://localhost:8000/testpage/) after you publish using the drop up menu at the bottom of the page.

The child page contains a title and a hero section and body. The formatting of the text can be changed by clicking the green + button that hovers to the left of the textbox. 

Build away!

## Acknowledgements

Currently, this is under development by a group of `n` people at [friByte](https://fribyte.no):

- Johannes Skivdal [@skivdal](https://github.com/skivdal)
- Kai Waløen [@KWaloen](https://github.com/KWaloen)
