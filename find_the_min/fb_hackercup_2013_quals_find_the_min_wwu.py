#!/usr/bin/env python
# William Wu <William.Wu@themathpath.com>, 2013-01-25
# Facebook Hacker Cup 2013 Qualification Round
# 45: Find the Min
import os, sys, re
import collections
from blist import sortedset # B+ tree

input_file = open(sys.argv[1])

# debug flag
debug = False

# number of test cases
line = input_file.readline().strip()
T = int(line)

# process each case
for t in xrange(0,T):
    
    # read parameters
    line1 = input_file.readline().strip()    
    line2 = input_file.readline().strip()        
    n,k = map(int,line1.split())
    a,b,c,r = map(int,line2.split())

    if debug:
        print "n=%d, k=%d" % (n,k)
        print "a=%d, b=%d, c=%d, r=%d" % (a,b,c,r)

    #########################
    # INITIALIZATION
    #########################

    # generate first k values of m
    m = [0]*k
    for i in xrange(0,k):
        if 0==i:
            m[0] = a
        else:
            m[i] = (b*m[i-1] + c) % r
        
    # deque: tracks FIFO queue
    d = collections.deque(m)

    # dictionary: histogram of elements and their counts
    h = {}
    for v in m:
        h[v] = h.get(v,0) + 1

    # b+tree: sorted collection of UNIQUE non-negative elements with no one directly above them, and also including -1 if 0 is not present
    b = sortedset([])
    vals = sorted(h.keys())
    for v in vals:
        if (v+1 not in h) and (v >= 1):
            b.add(v)
    if vals[0] != 0: 
        b.add(-1)


    #########################
    # ITERATIVE UPDATES
    #########################
    # for i in xrange(0,n-k)
    # key observation: 
    # 1. the smallest non-negative integer not present amongst k numbers must be between 0 and k
    # 2. therefore, after k+1 iterations, we have flushed the initial state out of the system, and the resulting sequence is periodic
    # 3. so the runtime is not O( (k log k) n ), but rather, O( k log k), or maybe even better
    z = [0]*(k+1)
    for i in xrange(0,k+1): 

        if debug:
            print d
            # print b
            # print (["%s: %s" % (v, h[v]) for v in sorted(h.keys())])
            print ""

        # 1. b+tree: determine new element to add in O(1)
        new = b[0]+1

        # 1.5 check:
        if new in h:
            print "Error: trying to add an allegedly new element when it is already present: %d" % new
            sys.exit()

        # 2. deque: find "old" element to remove in O(1) by popping
        old = d.popleft()

        # 3. dictionary: decrement count of "old" accordingly, removing keys completely if count = 0 (both to avoid size blowup and to test set membership quickly)
        if old in h:
            if h[old] <= 1: # should not be possible for h[old] <= 0
                h.pop(old,None)
            else:
                h[old] -= 1
                    
        # 4. deque: push new element
        d.append(new)
        
        # 5. dictionary: increment count of "new" accordingly --- this is supposed to be a new element
        h[new] = 1
        
        # 6. b+tree updates:
        # (a) removing old, part 1:
        #       if there are ZERO old's left in h, then remove old from b+tree
        if (old not in h):
            b.discard(old)
        # (b) removing old, part 2:
        #       if there are ZERO old's left in h, AND old-1 is in h, then add old-1 to b+tree
        if (old not in h) and ((old-1) in h):
            b.add(old-1)
        # (c) inserting new, part 1:
        #       if new-1 is in b+tree, then remove new-1 from b+tree
        if ((new-1) in b):
            b.discard(new-1)
        # (d) inserting new, part 2:
        #       if new+1 does not exist, then add new to b+tree
        if ((new+1) not in h):
            b.add(new)

        # note: since b is a SET, it will not contain duplicates, so we need not worry about the case where new = old - 1 ---> we cannot add the same number twice

        # track newly generated elements
        z[i] = new

    # output answer    
    print "Case #%d: %s" % (t+1, z[(n-k-1) % (k+1)])