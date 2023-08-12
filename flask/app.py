#!/bin/python
from flask import Flask, request
import json
from time import time
from os import urandom, name, makedirs, path
from base64 import b64encode
from copy import deepcopy
import logging
from gzip import open as gzopen
from shutil import copyfileobj
from bcrypt import checkpw, gensalt, hashpw
from redis import Redis
from redis.commands.json.path import Path




if name == "nt":
    divider = "\\"
elif name == "posix":
    divider = "/"
else: raise NotImplementedError

try:
    with open(f"logs{divider}lastest.log", "r") as old_log:
        datetime = old_log.read(19)
    datetime = datetime.replace(" ", "_")
    datetime = datetime.replace(".", "_")
    datetime = datetime.replace(":", "_")

        
    with open(f"logs{divider}lastest.log", "rb") as f_in:
        with gzopen(f"logs{divider}{datetime}.log.gz", "wb") as f_out:
            copyfileobj(f_in, f_out)
except FileNotFoundError: pass

if not path.exists("logs"):
    makedirs("logs")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S', filename=f"logs{divider}lastest.log", filemode="w")
logging.info("Starting up...")

app = Flask(__name__)
port = 5000

db = Redis(host="redis-db", port=6379, db=0)

ensure_ascii = True

treat_ufw = True
if name == "nt": treat_ufw = False # UFW does not exist on Windows
if treat_ufw: from os import system




def load_db():
    logging.info("Loading DBs...")
    global board_list
    global users_list
    global token_pair_list

    i = 0
    board_list = []
    while True:
        board = db.json().get(f"bbs:{i}")
        if board == None: break

        j = 0
        posts = []
        while True:
            post = db.json().get(f"bbs:{i}:{j}")
            if post == None: break
            posts.append(post)
            j += 1
        
        board["posts"] = posts
        board_list.append(board)
        i += 1

    i = 0
    users_list = []
    while True:
        user = db.json().get(f"users:{i}")
        if user == None: break
        users_list.append(user)
        i += 1

    i = 0
    token_pair_list = []
    while True:
        token_pair = db.json().get(f"tokens:{i}")
        if token_pair == None: break
        token_pair_list.append(token_pair)
        i += 1
    
    """ try:
        with open(f"bbs_data{divider}bbs.json", "r") as file:
            board_list = json.load(file)

    except FileNotFoundError:
        logging.warning("bbs.json not found. Committing seppuku.")
        print("bbs.json not found. Committing seppuku.")
        exit(1)

    try:
        with open(f"bbs_data{divider}users.json", "r") as file:
            users_list = json.load(file)

    except FileNotFoundError:
        logging.warning("users.json not found. Committing seppuku.")
        print("users.json not found. Committing seppuku.")
        exit(1)

    try:
        with open(f"bbs_data{divider}tokens.json", "r") as file:
            token_pair_list = json.load(file)

    except FileNotFoundError:
        logging.warning("tokens.json not found. Committing seppuku.")
        print("tokens.json not found. Committing seppuku.")
        exit(1) """
        
    logging.info("Checking token DB...")
    tmp_pair_list = token_pair_list.copy() # The copy() function prevents creation of reference to object token_pair_list
                                           # It is needed in order to prevent the for loop from skipping anything
    for token_pair in tmp_pair_list:
        if token_pair["valid_until"] < int(time()):
            logging.debug(f"Found an expired token pair: {json.dumps(token_pair)}")
            token_pair_list.remove(token_pair)
    del tmp_pair_list # We delete the copy in order to save memory

load_db()

def save_db():
    logging.info("Saving DBs...")

    tmp_board_list = deepcopy(board_list)

    for i, board in enumerate(tmp_board_list):
        for j, post in enumerate(board["posts"]):
            db.json().set(f"bbs:{i}:{j}", Path.root_path(), post)
        del board["posts"]
        db.json().set(f"bbs:{i}", Path.root_path(), board)
    
    for i, user in enumerate(users_list):
        db.json().set(f"users:{i}", Path.root_path(), user)

    for i, token in enumerate(token_pair_list):
        db.json().set(f"tokens:{i}", Path.root_path(), token)

    """ with open(f"bbs_data{divider}bbs.json", "w") as file:
        json.dump(board_list, file, indent=4, ensure_ascii=ensure_ascii)
    with open(f"bbs_data{divider}users.json", "w") as file:
        json.dump(users_list, file, indent=4, ensure_ascii=ensure_ascii)
    with open(f"bbs_data{divider}tokens.json", "w") as file:
        json.dump(token_pair_list, file, indent=4, ensure_ascii=ensure_ascii) """

save_db()




