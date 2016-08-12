class countislands(object):

    def __init__(self, island, rowno, columnno):
        self.island = island
        self.rows = rowno
        self.column = columnno
        self.visited = {(i,j) : 0 for i in range(self.rows) for j in range(self.column)}
        '''
         For dfs we need to find the path along X and Y
        '''
        self.x_path = [-1, -1, -1,  0, 0,  1, 1, 1]
        self.y_path = [-1,  0,  1, -1, 1, -1, 0, 1]

    def issafe(self, x, y):
        return (x >= 0 and x < self.rows)\
               and (y >= 0 and y < self.column) \
                and not self.visited[(x,y)]\
                  and self.island[x][y]

    def dfs(self, i, j):
         self.visited[(i, j)] = True
         for x, y in zip(self.x_path, self.y_path):
             if self.issafe(i + x, j + y):
                 self.dfs(i+x, j+y)

    def countisland(self):
        count = 0
        for i in range(self.rows):
            for j in range(self.column):
               if self.island[i][j] and not self.visited[(i, j)]:
                  self.dfs(i, j)
                  count += 1

        return count

island = [[1, 1, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1]]
A=countislands(island, 5, 5)
print A.countisland()
