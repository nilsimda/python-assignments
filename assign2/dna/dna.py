#!/usr/bin/env python3 -tt
"""
File: dna.py
------------
Assignment 2: Quest for the Holy Grail

Replace this with a description of the program.
"""

def min_distance(start, end) -> int:
    cache = {}
    def rec_dist(l1, l2):
        if (l1,l2) in cache:
            return cache[(l1,l2)]
        elif l1 == 0:
            result = l2 
        elif l2 == 0:
            result = l1
        elif start[l1-1] == end[l2-1]:
            result = rec_dist(l1-1, l2-1) 
        else: 
            subs = 1 + rec_dist(l1-1, l2-1)
            inse = 1 + rec_dist(l1, l2-1) 
            dele = 1 + rec_dist(l1-1, l2)
            result = min(inse, dele, subs)
        cache[(l1,l2)] = result
        return result
    return rec_dist(len(start), len(end))

"""
TODO
(1) Reads DNA strands from a file formatted as:
	startSequence1	endSequence1
	startSequence2	endSequence2
	...
	startSequenceN	endSequenceN
	Each start/end pair is on its own line, and the start and end strands
	are separated by a tab.
(2) Compute minimum edit distance between each pair.
(3) Output the total number of edits required for all DNA transformations
    in the file. Use this as the key from the next part of the assignment.
	"""
if __name__ == '__main__':
    DATA_FILE = 'dna.txt'
	# Read DNA strands from file
    dna =[] 
    with open(DATA_FILE, 'r') as f:
        for line in f:
            dna.append(line[:-1].split("\t"))

	# Use the min_distance function to compute the edit distance for each pair
	# Output the total number of edits
    print(sum([min_distance(*pair) for pair in dna]))