def login(usr: str, passwd: str):
    for user in users_list:
        if user["username"] == usr:
            if not user["enabled"]:
                logging.warning(f"{request.remote_addr} tried to log into disabled user ({usr}).")
                return json.dumps({"error": "User is disabled."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

            logging.info("bcrypt: Checking password...")
            if checkpw(passwd.encode(), user["password"].encode()) == False:
                logging.warning(f"{request.remote_addr} tried to log in with invalid password ({usr}; {passwd}).")
                return json.dumps({"error": "User credentials are incorrect."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

            token_length = 64 # v bitech
            new_token = b64encode(urandom(int(token_length/8))).decode().replace("=", "") # Probability of match: 2**-<token_length>
            new_valid_until = int(time()) + 1*7*24*60*60 # Convert one week (the validity length) to seconds
            
            new_token_pair = {"user": usr, "token": new_token, "valid_until": new_valid_until}
            token_pair_list.append(new_token_pair)
            logging.info(f"{request.remote_addr} logged in as {user['username']}.")
            return new_token.encode()
    logging.warning(f"{request.remote_addr} tried to log in with invalid username ({usr}; {passwd}).")
    return json.dumps({"error": "User credentials are incorrect."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

def logout(token: str):
    for token_pair in token_pair_list:
        if token_pair["token"] == token:
            token_pair_list.remove(token_pair)
            logging.info(f"{request.remote_addr} logged out {token_pair['user']}.")
            return True
    return json.dumps({"error": "Token not found."}, ensure_ascii=ensure_ascii), 498, [("Content-Type", "application/json; charset=utf-8")]

def register(usr: str, passwd: str):
    for user in users_list:
        if user["username"] == usr:
            logging.warning(f"{request.remote_addr} tried to register already existing user ({usr}).")
            return json.dumps({"error": "User with designed username already exists."}, ensure_ascii=ensure_ascii), 409, [("Content-Type", "application/json; charset=utf-8")]
    logging.info("bcrypt: Generating salt...")
    salt = gensalt()
    hashed_passwd = hashpw(passwd.encode(), salt).decode()
    
    new_user = {"username": usr, "password": hashed_passwd, "enabled": True}
    users_list.append(new_user)
    logging.info(f"{request.remote_addr} registered as {usr}.")
    return True

def unregister(usr: str, passwd: str):
    for user in users_list:
        if user["username"] == usr:
            
            logging.info("bcrypt: Checking password...")
            if checkpw(passwd.encode(), user["password"].encode()) == False:
                logging.warning(f"{request.remote_addr} tried to unregister with invalid password ({usr}; {passwd}).")
                return json.dumps({"error": "User with designed credentials not found."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

            users_list.remove(user)
            logging.info(f"{request.remote_addr} unregistered {usr}.")
            return True
    logging.warning(f"{request.remote_addr} tried to unregister with invalid username ({usr}; {passwd}).")
    return json.dumps({"error": "User with designed credentials not found."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

def chpasswd(usr: str, old_passwd:str, new_passwd: str):
    for user in users_list:
        if user["username"] == usr:

            logging.info("bcrypt: Checking password...")
            if checkpw(old_passwd.encode(), user["password"].encode()) == False:
                logging.warning(f"{request.remote_addr} tried to unregister with invalid password ({usr}; {old_passwd}; {new_passwd}).")
                return json.dumps({"error": "User with designed credentials not found."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

            logging.info("bcrypt: Generating salt...")
            salt = gensalt()

            user["password"] = hashpw(new_passwd.encode(), salt).decode()
            logging.info(f"{request.remote_addr} changed password for {usr}.")
            return True
    logging.warning(f"{request.remote_addr} tried to change password with invalid username ({usr}; {old_passwd}; {new_passwd}).")
    return json.dumps({"error": "User with designed credentials not found."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]

def check_token(token: str):
    for token_pair in token_pair_list:
        if token_pair["token"] == token:
            if token_pair["valid_until"] < int(time()):
                logout(token_pair["token"])
                logging.warning(f"{request.remote_addr} tried to use expired token.")
                return json.dumps({"error": "Token is expired. Please relogin."}, ensure_ascii=ensure_ascii), 440, [("Content-Type", "application/json; charset=utf-8")]
            return True
    logging.warning(f"{request.remote_addr} tried to use non-existent token.")
    return json.dumps({"error": "Token not found. Please relogin."}, ensure_ascii=ensure_ascii), 498, [("Content-Type", "application/json; charset=utf-8")]

def get_user_from_token(token: str):
    for token_pair in token_pair_list:
        if token_pair["token"] == token:
            return token_pair["user"]
    return False # No matching token found

def logout_all(token: str):
    result = check_token(token)
    if result != True:
        return result

    user = get_user_from_token(token)

    tmp_pair_list = token_pair_list.copy() # The copy() function prevents creation of reference to object token_pair_list
                                           # It is needed in order to prevent the for loop from skipping anything
    x = 0
    for token_pair in tmp_pair_list:
        if token_pair["user"] == user:
            token_pair_list.remove(token_pair)
            x += 1
    del tmp_pair_list # We delete the copy in order to save memory
    
    logging.info(f"As per request of {request.remote_addr}, logged out all {x} tokens of {user}.")
    return int(x)




@app.post("/reload")
def reload_db():
    if request.is_json:
        data = request.get_json()

        try: result = check_token(data["token"])
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide a token.")
            return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
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
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide a token.")
            return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        if result != True:
            return result

        save_db()
        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]




@app.post("/auth")
def old_auth():
    return json.dumps({"error": "Endpoint has been obsoleted. Please use /auth/<action>."}, ensure_ascii=ensure_ascii), 410, [("Content-Type", "application/json; charset=utf-8")]

@app.post("/auth/<action>")
def post_auth(action):
    if request.is_json:
        data = request.get_json()
        
        if action == "login":
            try: data["username"]; data["password"]
            except KeyError:
                logging.warning(f"{request.remote_addr} did not provide enough parameters.")
                return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

            result = login(data["username"], data["password"])
            if type(result) is bytes:
                new_token = result.decode()
                return json.dumps({"token": new_token}), 201, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "logout":
            try: data["token"]
            except KeyError:
                logging.warning(f"{request.remote_addr} did not provide enough parameters.")
                return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

            result = logout(data["token"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "register":
            try: data["username"]; data["password"]
            except KeyError:
                logging.warning(f"{request.remote_addr} did not provide enough parameters.")
                return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

            result = register(data["username"], data["password"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "unregister":
            try: data["username"]; data["password"]
            except KeyError:
                logging.warning(f"{request.remote_addr} did not provide enough parameters.")
                return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

            result = unregister(data["username"], data["password"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "chpasswd":
            try: data["username"]; data["old_password"]; data["new_password"]
            except KeyError:
                logging.warning(f"{request.remote_addr} did not provide enough parameters.")
                return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

            result = chpasswd(data["username"], data["old_password"], data["new_password"])
            if result == True:
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            return result
        
        elif action == "logout_all":
            try: data["token"]
            except KeyError:
                logging.warning(f"{request.remote_addr} did not provide enough parameters.")
                return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

            result = logout_all(data["token"])
            if type(result) is int:
                return json.dumps({"number": result}, ensure_ascii=ensure_ascii), 200, [("Content-Type", "application/json; charset=utf-8")]
            return result
            

        else: 
            logging.warning(f"{request.remote_addr} tried an unsupported action.")
            return json.dumps({"error": "Unsupported action."}, ensure_ascii=ensure_ascii), 422, [("Content-Type", "application/json; charset=utf-8")]
    
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]




@app.get("/")
def root():
    return "This server is currently to be accesed only via the API.", 501 # Todo: send the client program (when it'll be done)

@app.get('/flask-health-check')
def flask_health_check():
	return "success"

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
        try: new_board["name"]
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide enough parameters.")
            return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

        try: result = check_token(new_board["token"])
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide a token.")
            return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        
        if result != True:
            return result
        used_token = new_board["token"]
        new_board.pop("token")

        if not new_board["name"].isalnum():
            logging.warning(f"{request.remote_addr} tried to create a board with invalid name.")
            return json.dumps({"error": "Board name must be alphanumeric (A-Z, a-z, 0-9)."}), 400, [("Content-Type", "application/json; charset=utf-8")]

        for board in board_list:
            if board["name"] == new_board["name"]:
                logging.warning(f"{request.remote_addr} tried to create an existing board.")
                return json.dumps({"error": "Board with designed name already exists."}, ensure_ascii=ensure_ascii), 409, [("Content-Type", "application/json; charset=utf-8")]

        new_board["posts"] = []
        board_list.append(new_board)
        logging.info(f"{request.remote_addr} created a board ({new_board['name']}) as {get_user_from_token(used_token)}.")
        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
    
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.delete("/boards")
def delete_board():
    if request.is_json:
        board_to_delete = request.get_json()
        try: board_to_delete["name"]
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide enough parameters.")
            return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

        try: result = check_token(board_to_delete["token"])
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide a token.")
            return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        
        if result != True:
            return result

        for board in board_list:
            if board["name"] == board_to_delete["name"]:
                board_list.remove(board)
                logging.info(f"{request.remote_addr} deleted a board ({board_to_delete['name']}) as {get_user_from_token(board_to_delete['token'])}.")
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            
        logging.warning(f"{request.remote_addr} tried to access non-existent board.")    
        return json.dumps({"error": "Board does not exist."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.get("/boards/<board_name>")
def posts_on_board(board_name):
    for board in board_list:
        if board["name"] == board_name:
            return json.dumps(board["posts"], ensure_ascii=ensure_ascii), 200, [("Content-Type", "application/json; charset=utf-8")]
        
    logging.warning(f"{request.remote_addr} tried to access non-existent board.")     
    return json.dumps({"error": "Board not found."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]

@app.post("/boards/<board_name>")
def add_on_board(board_name):
    if request.is_json:
        new_post = request.get_json()
        try: new_post["title"]; new_post["contents"]
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide enough parameters.")
            return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

        try: result = check_token(new_post["token"])
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide a token.")
            return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        
        new_post["author"] = get_user_from_token(new_post["token"])

        if result != True:
            return result
        used_token = new_post["token"]
        new_post.pop("token")

        
        for board in board_list:
            if board["name"] == board_name:

                if new_post["title"]== "": # If the title is empty string
                    new_post["title"] = "Untitled post"

                if new_post["contents"] == "":
                    new_post["contents"] = "No contents"

                new_post["id"] = len(board["posts"])
                board["posts"].append(new_post)
                logging.info(f"{request.remote_addr} created a post ({new_post['name']}) as {get_user_from_token(used_token)}.")
                return "", 204, [("Content-Type", "application/json; charset=utf-8")]
            
        logging.warning(f"{request.remote_addr} tried to access non-existent board.")
        return json.dumps({"error": "Board does not exist."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]    
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]

@app.delete("/boards/<board_name>")
def delete_post(board_name):
    if request.is_json:
        post_to_delete = request.get_json()
        try: post_to_delete["id"]
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide enough parameters.")
            return json.dumps({"error": "Missing parameters."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

        try: result = check_token(post_to_delete["token"])
        except KeyError:
            logging.warning(f"{request.remote_addr} did not provide a token.")
            return json.dumps({"error": "Token not provided."}, ensure_ascii=ensure_ascii), 401, [("Content-Type", "application/json; charset=utf-8")]
        
        if result != True:
            return result

        for board in board_list:
            if board["name"] == board_name:
                for post in board["posts"]:
                    if post["id"] == post_to_delete["id"]:
                        board["posts"].remove(post)
                        logging.info(f"{request.remote_addr} deleted a post ({post_to_delete['name']}) as {get_user_from_token(post_to_delete['token'])}.")
                        return "", 204, [("Content-Type", "application/json; charset=utf-8")]
                
                logging.warning(f"{request.remote_addr} tried to delete non-existent post.")
                return json.dumps({"error": "Post with designed ID does not exist in this board."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]
            
        logging.warning(f"{request.remote_addr} tried to access non-existent board.") 
        return json.dumps({"error": "Board does not exist."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]
    return json.dumps({"error": "Request must be JSON."}, ensure_ascii=ensure_ascii), 415, [("Content-Type", "application/json; charset=utf-8")]




@app.errorhandler(400)
def err_400(error):
    logging.warning(f"{request.remote_addr} sent a malformed request.")
    return json.dumps({"error": "The request was malformed."}, ensure_ascii=ensure_ascii), 400, [("Content-Type", "application/json; charset=utf-8")]

@app.errorhandler(404)
def err_404(error):
    logging.warning(f"{request.remote_addr} tried to access non-existent endpoint.")
    return json.dumps({"error": "Requested endpoint can't be found."}, ensure_ascii=ensure_ascii), 404, [("Content-Type", "application/json; charset=utf-8")]

@app.errorhandler(405)
def err_405(error):
    logging.warning(f"{request.remote_addr} tried to access an endpoint using invalid method.")
    return json.dumps({"error": "Method not allowed."}, ensure_ascii=ensure_ascii), 405, [("Content-Type", "application/json; charset=utf-8")]

@app.errorhandler(500)
def err_500(error):
    logging.error(f"Internal server error caused by a request from {request.remote_addr}")
    return json.dumps({"error": "Internal server error. Please notify the administrator."}, ensure_ascii=ensure_ascii), 500, [("Content-Type", "application/json; charset=utf-8")]




if treat_ufw:
    logging.info("Adding UFW rule...")
    system(f"sudo ufw allow {port}/tcp")
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=port) # If debug=True, any changes to the JSON DB
                         # will be discarded after exiting or reload
                         # It's easier to use VSCode's debugger for Flask
if treat_ufw:
    logging.info("Deleting UFW rule...")
    system(f"sudo ufw delete allow {port}/tcp")

save_db()
logging.info("Quitting...")