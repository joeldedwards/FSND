# FSND Capstone Project

## Capstone Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7.7

Follow instructions to install the version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It's good practise to work within a virtual environment whenever using Python. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we use to handle cross origin requests from the frontend server. 

## Database Setup

Create the "movies" database in PostgreSQL
```
createdb movies
```

## Testing

Heroku Testing Endpoint

```
https://fsnd-capstone-casting1.herokuapp.com/
```

# API Endpoints

### GET '/movies'
Fetch a dictionary of movies in which the keys are the ids and the value is the corresponding string of the movie curl `http://127.0.0.1:5000/movies`

- Request Arguments: None
- Returns: 

```
{
  "movies": [
    {
      "id": 1,
      "title": "Blade",
      "release_year": 1998
    },
    {
      "id": 2,
      "title": "The Last Samurai",
      "release_year": 2003
    },
    {
      "id": 3,
      "title": "Interview With The Vampire",
      "release_year": 2003
    }
  ], 
  "success": True, 
  "total_movies": 3
}
```
### POST '/movies/add'
Adds a new movie to the movies list `curl http://127.0.0.1:5000/movies/add -X POST -H "Content-Type: application/json" -d '{"title": "Pulp Fiction", "release_year":"1994"}'`

- Request Arguments: {title:string, release_year:int}
- Returns: 

```
{
    "success": True,
    "created": 4
}
```
### PATCH '/movies/<movie_id>'
Updates an existing movie from the movies list `curl http://127.0.0.1:5000/movies/4 -X PATCH -H "Content-Type: application/json" -d '{"title": "Pulp Fiction", "release_year":"1995"}'`

- Request Arguments: movie_id:int
- Returns: 

```
{
    "success": True,
    "updated": 4
}
```
### DELETE '/movies/<movie_id>'
Deletes a movie from the movies list `curl -X DELETE http://127.0.0.1:5000/movies/2`

- Request Arguments: movie_id:int
- Returns: 

```
{
    "success": True,
    "deleted": 2
}
```

### GET '/actors'
Fetch a dictionary of actors curl `http://127.0.0.1:5000/actors`

- Request Arguments: None
- Returns: 

```
{
  "actors": [
    {
      "id": 1,
      "name": "Dwayne Johnson",
      "age": 48,
      "gender": "male"
    },
    {
      "id": 2,
      "name": "Jet Li",
      "age": 57,
      "gender": "male"
    },
    {
      "id": 3,
      "name": "Michelle Yeoh",
      "age": 58,
      "gender": "female"
    }
  ], 
  "success": True, 
  "total_actors": 3
}
```
### POST '/actors/add'
Adds a new movie to the movies list `curl http://127.0.0.1:5000/actors/add -X POST -H "Content-Type: application/json" -d '{"name":"Kerry Washington", "age":"43", "gender":"female"}'`

- Request Arguments: {name:string, age:int, gender:string}
- Returns: 

```
{
    "success": True,
    "created": 4
}
```
### PATCH '/actors/<actor_id>'
Updates an existing movie from the movies list `curl http://127.0.0.1:5000/actors/4 -X PATCH -H "Content-Type: application/json" -d '{"name":"Kerry Washington", "age":"44", "gender":"female"}'`

- Request Arguments: actor_id:int
- Returns: 

```
{
    "success": True,
    "updated": 4
}
```
### DELETE '/actors/<actor_id>'
Deletes a movie from the movies list `curl -X DELETE http://127.0.0.1:5000/actors/2`

- Request Arguments: actor_id:int
- Returns: 

```
{
    "success": True,
    "deleted": 2
}
```

## Permissions

Permissions|Details
---|---
get:movies|Access all movies
post:movies|Add movies
patch:movies|Update movies
delete:movies|Delete movies
get:actors|Access all actors
post:actors|Add actors
patch:actors|Update actors
delete:actors|Delete actors

## Roles

Role|Permissions
---|---
Casting Assistant| get:movies get:actors
Casting Director| get:movies get:actors post:actors delete:actors  patch:actors patch:movies
Executive producer| get:movies get:actors post:actors post:movies delete:actors delete:movies patch:actors patch:movies

### AUTHORS

Joel Edwards

## Acknowledgements

Udacity FSND Instructors