
fname = "AoC_Day1.in"

with open(fname, 'r') as f:
    inp = f.readlines()

ans = 0



for line in inp:
    first = -1
    last = -1

    for i in range(len(line)):
        try: 
            int(line[i])
            if first == -1:
                first = i
            else:
                last = i
        except:
            pass
    if first != -1 and last != -1:
        ans += int(line[first]+line[last])
    elif first != -1:
        ans += int(line[first]*2)

print(ans)