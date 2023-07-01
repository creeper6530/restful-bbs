# Board management
List, add or delete boards
<br></br>

## Get a list of boards
### Endpoint
`GET /boards`
### Responses
<table>
<tr>
<td> Status </td> <td> Response </td>
</tr>


<tr>
<td>

200 OK

</td>
<td>

Returns a list of boards with name and number of posts on board.
<br>Example response:
```
GET /boards
```
```json
[
  {
    "name": "Lobby",
    "posts": 0
  },
  {
    "name": "Technika",
    "posts": 3
  }
]
```

</td>
</table>

### Example
`curl -i http://127.0.0.1:5000/boards -X GET`

## Add a board
### Endpoint
`POST /boards`
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
### Responses
| Status | Response |
|----|----|
| 204 NO CONTENT | Successfully deleted board. No additional action needed. |
| 404 NOT FOUND | Board with designed name does not exists. |


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
<tr>
<td> Status </td> <td> Response </td>
</tr>
<tr>
<td>

200 OK

</td>
<td>

Returns a list of posts on a board with title, contents, author and ID of post.
<br>Example response:
```
GET /boards/Technika
```
```json
[
    {
        "title": "Test cislo 1",
        "contents": "Rokjsbj",
        "author": "Administrator",
        "id": 0
    },
    {
        "title": "Test cislo 5874",
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

</td>
<tr>
<td>

404 NOT FOUND

</td>
<td>

Board with designed name does not exist.

</td>
</tr>
</table>

### Example
`curl -i http://127.0.0.1:5000/boards/Technika -X GET`

## Add a post on the board
### Endpoint
`POST /boards/<board>`
### Parameters
| Parameter | Description |
| --- | --- |
| board | Name of board to operate with |
### Responses
| Status | Response |
|---|---|
| 204 NO CONTENT | Successfully added post. No additional action needed. |
| 404 NOT FOUND | Board with designed name does not exist. |
### Example
`curl -i http://127.0.0.1:5000/boards/Technika -X POST -H 'Content-Type: application/json' -d '{"title": "Test", "contents": "Random article", "token":"S4mpl3T0k3n"}'`

## Delete a post from the board
### Endpoint
`DELETE /boards/<board>`
### Parameters
| Parameter | Description |
| --- | --- |
| board | Name of board to operate with |
### Responses
| Status | Response |
|---|---|
| 204 NO CONTENT | Successfully deleted post. No additional action needed. |
| 404 NOT FOUND | Board with designed name or post with designed ID does not exist. |
### Example
`curl -i http://127.0.0.1:5000/boards/Technika -X DELETE -H 'Content-Type: application/json' -d '{"id": 3, "token":"S4mpl3T0k3n"}'`


# General errors
The following error descriptions supplement the errors in specific cases.
## All-time general
| Status | Description |
| --- | --- |
| 400 BAD REQUEST | The request was malformed. |
| 404 NOT FOUND | Requested endpoint does not exist. |
| 405 METHOD NOT ALLOWED | HTTP method requested is not permitted at designed endpoint. |
| 500 INTERNAL SERVER ERROR | Error occured in the server code. Please notify the administrator in case this happens. |

## Except GET method
These errors do not occur in the GET method.
| Status | Description |
| --- | --- |
| 401 UNAUTHORIZED | Authorization token was not provided. |
| 415 UNSUPPORTED MEDIA TYPE | Request must be JSON, and was not. |
| 440 LOGIN TIMEOUT (unofficial) | Token provided is expired. You need to re-login. |
| 498 INVALID TOKEN (unofficial) | Token provided is invalid. You need to re-login. |