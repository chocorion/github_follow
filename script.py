#!/usr/bin/env python3

import requests, sys

baseUrl = "http://api.github.com/users/"
firstUser = input("First user name : ")

try:
    depth = int(input("Depth : "))
except:
    print("Depth must be an int, greater than 0 !")
    sys.exit(1)


userTab = {
    firstUser: list()
}

def getUser(username):
    r = requests.get(baseUrl + username)

    if (r.status_code == 200):
        return r.json()

    return None

def getFollowing(username):
    r = requests.get(baseUrl + username + "/following")

    if (r.status_code == 200):
        return r.json()

    return None


if __name__ == "__main__":
    current_user = [firstUser]

    for i in range(depth):
        new_user = []

        for user in current_user:
            following = getFollowing(user)

            if (following == None):
                print("Can't get following for user {}".format(user))
                continue
            
            for following_user in following:
                userTab[user].append(following_user["login"])

                if (following_user["login"] not in userTab):
                    userTab[following_user["login"]] = list()

                    new_user.append(following_user["login"])
        
        current_user = new_user

print(userTab)
#follows = response.json()["following_url"]
#print("follows : {}".format(follows))
