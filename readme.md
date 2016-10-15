Instructions to run project
---------------------------

1. Extract the zip file to a directory. This folder is the project directory.
2. If you wish to create a virtual environment for python, create and activate it.
3. Install the requirements by typing `pip3 install -r requirements.txt`
    in the project directory.
4. Change directory to `src/` directory.
5. Run server with `python3 manage.py runserver`.
6. Visit http://localhost:8000

Notes
-----
* Visit http://127.0.0.1:8000/movie/2515 to see multiple show times of a movie
in a single theater ((Berkeley) California Theater has 3 shows)
* To check with different data (with same json format) replace `/src/movie_data.json` with new json file and then run `python3 manage.py reloaddata` (*This might take some time*).

To load data
------------
Run the custom django administration command `python3 manage.py reloaddata`

* This command will download check for `movie_data.json` file
* If it exists, will erase all the data in database and loads it into database
* If the file does not exists, it will be downloaded
    from http://188.166.208.228/us_movies/ and load it into database.

**All the old data will be erased and this process can take lot of time based on data and database.**
