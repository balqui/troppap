'''
cannedveg: 276
frozenmeal: 268
beer: 255
fruitveg: 255
wine: 251
confectionery: 248
fish: 245

size 0: 1 closures
size 1: 7 closures
size 2: 21 closures
size 3: 35 closures
size 4: 32 closures
size 5: 14 closures
size 6: 4 closures
size 7: 1 closures
'''

keep = set(('confectionery', 'cannedveg', 'frozenmeal', 'beer', 'fish', 'wine', 'fruitveg'))
cnt = 0
with open("markbask.txt") as data:
    with open("minimarket.txt", "w") as reduced:
        for line in data:
            tr = keep.intersection(line.split())
            if len(tr) > 1:
                cnt += 1
                reduced.write(' '.join(tr) + '\n')
print(cnt)

