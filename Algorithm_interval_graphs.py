import sys
from collections import deque

with open(sys.argv[2]) as words:
    with open(sys.argv[2], 'r') as my_file:
        data1 = my_file.read()
words.close()
data = [int(i) for i in data1.split()]
inner_list = []
graph = []

for item in data:
    inner_list.append(item)
    if len(inner_list) == 2:
        graph.append(inner_list)
        inner_list = []
if inner_list:
    graph.append(inner_list)

arr = set()
for i in graph:
    for j in i:
        arr.add(j)
sigma = []
sigma.append(arr)
visited = []
adjacency_list = {}

for pair in graph:
    v1, v2 = pair

    if v1 not in adjacency_list:
        adjacency_list[v1] = []
    if v2 not in adjacency_list:
        adjacency_list[v2] = []
    adjacency_list[v1].append(v2)
    adjacency_list[v2].append(v1)

def lexbfs(sigma, adjacency_list, arr, visited):
    # convert sets to lists to not lose the index
    listed = []
    for s in sigma:
        listed.append(list(s))
    # While list is empty
    for z in range(0, len(arr), 1):

        # add the first element from first set in visited array
        u = min(listed[0])
        visited.append(min(listed[0]))
        # remove an element from first set
        listed[0].remove(min(listed[0]))
        # remove first empty set
        if (len(listed[0]) == 0):
            listed.remove(listed[0])
        # searching for the neighbors in the inner lists
        neigh = {}
        for j in adjacency_list[u]:
            if j not in visited:
                index = None
                for i, sublist in enumerate(listed):
                    if j in sublist:
                        index = i
                        break
                if index not in neigh:
                    neigh[index] = []
                neigh[index].append(j)
                listed[index].remove(j)
        # insert the new lists before the S lists
        gr = 0
        for w in neigh:
            if w == 0:
                listed.insert(w, neigh[w])
                gr = 1
            else:
                listed.insert(gr + w, neigh[w])
                gr = gr + 1
        # remove all S lists that are empty
        for ind in listed:
            if ind == []:
                listed.remove(ind)
    if sys.argv[1] == "lexbfs":
        print(visited)
    return visited

def chordal(visited, adjacency_list):
    lexbfs(sigma, adjacency_list, arr, visited)
    revL = visited[::-1]
    res = True
    i = revL[0]
    index = 0
    metrit = 0
    while res and metrit < len(revL) - 1:
        val = adjacency_list[i]

        closest_element = None
        for element in val:
            if element >= i:
                break
            closest_element = element
        first = closest_element
        indFirst = revL.index(first)

        neI = []
        neF = []
        for j in revL[index + 1:]:
            if j in val:
                neI.append(j)
            neI.sort()
        for j in revL[indFirst + 1:]:
            if j in adjacency_list[first]:
                neF.append(j)
            neF.sort()
        if first in neI:
            neI.remove(first)

        if set(neI).issubset(set(neF)):
            res = True
        else:
            res = False
        if index < len(revL):
            index += 1
            if index <= len(revL) - 1:
                i = revL[index]
        metrit += 1
    if sys.argv[1] == "chordal":
        print(res)
    return res

def interval(adjacency_list, visited):
    res = chordal(visited, adjacency_list)
    remaining_components = {}
    # Step 1
    for node in adjacency_list:
        visited = []
        remaining_components[node] = []
        deq = deque([node])
        visited.append(node)
        components = [node]

        while deq:
            current_node = deq.popleft()

            for neighbor in adjacency_list[current_node]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    components.append(neighbor)
                    deq.append(neighbor)

        remaining_components[node].extend(components)

    # Step 2
    V = len(adjacency_list)
    cArr = [[0] * V for _ in range(V)]
    node_to_index = {node: index for index, node in enumerate(adjacency_list)}
    # Fill the list based on the adjacency list and components dictionary
    for u, neighbors in adjacency_list.items():
        uind = node_to_index[u]
        ucomp = components[u]
        for v in neighbors:
            v_index = node_to_index[v]
            cArr[uind][v_index] = remaining_components[ucomp]
            if uind in cArr[uind][v_index]:
                cArr[uind][v_index].remove(uind)
            for w in adjacency_list[uind]:
                if w in cArr[uind][v_index]:
                    cArr[uind][v_index].remove(w)
    vertices = list(adjacency_list.keys())
    teams = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            for k in range(j + 1, len(vertices)):
                vertex1 = vertices[i]
                vertex2 = vertices[j]
                vertex3 = vertices[k]
                if vertex2 not in adjacency_list[vertex1] and vertex3 not in adjacency_list[vertex1] and vertex2 not in \
                        adjacency_list[vertex3]:
                    teams.append(list((vertex1, vertex2, vertex3)))

    # Step 3: Compare the components for each element of the teams
    atfree = True
    for i in teams:
        triple = i[0]
        if cArr[i[0]][i[1]] == cArr[i[0]][i[2]] and cArr[i[1]][i[0]] == cArr[i[1]][i[2]] \
                and cArr[i[2]][i[0]] == cArr[i[2]][i[1]] and cArr[i[0]][i[1]] != 0 and cArr[i[0]][i[2]] != 0 \
                and cArr[i[1]][i[0]] != 0 and cArr[i[1]][i[2]] != 0 and cArr[i[2]][i[0]] != 0 and cArr[i[2]][i[1]] != 0:
            atfree = False
    if atfree == True and res == True:
        print(atfree)
        return atfree
    else:
        print(False)
        return False

if sys.argv[1] == "lexbfs":
    lexbfs(sigma, adjacency_list, arr, visited)
elif sys.argv[1] == "chordal":
    chordal(visited, adjacency_list)
elif sys.argv[1] == "interval":
    interval(adjacency_list, visited)
