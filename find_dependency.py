import collections

def buildlist(edge):
    gmap = collections.OrderedDict()
    for v in edge:
        start, end = v
        if start in gmap:
            gmap[start].append(end)
        else:
            gmap[start] = [end]
    return gmap


def finddep(gmap, nodelist, visited, output, index):
    if index == len(nodelist):
        print output
        return
    start = nodelist[index]
    output.append(start)
    visited[start] = 1
    if start in gmap:
        next = gmap[start]
        for v in next:
            if visited[v] == 0:
               finddep(gmap, nodelist, visited, v, output, index + 1)
               visited[start] = 0
    finddep(gmap, nodelist, visited, output, index + 1)



nodecount  =  4
edge = [[1,0],[2,0],[3,1],[3,2]]
nodelist = [i for i in range(nodecount)]
visited ={i: 0 for i in range(nodecount) }
gmap = buildlist(edge)
start = nodelist[0]
finddep(gmap, nodelist, visited, [], 0)