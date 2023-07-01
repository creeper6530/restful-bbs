# Examples of usage

## Loading and saving DBs
- `curl -i http://127.0.0.1:5000/reload -X POST -H 'Content-Type: application/json' -d '{"token":"S4mpl3T0k3n"}'`
- `curl -i http://127.0.0.1:5000/save -X POST -H 'Content-Type: application/json' -d '{"token":"S4mpl3T0k3n"}'`

## Auth
- `curl -i http://127.0.0.1:5000/auth/login -X POST -H 'Content-Type: application/json' -d '{"username":"guest1", "password":"qwerty"}'`
- `curl -i http://127.0.0.1:5000/auth/logout -X POST -H 'Content-Type: application/json' -d '{"token":"<add_token_here>"}'` Insertion of a token is required.
<br><br>

- `curl -i http://127.0.0.1:5000/auth/register -X POST -H 'Content-Type: application/json' -d '{"username":"test", "password":"somepasswd"}'`
- `curl -i http://127.0.0.1:5000/auth/chpasswd -X POST -H 'Content-Type: application/json' -d '{"username":"test", "old_password":"somepasswd", "new_password":"anotherpasswd"}'`
- `curl -i http://127.0.0.1:5000/auth/unregister -X POST -H 'Content-Type: application/json' -d '{"username":"test", "password":"anotherpasswd"}'`