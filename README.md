# Dirlididi API

## Endpoints

| Method | Endpoint     | Entry                    | Result                 |
| ------ | ------------ | -----                    | ---------------------- |
| POST   | /problem | name, description, tests (JSON list with name, input, output and tip(optional)), tip(optional) | Creates and returns a Problem |  
| GET    | /problem | | Returns all Problems |
| GET | /problem/<key:String> | | Returns a Problem by key |