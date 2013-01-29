#!/usr/bin/env python
# William Wu <William.Wu@themathpath.com>, 2013-01-25
# Facebook Hacker Cup 2013 Qualification Round
# 35: Balanced Smileys
import os, sys, re

input_file = open(sys.argv[1])
line_count = 0
max_lines = 0 
debug = False

# number of test cases
line = input_file.readline().strip()
T = int(line)

# process each case
for t in xrange(0,T):
    # read line
    line = input_file.readline().strip()    
    if "" == line: # empty string
        print("Case #%d: YES" % (t+1))
    elif not re.match(re.compile("^[A-Za-z :\(\)]*$"),line): # strange chars
        print("Case #%d: NO" % (t+1))
    else: 
        # DYNAMIC PROGRAMMING WITH MEMOIZATION
        # A[i][j] = line[i:j+1] is balanced ?
        # A[i][j] = the substring from i to j inclusive is balanced ?
        # important detail: 
        # python slicing has the first index as inclusive and the second index as exclusive. 
        # but my memoization array is inclusive on both ends.

        # initialization
        n = len(line)
        A = [[0 for i in range(n)] for j in range(n)]
        for i in range(0,n): 
            for j in range(0,i):
                A[i][j] = True # empty strings

        # zig-zag upwards starting from bottom of matrix                
        for i in range(n-1,-1,-1): # i ranges from n-1 to 0
            for j in range(i,n): # j ranges from i to n-1
                substr = line[i:j+1] # substring from i to j inclusive
                if debug: print "i=%d, j=%d, substr=%s" % (i,j,substr)
                if "" == substr: # empty string
                    A[i][j] = True
                elif re.match(re.compile("^[a-z :]$"),substr): # single character
                    A[i][j] = True
                elif ":(" == substr or ":)" == substr: # emoticon
                    A[i][j] = True
                elif len(substr) >= 2 and substr[0] == '(' and substr[-1] == ')' and A[i+1][j-1]: # nested
                    A[i][j] = True
                else: # try all possible split locations
                    successful_split = False
                    for k in xrange(i,j):
                        if debug: 
                            print "===================="
                            print "\tk=%d" % k
                            print "\t\tpart1> %s" % line[i:k+1]
                            print "\t\tpart2> %s" % line[k+1:j+1]
                        if A[i][k] and A[k+1][j]:
                            successful_split = True
                            break
                    if successful_split:
                        A[i][j] = True
                    else: 
                        A[i][j] = False

        # print memoization array
        if debug:
            for i in range(0,n):
                for j in range(0,n): 
                    # sys.stdout.write("%5s " % (A[i][j]))
                    sys.stdout.write("%5s [%10s] " % (A[i][j], line[i:j+1]))
                sys.stdout.write("\n")
    
        # output answer    
        print("Case #%d: %s" % (t+1,"YES" if A[0][n-1] else "NO"))