from collections import deque
import sys

# storing the string where we will search the elements
with open(sys.argv[len(sys.argv)-1]) as words:
    with open(sys.argv[len(sys.argv)-1], 'r') as my_file:
        text = my_file.read()
words.close()

# preparation of data array, which contains the
# different words that were given as input
icounter = 0
vOutput = ''
isV = 1
if sys.argv[1] == '-v':
    isV = 2
    vOutput = '-v'
data = []
data = ['' for i in range(isV, len(sys.argv)-1)]
for i in range(isV, len(sys.argv)-1):
    data[icounter] = sys.argv[i]
    icounter += 1
data = [i[::-1] for i in data]

# finds the positions where two words differ
def helper(str1, str2):
    mina = min(str1, str2)
    index = -1
    for z in range(0, len(mina)):
        s1 = str1[z]
        s2 = str2[z]
        if not s1 == s2:
            index = z
            break
    return index


# depth calculation for all the nodes
def find_depths(adjlist):
    def dfs(vertex, depth):
        depths[vertex] = depth
        for neighbor, connection in enumerate(adjlist[vertex]):
            if connection == 1 and depths[neighbor] == -1:
                dfs(neighbor, depth + 1)
    num = len(adjlist)
    depths = [-1] * num
    for vertex in range(num):
        if depths[vertex] == -1:
            dfs(vertex, 0)
    return depths


# supporting method for trie creation, to be used for the adjacency list
def build_trie(string_array):
    trie = {"vertex": 0, "children": {}}
    id = 1
    for s in string_array:
        vertex = trie
        for ch in s:
            if ch not in vertex["children"]:
                current_vertex = {"vertex": id, "children": {}}
                vertex["children"][ch] = current_vertex
                id += 1
            vertex = vertex["children"][ch]
        vertex["final"] = True
    return trie


# creation of the adjacency list through the children of the nodes
def create_adjacency_list(trie):
    result = {}
    def dfs(node):
        vertex = node['vertex']
        children = node['children']
        child_vertices = []
        for key, child_node in children.items():
            child_vertex = child_node['vertex']
            child_vertices.append(child_vertex)
            dfs(child_node)
        result[vertex] = child_vertices
    dfs(trie)
    d = {}
    for vertex, children in result.items():
        d[vertex] = children
    adj = [[0] * len(dictionary) for i in range(len(dictionary))]
    for i in range(len(d)):
        for j in d[i]:
            adj[i][j] = 1
    return adj, d


# the final algorithm, using all data structures of the program
def commentzWalter(t):
    queue = deque()
    i = pmin - 1
    j = 0
    u = 0
    m = ''
    while i < len(t):
        while HasChild(u, t[i-j]):
            u = getChild(u, t[i-j])
            m = m + t[i-j]
            j += 1
            if u in final_nodes:
                queue.append((m[::-1], i-j+1))
        if j > i:
            j = i
        s = min(s2[u], max(s1[u], rt[t[i-j]]-j-1))
        i = i + s
        j = 0
        u = 0
        m = ''
    for w in queue:
        print(": ".join(str(element) for element in w))
    return queue


# determines whether a node has a child with an edge c
def HasChild(u, c):
    for i in children[u]:
        if letters[i] == c:
            return True
    return False

# returns the child of a node that is connected through an edge c
def getChild(u, c):
    for i in children[u]:
        if letters[i] == c:
            return i


# initialisation for first word
letters = []
letters.append("")
dictionary = {}
for i in range(0, len(data[0]), 1):
    dictionary[i] = True
for j in data[0]:
    letters.append(j)
dictionary[len(data[0])] = False

# constructing the dictionary with the nodes of the trie
# the node-key gets the value false if it is final, and true otherwise
for i in range(1, len(data)):
    max1 = -1
    pos = 0
    for j in range(0, i):
        # each time we want to keep the words with greater same prefix
        if helper(data[i], data[j]) > max1:
            pos = j
            max1 = helper(data[i], data[j])
    index = helper(data[i], data[pos])
    final = list(dictionary.keys())[-1]
    for w in range(final + 1, final + len(data[i]) - index):
        dictionary[w] = True
    dictionary[len(dictionary)] = False

