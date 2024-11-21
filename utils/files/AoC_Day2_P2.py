import re

fname = "AoC_Day2.in"

with open(fname, "r") as f:
    lines = f.readlines()


ans = 0

for k in range(len(lines)):
    line = lines[k]
    line = re.sub("\n", "", line)
    sets = line[line.index(":")+2:].split("; ")
    for i in range(len(sets)):
        sets[i] = sets[i].split(", ")
        for j in range(len(sets[i])):
            sets[i][j] = sets[i][j].split(" ")
            sets[i][j][0] = int(sets[i][j][0])
    

    ansBlue = ansRed = ansGreen = 0
    # print(sets)
    for j in range(len(sets)):
        blue = red = green = 0
        s = sets[j]
        for p in s:
            # print(p)
            if p[1] == "red":
                red += p[0]
            elif p[1] == "blue":
                blue += p[0]
            elif p[1] == "green":
                green += p[0]
        ansBlue = max(blue, ansBlue)
        ansRed = max(red, ansRed)
        ansGreen = max(green, ansGreen)
    
        # print(red, green, blue)
        
    ans += ansBlue*ansRed*ansGreen


print(ans)