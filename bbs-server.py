from flask import Flask, request
import json
from time import time
from os import urandom, name
from base64 import b64encode
from copy import deepcopy




app = Flask(__name__)

if name == "nt":
    dividor = "\\"
elif name == "posix":
    dividor = "/"
else: raise NotImplementedError

ensure_ascii = True


def load_db():
    global board_list
    global users_list
    global token_pair_list
    print("Loading DBs...")

    try:
        with open(f"bbs_data{dividor}bbs.json", "r") as file:
            board_list = json.load(file)

    except FileNotFoundError:
        board_list = [{"name": "Lobby",
                "posts": []},

                {"name": "Technika",
                "posts": [
                    {"title": "LOLZ",
                    "contents": "No contents",
                    "id": 0}]}]

    try:
        with open(f"bbs_data{dividor}users.json", "r") as file:
            users_list = json.load(file)

    except FileNotFoundError:
        users_list = [{"username": "guest1",
                "password": "qwerty",
                "enabled": True},

                {"username": "guest2",
                "password": "12345678",
                "enabled": False},

                {"username": "guest3",
                "password": "password",
                "enabled": False}]

    try:
        with open(f"bbs_data{dividor}tokens.json", "r") as file:
            token_pair_list = json.load(file)

    except FileNotFoundError:
        token_pair_list = [{"user": "guest1",
                "token": "hcHci68fFJE=",
                "valid_until": 1470987405}, # Před ~7 lety

                {"user": "guest2",
                "token": "Pa5oDCzuIFN=",
                "valid_until": 1470987405},

                {"user": "guest3",
                "token": "CKJbn897hds=",
                "valid_until": 1470987405}]
        
    print("Checking token DB...")
    tmp_pair_list = token_pair_list.copy() # Funkce copy() zabraňuje vzniku reference na objekt token_pair_list
                                           # Tvorba kopie je potřeba, aby for smyčka nic nepřeskočila
    for token_pair in tmp_pair_list:
        if token_pair["valid_until"] < int(time()):
            token_pair_list.remove(token_pair)
    del tmp_pair_list # Smažeme kopii, abychom ušetřili paměť

load_db()

def save_db():
    print("Saving DBs...")
    with open(f"bbs_data{dividor}bbs.json", "w") as file:
        json.dump(board_list, file, indent=4, ensure_ascii=ensure_ascii)
    with open(f"bbs_data{dividor}users.json", "w") as file:
        json.dump(users_list, file, indent=4, ensure_ascii=ensure_ascii)
    with open(f"bbs_data{dividor}tokens.json", "w") as file:
        json.dump(token_pair_list, file, indent=4, ensure_ascii=ensure_ascii)




