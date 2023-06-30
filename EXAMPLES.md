# Examples of usage

## Boards
- `curl -i http://127.0.0.1:5000/boards -X GET`
- `curl -i http://127.0.0.1:5000/boards -X POST -H 'Content-Type: application/json' -d '{"name":"ShrekIsLove", "token":"S4mpl3T0k3n"}'`
- `curl -i http://127.0.0.1:5000/boards -X DELETE -H 'Content-Type: application/json' -d '{"name":"ShrekIsLove", "token":"S4mpl3T0k3n"}'`

## Posts
- `curl -i http://127.0.0.1:5000/boards/Technika -X GET`
- `curl -i http://127.0.0.1:5000/boards/Technika -X POST -H 'Content-Type: application/json' -d '{"title": "Test", "contents": "Random article", "token":"S4mpl3T0k3n"}'`
- `curl -i http://127.0.0.1:5000/boards/Technika -X DELETE -H 'Content-Type: application/json' -d '{"id": 3, "token":"S4mpl3T0k3n"}'`

## Loading and saving DBs
- `curl -i http://127.0.0.1:5000/reload -X POST -H 'Content-Type: application/json' -d '{"token":"S4mpl3T0k3n"}'`
- `curl -i http://127.0.0.1:5000/save -X POST -H 'Content-Type: application/json' -d '{"token":"S4mpl3T0k3n"}'`

## Auth
- `curl -i http://127.0.0.1:5000/auth -X POST -H 'Content-Type: application/json' -d '{"action":"login", "username":"guest1", "password":"qwerty"}'`
- `curl -i http://127.0.0.1:5000/auth -X POST -H 'Content-Type: application/json' -d '{"action":"logout", "token":"<add_token_here>"}'` Insertion of a token is required.