"""
Tests for nonce items, closures of singletons, 
and other expectedly-low-support conditions.
"""

from collections import Counter

from dataset import Dataset
from hyperparam import HyperParam




# ~ fnm = "markbask"
# ~ fnm = "supermarket"
# ~ fnm = "adultrain"
# ~ fnm = "cmc-full"
# ~ fnm = "chess.td"
# ~ fnm = "connect.td"
# ~ fnm = "mushroomTr" 
# ~ fnm = "votesTr" 
fnm = "NOW" 
# ~ fnm = "papersTr"

if fnm.endswith('.td') or fnm.endswith('.txt'):
    filenamefull = fnm
    filename, _ = fnm.rsplit('.',1)
else:
    filename = fnm
    filenamefull = fnm + ".txt" # of ".td" one day...

try:
    datafile = open(filenamefull)
    assert datafile._checkReadable()
    print("File is now open.")
except (IOError, OSError, AssertionError):
    print("Nonexistent or unreadable file.")
    exit(1)

hpar = HyperParam()
print("Reading in dataset from file", filenamefull)
d = Dataset(datafile, hpar)
print(f"{len(d.univ)} items.") 
cnt = Counter()
cnt_cl_singl = 0
tlen = 0
seen = set()
for it in d.occurncs:
    if len(d.occurncs[it]) < 8:
        cnt[len(d.occurncs[it])] += 1
    if len(d.occurncs[it]) == 1 and it not in seen:
        seen.update(d.inters(d.occurncs[it]))
        cnt_cl_singl += 1
        tlen += len(d.inters(d.occurncs[it]))
        # ~ if cnt_cl_singl == 25: break

print(cnt)

print(cnt_cl_singl, tlen/cnt_cl_singl)

    # ~ if len(d.occurncs[it]) < 4 and it not in seen:
        # ~ print(cnt, len(d.occurncs[it]), d.inters(d.occurncs[it]))
        # ~ seen.update(d.inters(d.occurncs[it]))
        # ~ cnt += 1
        # ~ if cnt == 25: break
