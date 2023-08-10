# Board management
List, add or delete boards
<br></br>

## Get a list of boards
### Endpoint
`GET /boards`
### Responses
<table>
<tr><td><b> Status </td><td><b> Response </td></tr>
<tr><td> 200 OK </td>
<td>

Returns a list of boards with name and number of posts on board.
<br>Example response:
```json
[
  {
    "name": "Lobby",
    "posts": 0
  },
  {
    "name": "Tech",
    "posts": 3
  }
]
```

</td></table>

### Example
`curl -i http://127.0.0.1:5000/boards -X GET`

## Add a board
### Endpoint
`POST /boards`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "name": "string",
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Response |
|---|---|
| 204 NO CONTENT | Successfully added board. No additional action needed. |
| 400 BAD REQUEST | Board name contains invalid characters. |
| 409 CONFLICT | Board with designed name already exists. |
### Example
`curl -i http://127.0.0.1:5000/boards -X POST -H 'Content-Type: application/json' -d '{"name":"ShrekIsLove", "token":"S4mpl3T0k3n"}'`

## Delete a board
### Endpoint
`DELETE /boards`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "name": "string",
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Response |
|----|----|
| 204 NO CONTENT | Successfully deleted board. No additional action needed. |
| 404 NOT FOUND | Board with designed name does not exists. |
### Example
`curl -i http://127.0.0.1:5000/boards -X DELETE -H 'Content-Type: application/json' -d '{"name":"ShrekIsLove", "token":"S4mpl3T0k3n"}'`


<hr>

# Post management
Get posts from board, add or delete posts on board.
<br><br>

## Get posts from board
### Endpoint
`GET /boards/<board>`
### Parameters
| Parameter | Description |
| --- | --- |
| board | Name of board to operate with |
### Responses
<table>
<tr><td><b> Status </td><td><b> Response </td></tr>
<tr><td> 200 OK </td><td>

Returns a list of posts on a board with title, contents, author and ID of post.
<br>Example response:
```json
[
  {
    "title": "Test number 1",
    "contents": "Rokjsbj",
    "author": "Administrator",
    "id": 0
  },
  {
    "title": "Test number 5874",
    "contents": "vkhdbjs bk",
    "author": "Administrator",
    "id": 1
  },
  {
    "title": "LOLZ",
    "contents": "No contents",
    "author": "Administrator",
    "id": 2
  }
]
```

</td></tr>
<tr><td> 404 NOT FOUND </td>
<td> Board with designed name does not exist. </td></tr>
</table>

### Example
`curl -i http://127.0.0.1:5000/boards/Tech -X GET`

## Add a post on the board
### Endpoint
`POST /boards/<board>`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> board </td><td> Name of board to operate with </td></tr>
<tr><td> body </td>
<td>

```json
{
  "title": "string",
  "contents": "string",
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Response |
|---|---|
| 204 NO CONTENT | Successfully added post. No additional action needed. |
| 404 NOT FOUND | Board with designed name does not exist. |
### Example
`curl -i http://127.0.0.1:5000/boards/Tech -X POST -H 'Content-Type: application/json' -d '{"title": "Test", "contents": "Random article", "token":"S4mpl3T0k3n"}'`

## Delete a post from the board
### Endpoint
`DELETE /boards/<board>`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> board </td><td> Name of board to operate with </td></tr>
<tr><td> body </td>
<td>

```json
{
  "id": 0,
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Response |
|---|---|
| 204 NO CONTENT | Successfully deleted post. No additional action needed. |
| 404 NOT FOUND | Board with designed name or post with designed ID does not exist. |
### Example
`curl -i http://127.0.0.1:5000/boards/Tech -X DELETE -H 'Content-Type: application/json' -d '{"id": 3, "token":"S4mpl3T0k3n"}'`


<hr>

# DB control

## Reload DBs from files
### Endpoint
`POST /reload`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Response |
| --- | --- |
| 204 NO CONTENT | DBs were successfully reloaded. |
### Example
`curl -i http://127.0.0.1:5000/reload -X POST -H 'Content-Type: application/json' -d '{"token":"S4mpl3T0k3n"}'`

## Save DBs to files
### Endpoint
`POST /save`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Response |
| --- | --- |
| 204 NO CONTENT | DBs were successfully saved. |
### Example
`curl -i http://127.0.0.1:5000/save -X POST -H 'Content-Type: application/json' -d '{"token":"S4mpl3T0k3n"}'`


<hr>

