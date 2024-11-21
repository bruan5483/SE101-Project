import re
fname = "AoC_Day3.in"

with open(fname, "r") as f:
    lines = f.readlines()


    

for i in range(len(lines)):
    lines[i] = re.sub("\n", "", lines[i])

lines = [[y for y in x] for x in lines]


ans = 0

for i in range(len(lines)):
    for j in range(len(lines[i])):
        symbol = False
        try:
            int(lines[i][j])
            num = lines[i][j]
                
            for c in range(i, i + len(num)):
                try:
                    for dir in [[0, 1], [1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1], [-1, 0], [0, -1]]:
                        nRow = i + dir[0]
                        nCol = j + dir[1]
                        int(lines[nRow][nCol])
                except:
                    if lines[nRow][nCol] != ".":
                        ans += int(num)
                        break
        except:
            num = ""
            continue

print(ans)