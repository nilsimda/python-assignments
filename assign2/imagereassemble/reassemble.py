#!/usr/bin/env python3 -tt
"""
File: reassemble.py
-------------------
Assignment 2: Quest for the Holy Grail

Works but is slow for large number of slices, maybe improve
in the future.
"""

import imageutils
import math

def slice_similarity(s1, s2):
    return column_similarity(s1[-1], s2[0])
    
def column_similarity(c1, c2):
    return sum([p_similarity(p1,p2)
                for p1, p2 in zip(c1, c2)])

def p_similarity(p1, p2):
    return sum([(p1.red - p2.red)**2,
                (p1.green-p2.green)**2,
                (p1.blue - p2.blue)**2,
                (p1.alpha - p2.alpha)**2])

def find_pair(slices):
    cache = {}
    for (i, s1) in enumerate(slices): 
        for (ii, s2) in enumerate(slices): 
            if i != ii:
                cache[(i, ii)] = slice_similarity(s1,s2)

    return min(cache.items(), key=lambda x: x[1])[0]

def reassemble(slices):
    while len(slices) > 1:
        print(f"Slices left: {len(slices)}")

        i, ii = find_pair(slices)
        x = slices[i]
        y = slices[ii]
        slices.append(x+y)
        slices.remove(x)
        slices.remove(y)

    return slices[0]
    
if __name__ == '__main__':
    fs = imageutils.files_in_directory("shredded/destination")
    slices=[]
    for f in fs:
        slices.append(imageutils.load_image(f))

    img = reassemble(slices)
    imageutils.save_image(img, "destination.png")
