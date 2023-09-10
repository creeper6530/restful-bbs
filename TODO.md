# TODOs

- [x] Move TODOs to a special file in order to not make mess in the commits
- [x] Solve, when a token is needed, but not provided (use error code 499 or 401)
- [x] Remove the "=" at the end of tokens
- [x] Try programming from RPi via SSH in order to fully utilize Linux' pros
- [x] Examples for login/logout
- [x] ~~Send only list of Boards when `GET /boards`~~ Send number of posts on a board when `GET /boards` instead of list of them
- [x] Add `register()`, `underister()`, `chpasswd()` and integrate into endpoint
- [x] Split `/auth` endpoint into respective `/auth/<action>`
- [x] Write documentation
- [x] Solve, when other variables besides token are missing
- [x] Log actions with username (you can find out from the token) and IP
- [x] Hash users' passwords in DB
- [x] Optimize bcrypt's import
- [x] Translate the whole project to English
- [x] Remove sample DBs in code
- [x] Add `logout_all()` for invalidating all tokens of a certain user
- [x] Dockerize (put in Docker)
- [x] Optimize Dockerization, because now it is a hot mess
- [x] Move the BBS savefile from file to Redis
- [x] Solve loading the whole BBS into RAM - work directly with Redis w/o loading it to RAM
- [x] Theoretically, it's possible to encounter problems when deleting board that's not the last board in the DB. <br>
Example: It is possible to arrange the DB into this state: `bbs:0 bbs:1 bbs:3 bbs:4` by deleting `bbs:2`. <br>
This could cause duplicate boards / users (because the BBS wouldn't acknowledge the presence of `bbs:3` and `bbs:4` because it would get `None` for `bbs:2`). <br>
Solve it by shifting all keys with index > current working index (shifting `bbs:3` back to `bbs:2` and `bbs:4` to `bbs:3`).
- [ ] Fetch only necessary fields (see https://developer.redis.com/howtos/redisjson/using-python#fetching-specific-fields-from-a-json-document to learn how)
- [ ] Learn how to return multiple keys by Redis (remove the `while` loops)
- [ ] Test more Gunicorn workers
- [ ] Implement permissions (right now you can `GET` everything w/o login and `POST` or `DELETE` w/ login)
- [ ] Write unit tests (check that nothing's broken)
- [ ] Prettify/Format the code
- [ ] Client