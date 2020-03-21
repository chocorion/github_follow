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
except:
    print("You need to create a file token.txt with a github token inside !")


print(token)

sys.exit(0)
userTab = {
    firstUser: list()
}

def getUser(username):
    r = requests.get(baseUrl + username, auth=('token', '0f3309802e6b1f8f346577761fb21ab81aea43ca'))

    if (r.status_code == 200):
        return r.json()

    return None

def getFollowing(username):
    r = requests.get(baseUrl + username + "/following", auth=('token', '0f3309802e6b1f8f346577761fb21ab81aea43ca'))

    if (r.status_code == 200):
        return r.json()

    return None


def createGraph():
    G = nx.MultiDiGraph()
    
    for user in userTab.keys():
        for following in userTab[user]:
            G.add_edge(user, following)

    return G


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

    graph = createGraph()
    pos = nx.spring_layout(graph, iterations=10)
    nx.draw(graph, pos, node_size=0, alpha=0.4, edge_color='r', font_size=16, with_labels=True)

    plt.show()




