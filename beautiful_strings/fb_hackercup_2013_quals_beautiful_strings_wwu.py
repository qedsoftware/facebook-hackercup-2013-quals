#!/usr/bin/env python
# William Wu <William.Wu@themathpath.com>, 2013-01-25
# Facebook Hacker Cup 2013 Qualification Round
# 20: Beautiful strings
import os, sys, re
input_file = open(sys.argv[1])
line_count = 0
max_lines = 0 
while 1:
    line = input_file.readline()
    if not line:
        break
    else:
        if line_count == 0:
            max_lines = int(line)
        else:
            # remove non-alphabetic characters and convert to lowercase
            line_filtered = re.sub(r'[^A-Za-z]+', '', line).lower()            
            # generate histogram
            hist = {}
            for c in line_filtered:
                hist[c] = hist.get(c, 0) + 1
            # sort histogram counts
            sorted_counts = sorted(hist.values(),reverse=True);
            # construct maximum score via greedy algorithm
            score = 0;
            for k in xrange(0,len(sorted_counts)):
                score += sorted_counts[k]*(26 - k)
            print("Case #%d: %d" % (line_count, score))
        line_count += 1