# creation of letter array, containing the letters of each edge
counter = 0
wordCount = 1
for i in range(len(letters), len(dictionary)):
    if not dictionary[i]:
        temp = data[wordCount]
        for u in range(len(data[wordCount]) - counter - 1, len(data[wordCount])):
            letters.append(temp[u])
        wordCount += 1
        counter = 0
    else:
        counter += 1

# adjacency matrix
adj, children = create_adjacency_list(build_trie(data))

# building the rt dictionary using the depths
pmin = len(min(data, key=len))
# storing the unique elements that can be found in letters array
unElements = set(letters)
unElements.remove("")
countArr = []
du = {}
depths = find_depths(adj)
for i in unElements:
    minElement = len(depths)
    for j in range(len(letters)):
        if letters[j] == i:
            if depths[j] < minElement:
                minElement = depths[j]
    du[i] = minElement
rt = {}
for i in du:
    rt[i] = min(du[i], pmin + 1)
rt['rest of characters'] = pmin + 1

# creation of failure
# initialisation of values
failure = [-1] * len(depths)
for i in range(0, len(depths)):
    if depths[i] <= 1:
        failure[i] = 0
queue = [0]
visited = [False] * len(adj)
visited[0] = True
visited_vertices = [0]
# starting the BFS
while queue:
    node = queue.pop(0)
    for neighbor, is_connected in enumerate(adj[node]):
        if is_connected and not visited[neighbor]:
            queue.append(neighbor)
            visited[neighbor] = True
            visited_vertices.append(neighbor)
            # calculations for failure
            u = neighbor
            if depths[u] >= 1:
                for v in children[u]:
                    # children check for the first instances
                    c = letters[v]
                    uNew = failure[u]
                    done = False
                    for vNew in children[uNew]:
                        if c == letters[vNew]:
                            failure[v] = vNew
                            done = True
                    if not done:
                        # calculations while we change the uNew
                        # nodes, and we move further up the trie
                        uNew = failure[uNew]
                        while not done and uNew != 0:
                            for vNew in children[uNew]:
                                if c == letters[vNew]:
                                    failure[v] = vNew
                                    done = True
                            uNew = failure[uNew]
                        if not done and uNew == 0:
                            done = True
                            failure[v] = 0


# calculation of set1 values through the failure structure
unique_values = set(failure)
unique_values.remove(0)
set1 = {}
for j in unique_values:
    arr = []
    for i in range(len(failure)):
        if failure[i] == j:
            arr.append(i)
    set1[j] = arr

# calculation of set2 values through the given mathematical formula
final_nodes = []
for i in dictionary:
    if not dictionary[i]:
        final_nodes.append(i)
set2 = {}
for i in set1:
    arr = []
    for j in set1[i]:
        if j in final_nodes:
            arr.append(j)
    if arr:
        set2[i] = arr

# calculation of s1 through the given mathematical formula
root = next(iter(dictionary))
s1 = [0 for i in range(len(dictionary))]
for u in range(len(dictionary)):
    if u == root:
        s1[u] = 1
    else:
        if u in set1:
            for u_new in set1[u]:
                k = depths[u_new] - depths[u]
                s1[u] = min(pmin, k)
        else:
            s1[u] = pmin

# calculation of s2 through the given mathematical formula
s2 = [0 for i in range(len(dictionary))]
for u in range(len(dictionary)):
    if u == root:
        s2[u] = pmin
    else:
        for c in children:
            if u in children[c]:
                parent = c
        if u in set2:
            for u_new in set2[u]:
                k = depths[u_new] - depths[u]
                s2[u] = min(s2[parent], k)
        else:
            s2[u] = s2[parent]

# final presentation
if vOutput == '-v':
    for i in range(0, len(s1)):
        print(i, ": ", s1[i], s2[i])

# Commentz Walter algorithm
commentzWalter(text)
