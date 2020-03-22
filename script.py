#!/usr/bin/env python3

import requests, sys

import matplotlib.pyplot as plt
import networkx as nx

baseUrl = "http://api.github.com/users/"
firstUser = input("First user name : ")

try:
    depth = int(input("Depth : "))
except:
    print("Depth must be an int, greater than 0 !")
    sys.exit(1)

try:
    with open('token.txt') as file:
        token = file.readline()
        token = token[:len(token)]
except:
    print("You need to create a file token.txt with a github token inside !")
    sys.exit(0)


userTab = {
    firstUser: list()
}

def getUser(username):
    r = requests.get(baseUrl + username, auth=('token', token))

    if (r.status_code == 200):
        return r.json()

    print("Warning : getUser, status code {}".format(r.status_code))
    return None

def getFollowing(username):
    r = requests.get(baseUrl + username + "/following", auth=('token', token))

    if (r.status_code == 200):
        return r.json()

    print("Warning : getFollowing, status code {}".format(r.status_code))
    return None

def getPopularity():
    popularity = dict()

    for user in userTab.keys():
        popularity[user] = 0

    for user in userTab.keys():
        for followed in userTab[user]:
            popularity[followed] += 1

    return popularity    

def createGraph():
    G = nx.MultiDiGraph()
    users = userTab.keys()

    popularity = getPopularity()

    for user in users:
        G.add_node(user, size=popularity[user])
    
    for user in users:
        for following in userTab[user]:
            G.add_edge(user, following)

    return G


if __name__ == "__main__":
    current_user = [firstUser]

    for i in range(depth):
        new_user = []

        for user in current_user:
            print("Checking user {}".format(user))
            following = getFollowing(user)
            
            if (following == None):
                print("\tCan't get following for this user...")
                continue
            print("\t following {} persons : {{ ".format(len(following)), end="")
            for following_user in following:
                print("{} ".format(following_user["login"]), end="")
                userTab[user].append(following_user["login"])

                if (following_user["login"] not in userTab):
                    userTab[following_user["login"]] = list()

                    new_user.append(following_user["login"])
            print("}")
        
        current_user = new_user

    print(getPopularity())

    graph = createGraph()
    pos = nx.spring_layout(graph, iterations=10)
    nx.draw(graph, pos, node_size=0, alpha=0.7, edge_color='r', font_size=13, with_labels=True)

    plt.show()




