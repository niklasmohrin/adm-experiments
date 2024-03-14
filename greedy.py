# This is a sample Python script.
import tsp_utils as tspu
# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import random
import matplotlib.pyplot as plt
import numpy as np
def plot(points, path):
    X = []
    Y = []
    for (x, y) in points:
        X.append(x)
        Y.append(y)
    x = []
    y = []
    for i in path:
        x.append(X[i])
        y.append(Y[i])
    print(x)
    print(y)
    plt.plot(x, y)
    plt.title("path")
    plt.show()
def greedy_chose(n, max):
    points, dist = tspu.randomEuclGraph(n,100)
    distances = np.zeros(shape=(n,n))
    for ((u,v),z) in dist.items() :
        distances[u][v] = z
    already_visited = [0]
    max_g = max
    path = [0]
    sec = []
    n_iter = 0
    for i in range(n):
        sec.append(i)
    while len(path)!=n :

        for i,j in enumerate(distances[path[-1]:]):
            if n_iter == n-1:
                break
            print('n_iter: ' + str(n_iter) + ' path:' + str(path))
            n_iter += 1
            keys = j.argsort()[1:max_g+1] #Keys has the indexes of the max_g nearest neighbours excluding the first bc it's itself
            random_array = np.arange(max_g) # I use a random array to select random indixes from keys
            random.shuffle(random_array) # Here it becomes random
            appended = False
            for k in random_array:
                if int(keys[k]) not in map(int, path):
                    path.append(keys[k])
                    appended = True
                    break
            if appended == False:
                while True:
                    random_choice = random.choice(sec)
                    if random_choice not in map(int,path):
                        break
                path.append(random_choice)

    print("solution path" + str(path))
    print(points)
    plot(points, path)
if __name__ == '__main__':
    greedy_chose(10,2)