# Authorization

## Login
### Endpoint
`POST /auth/login`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "username": "string",
  "password": "string"
}
```

</td>
</table>

### Responses 
<table>
<tr><td><b> Status </td><td><b> Response </td></tr>
<tr><td> 200 OK </td>
<td>

Returns a token for the user to use.
<br>Example response:
```json
{
  "token": "aXQD7WHV3wI"
}
```

</td></tr>
<tr><td> 401 UNAUTHORIZED </td>
<td> Designed user credentials either do not exist or are disabled. </td></tr>
</table>

### Example
`curl -i http://127.0.0.1:5000/auth/login -X POST -H 'Content-Type: application/json' -d '{"username":"guest1", "password":"qwerty"}'`

## Logout
### Endpoint
`POST /auth/logout`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "token": "string"
}
```

</td>
</table>

### Responses
| Status | Description |
| --- | --- |
| 204 NO CONTENT | Successfully logged user out. No additional action needed. |
| 498 INVALID TOKEN (unofficial) | Token provided does not exist. There is nothing to log out. |
### Example
`curl -i http://127.0.0.1:5000/auth/logout -X POST -H 'Content-Type: application/json' -d '{"token":"<add_token_here>"}'` Insertion of a token is required.

## Logout all
### Endpoint
`POST /auth/logout_all`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "token": "string"
}
```

</td>
</table>

### Responses
<table>
<tr><td><b> Status </td><td><b> Response </td></tr>
<tr><td> 200 OK </td>
<td>

Returns a number of tokens logged out.
<br>Example response:
```json
{
  "number": 3
}
```

</td></tr></table>

### Example
`curl -i http://127.0.0.1:5000/auth/logout_all -X POST -H 'Content-Type: application/json' -d '{"token":"<add_token_here>"}'` Insertion of a token is required.

## Register
### Endpoint
`POST /auth/register`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "username": "string",
  "password": "string"
}
```

</td>
</table>

### Responses
| Status | Description |
| --- | --- |
| 204 NO CONTENT | Successfully registered user. You can now log in. |
| 409 CONFLICT | User with designed username already exists. |
### Example
`curl -i http://127.0.0.1:5000/auth/register -X POST -H 'Content-Type: application/json' -d '{"username":"test", "password":"somepasswd"}'`

## Change password
### Endpoint
`POST /auth/chpasswd`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "username": "string",
  "old_password": "string",
  "new_password": "string"
}
```

</td>
</table>

### Responses
| Status | Description |
| --- | --- |
| 204 NO CONTENT | Successfully changed password. No additional action needed. |
| 401 UNAUTHORIZED | Designed user credentials do not exist. |
### Example
`curl -i http://127.0.0.1:5000/auth/chpasswd -X POST -H 'Content-Type: application/json' -d '{"username":"test", "old_password":"somepasswd", "new_password":"anotherpasswd"}'`

## Unregister
### Endpoint
`POST /auth/unregister`
### Parameters
<table>
<tr><td><b> Parameter </td><td><b> Description </td></tr>
<tr><td> body </td>
<td>

```json
{
  "username": "string",
  "password": "string"
}
```

</td>
</table>

### Responses
| Status | Description |
| --- | --- |
| 204 NO CONTENT | Successfully changed password. No additional action needed. |
| 401 UNAUTHORIZED | Designed user credentials do not exist. |
### Example
`curl -i http://127.0.0.1:5000/auth/unregister -X POST -H 'Content-Type: application/json' -d '{"username":"test", "password":"anotherpasswd"}'`

<hr>


# General errors
The following error descriptions supplement the errors in specific cases.

## All-time general
| Status | Description |
| --- | --- |
| 400 BAD REQUEST | The request was malformed. This is most commonly caused by missing parameters. |
| 404 NOT FOUND | Requested endpoint does not exist. |
| 405 METHOD NOT ALLOWED | HTTP method requested is not permitted at designed endpoint. |
| 500 INTERNAL SERVER ERROR | Error occured in the server code. Please notify the administrator in case this happens. |

## Does not apply to GET method and auth
| Status | Description |
| --- | --- |
| 401 UNAUTHORIZED | Authorization token was not provided. |
| 415 UNSUPPORTED MEDIA TYPE | Request must be JSON, and was not. |
| 440 LOGIN TIMEOUT (unofficial) | Token provided is expired. You need to re-login. |
| 498 INVALID TOKEN (unofficial) | Token provided is invalid. You need to re-login. |