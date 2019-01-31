# Dirlididi API

## Populate DB
The DB is automatically populated with problems/courses/users when `POPULATE = True in `app.py`.

## Endpoints

| Method | Endpoint     | Entry                    | Query      |  Result                 |
| ------ | ------------ | -----                    |----------- |  ---------------------- |
| POST   | /problem | JWT Authorization header, name, description, tip(optional), tests (JSON list with name, input, output and tip(optional)) | | Creates and returns a Problem. |  
| GET    | /problem | | name (word or phrase contained in a problem's name)| Returns all Problems. |
| GET | /problem/<key:String> |  | | Returns a Problem by key. |
| POST | /auth | tokenId (from Google) | | Create a user if it doesn't exist and returns JWT token. |
| GET | /user | JWT Authorization header | | Returns user information. |
| POST | /solve | (User) token, (Problem) key, code, tests | | Registers and returns a solution for a problem. |
| POST | /course | JWT Authorization header, name, description, problems (String list with problems keys, optional), language (optional) | | Creates and returns a course. |
| GET | /course | | | Returns all courses |
| GET | /user/courses | JWT authorization token | | Returns all user courses. |
| GET | /course/id/<id:Integer> | | | Returns a course by id. |
| GET | /course/token/<token:String> | | | Returns a course by token. |
| POST | /course/id/<id:Integer> or /course/token/<token:String> | JWT Authorization header, action ("join" or "leave") | | Assigns/removes a user to/from a course, returns the course. |
| GET | /info | | | Returns Dirlididi info (courses, users, problems, solutions quantity). |
| GET | /admin/publish-request | | JWT Authorization header, user must be admin | Returns all available Publish Requests. |
| POST | /admin/publish-request | JWT Authorization header, id (Publish Request id), action ("accept" or "decline), user must be admin | | Accepts/declines a Publish Request, making a problem public if accepted. Returns the Problem. |
| PUT | /problem/<key:String> or /course/id/<id:Integer> | JWT Authorization header, Entity data | | Updates a problem or a course (user must be owner of the problem/course) |
| DELETE | /problem/<key:String> or /course/id/<id:Integer> | JWT Authorization header | | Deletes a problem/course (user must be owner of the problem/course) |
