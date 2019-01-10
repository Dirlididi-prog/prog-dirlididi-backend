# Dirlididi API

## Endpoints

| Method | Endpoint     | Entry                    | Result                 |
| ------ | ------------ | -----                    | ---------------------- |
| POST   | /problem | JWT Authorization header, name, description, , tip(optional), tests (JSON list with name, input, output and tip(optional)) | Creates and returns a Problem |  
| GET    | /problem | | Returns all Problems |
| GET | /problem/<key:String> |  | Returns a Problem by key |
| POST | /auth | email, password | Authenticates a user and returns JWT token |
| POST | /user | email, password | Creates and returns a User |
| GET | /user | JWT Authorization header | Returns user information |