def login(usr: str, passwd: str):
    for user in users_list:
        if user["username"] == usr and user["password"] == passwd:
            if not user["enabled"]:
                return json.dumps({"error": "User is disabled."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

            token_length = 64 # v bitech
            new_token = b64encode(urandom(int(token_length/8))).decode().replace("=", "") # Pravděpodobnost shody 2**-<token_length>
            new_valid_until = int(time()) + 1*7*24*60*60 # 1 týden do sekund (platnost 1 týden)
            
            new_token_pair = {"user": usr, "token": new_token, "valid_until": new_valid_until}
            token_pair_list.append(new_token_pair)
            return new_token
    return json.dumps({"error": "User credentials are incorrect."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

def logout(token: str):
    for token_pair in token_pair_list:
        if token_pair["token"] == token:
            token_pair_list.remove(token_pair)
            return True
    return json.dumps({"error": "Token not found."}, ensure_ascii=ensure_ascii), 498, [("Content-Type", "application/json; charset=utf-8")]

def register(usr: str, passwd: str):
    for user in users_list:
        if user["username"] == usr:
            return json.dumps({"error": "User with designed username already exists."}, ensure_ascii=ensure_ascii), 409, [("Content-Type", "application/json; charset=utf-8")]
    
    new_user = {"username": usr, "password": passwd, "enabled": True}
    users_list.append(new_user)
    return True

def unregister(usr: str, passwd: str):
    for user in users_list:
        if user["username"] == usr and user["password"] == passwd:
            users_list.remove(user)
            return True
    return json.dumps({"error": "User with designed credentials not found."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

def chpasswd(usr: str, old_passwd:str, new_passwd: str):
    for user in users_list:
        if user["username"] == usr and user["password"] == old_passwd:
            user["password"] = new_passwd
            return True
    return json.dumps({"error": "User with designed credentials not found."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

def check_token(token: str):
    for token_pair in token_pair_list:
        if token_pair["token"] == token:
            if token_pair["valid_until"] < int(time()):
                logout(token_pair["token"])
                return json.dumps({"error": "Token is expired. Please relogin."}, ensure_ascii=ensure_ascii), 440, [("Content-Type", "application/json; charset=utf-8")]
            return True
    return json.dumps({"error": "Token not found. Please relogin."}, ensure_ascii=ensure_ascii), 498, [("Content-Type", "application/json; charset=utf-8")]

def get_user_from_token(token: str):
    for token_pair in token_pair_list:
        if token_pair["token"] == token:
            return token_pair["user"]
    return False # No matching token found




@app.post("/reload")
def reload_db():
    if request.is_json:
        data = request.get_json()

        try: result = check_token(data["token"])
        except KeyError: return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result

        load_db()
        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.post("/save")
def save_db_api():
    if request.is_json:
        data = request.get_json()

        try: result = check_token(data["token"])
        except KeyError: return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result

        save_db()
        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]




@app.get("/auth")
def get_auth():
    return json.dumps({"error": "Method not allowed."}, ensure_ascii=ensure_ascii), 405, [("Content-Type", "application/json; charset=utf-8")]

@app.post("/auth")
def post_auth():
    if request.is_json:
        data = request.get_json()
        action = data["action"]
        
        if action == "login":
            result = login(data["username"], data["password"])
            if type(result) is bytes:
                new_token = result.decode()
                return json.dumps({"token": new_token}), 201, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "logout":
            result = logout(data["token"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "register":
            result = register(data["username"], data["password"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "unregister":
            result = unregister(data["username"], data["password"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "change_password":
            result = chpasswd(data["username"], data["old_password"], data["new_password"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
    
        else: return json.dumps({"error": "Unsupported action."}, ensure_ascii=ensure_ascii), 422, [("Content-Type", "application/json; charset=utf-8")]
    
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]




@app.get("/")
def root():
    return "This server is currently to be accesed only via the API.", 501 # Todo: odeslat klientský program

@app.get("/boards")
def list_boards():
    postless_board_list = deepcopy(board_list)
    for board in postless_board_list:
        board["posts"] = len(board["posts"])

    return json.dumps(postless_board_list, ensure_ascii=ensure_ascii), 200, [("Content-Type", "application/json; charset=utf-8")]

@app.post("/boards")
def add_board():
    if request.is_json:
        new_board = request.get_json()

        try: result = check_token(new_board["token"])
        except KeyError: return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result
        new_board.pop("token")

        if not new_board["name"].isalnum():
            return json.dumps({"error": "Board name must be alphanumeric (A-Z, a-z, 0-9)."}), 400, [("Content-Type", "application/json; charset=utf-8")]

        for board in board_list:
            if board["name"] == new_board["name"]:
                return json.dumps({"error": "Board with designed name already exists."}, ensure_ascii=ensure_ascii), 409, [("Content-Type", "application/json; charset=utf-8")]

        new_board["posts"] = []
        board_list.append(new_board)
        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
    
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.delete("/boards")
def delete_board():
    if request.is_json:
        board_to_delete = request.get_json()

        try: result = check_token(board_to_delete["token"])
        except KeyError: return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result

        for board in board_list:
            if board["name"] == board_to_delete["name"]:
                board_list.remove(board)
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            
        return json.dumps({"error": "Board does not exist."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.get("/boards/<board_name>")
def posts_on_board(board_name):
    for board in board_list:
        if board["name"] == board_name:
            return json.dumps(board["posts"], ensure_ascii=ensure_ascii), 200, [("Content-Type", "application/json; charset=utf-8")]
        
    return json.dumps({"error": "Board not found."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]

@app.post("/boards/<board_name>")
def add_on_board(board_name):
    if request.is_json:
        new_post = request.get_json()

        new_post["author"] = get_user_from_token(new_post["token"])

        try: result = check_token(new_post["token"])
        except KeyError: return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result
        new_post.pop("token")

        
        for board in board_list:
            if board["name"] == board_name:

                try:
                    if new_post["title"]== "":
                        raise KeyError
                except KeyError:
                    new_post["title"] = "Untitled post"

                try:
                    if new_post["contents"] == "":
                        raise KeyError
                except KeyError:
                    new_post["contents"] = "No contents"

                new_post["id"] = len(board["posts"])
                board["posts"].append(new_post)
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
    
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.delete("/boards/<board_name>")
def delete_post(board_name):
    if request.is_json:
        post_to_delete = request.get_json()

        try: result = check_token(post_to_delete["token"])
        except KeyError: return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result

        for board in board_list:
            if board["name"] == board_name:
                for post in board["posts"]:
                    if post["id"] == post_to_delete["id"]:
                        board["posts"].remove(post)
                        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
                
                return json.dumps({"error": "Post with designed ID does not exist in this board."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]
            
        return json.dumps({"error": "Board does not exist."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]




@app.errorhandler(400)
def err_400(error):
    return json.dumps({"error": "Bad request."}), 400, [("Content-Type", "application/json; charset=utf-8")]

@app.errorhandler(404)
def err_404(error):
    return json.dumps({"error": "Requested endpoint can't be found."}), 404, [("Content-Type", "application/json; charset=utf-8")]

@app.errorhandler(500)
def err_500(error):
    return json.dumps({"error": "Internal server error. Please notify the administrator."}), 500, [("Content-Type", "application/json; charset=utf-8")]




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False) # Pokud debug=True, jakékoli změny do JSON databáze
                         # se zahodí po ukončení nebo reloadu
                         # Jednodušší je spouštět debugování skrze VSCode debugger

save_db()