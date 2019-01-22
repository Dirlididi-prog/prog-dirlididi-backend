# Dirlididi API

## Populate db
In order to populate the database, run the app with `python app.py` or `docker-compose up`, navigate to `/dev` folder and run `populate_db.py`. In short:

    docker-compose up -d
    cd dev && python populate_db.py

## Endpoints

| Method | Endpoint     | Entry                    | Result                 |
| ------ | ------------ | -----                    | ---------------------- |
| POST   | /problem | JWT Authorization header, name, description, tip(optional), tests (JSON list with name, input, output and tip(optional)) | Creates and returns a Problem |  
| GET    | /problem | | Returns all Problems |
| GET | /problem/<key:String> |  | Returns a Problem by key |
| POST | /auth | email, password | Authenticates a user and returns JWT token |
| POST | /user | email, password | Creates and returns a User |
| GET | /user | JWT Authorization header | Returns user information |
| POST | /solve | (User) token, (Problem) key, code, tests | Registers and returns a solution for a problem |
| POST | /course | JWT Authorization header, name | Creates and returns a course |
| GET | /course | | Returns all courses |
| GET | /user/courses | JWT authorization token | Returns all user courses |
| GET | /course/id/<id:Integer> | | Returns a course by id |
| GET | /course/token/<token:String> | | Returns a course by token |
| POST | /course/id/<id:Integer> or /course/token/<token:String> | JWT Authorization header, action("join" or "leave") | Assigns/removes a user to/from a course, returns the course |
| GET | /info | | Returns Dirlididi info (courses, users, problems, solutions quantity) |
