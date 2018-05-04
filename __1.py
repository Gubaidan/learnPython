
def permute(nums):
    dp = [[0]*3 for _ in range(3)]
    tem = (0,0,0)
    for i in range(3):
        for j in range(3):
            if nums[i][j] == 1:
                if tem[2] == 0:
                    dp[i][j] = 0
                    t = tem[2] + 1
                    tem = (i, j, t)
                else:
                    if i == 0:
                        dp[i][j] = dp[tem[0]][tem[1]] + tem[2]
                        t = tem[2] + 1
                        tem = (i, j, t)
                    else:
                        tem[1] != dp[tem[0]][tem[1]] + tem[2] + dp[tem[0]][tem[1]]*tem[2]
T = int(input())
l = []
for i in range(T):
    l1 = input()
    l2 = input()
    l3 = input()
    l.append((l1,l2,l3))
grid = [[0]*3 for _ in range(3)]
print(grid)
for tem in l:
    for i in range(len(tem)):
        for j in range(len(tem[i])):
            if tem[i][j] == '.':
                grid[i][j] = 1

    dp = permute(grid)
    res = []
    for i in range(2,-1,-1):
        for j in range(2,-1,-1):
            if grid[i][j] == 1:
                res.append(dp[i][j])
    print(max(res))

