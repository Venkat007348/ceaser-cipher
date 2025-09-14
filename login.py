def check_login(username, password):
    users = {
        "alice": "1234",
        "bob": "abcd"
    }
    return users.get(username) == password
