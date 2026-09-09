'''
cannedveg: 261
frozenmeal: 245
beer: 239
fruitveg: 194
wine: 183

size 0: 1 closure
size 1: 5 closures
size 2: 10 closures
size 3: 10 closures
size 4: 4 closures
size 5: 1 closure
'''

keep = set(('cannedveg', 'frozenmeal', 'beer', 'wine', 'fruitveg'))
cnt = 0
with open("markbask.txt") as data:
    with open("micromarket.txt", "w") as reduced:
        for line in data:
            tr = keep.intersection(line.split())
            if len(tr) > 1:
                cnt += 1
                reduced.write(' '.join(tr) + '\n')
print(cnt)

