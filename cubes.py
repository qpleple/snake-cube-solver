#!/usr/bin/env python

import numpy as np

i, j, k = np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])
six = [i, j, k, -i, -j, -k]
vectors = {
    tuple(i): 'i', tuple(j): 'j', tuple(k): 'k',
    tuple(-i): '-i', tuple(-j): '-j', tuple(-k): '-k',
}

class Cube90(object):
    position = np.array([0, 0, 0])
    orientation_top = k
    orientation_next = i

    def possible_orientation_top(self):
        return six

    def possible_orientation_next(self):
        return [v for v in six if np.dot(v, self.orientation_top) == 0]

    def position_next(self):
        return self.position + self.orientation_next

    def description(self):
        return "{} top={} next={}".format(self.position + np.array([1,1,1]), vectors[tuple(self.orientation_top)], vectors[tuple(self.orientation_next)])


class Cube180(Cube90):
    orientation_top = k
    orientation_next = -k

    def possible_orientation_next(self):
        return [-self.orientation_top]

    def description(self):
        return super(Cube180, self).description() + ' (180)'

def update_box(box, cube):
    (x_min, x_max, y_min, y_max, z_min, z_max) = box
    x, y, z = tuple(cube.position)
    return (min(x, x_min), max(x, x_max), min(y, y_min), max(y, y_max), min(z, z_min), max(z, z_max))

def is_box_valid(box):
    (x_min, x_max, y_min, y_max, z_min, z_max) = box
    return x_max - x_min <= 2 and y_max - y_min <= 2 and z_max - z_min <= 2

def explore(chain_done, chain_todo, box, visited):
    if chain_todo == []:
        print "\n".join(c.description() for c in chain_done)
        return True

    cube = chain_todo[0]
    previous = chain_done[-1]
    cube.position = previous.position_next()
    cube.orientation_top = -previous.orientation_next
    t = tuple(cube.position)
    box = update_box(box, cube)
    if t in visited or not is_box_valid(box):
        return False
    
    for o in cube.possible_orientation_next():
        cube.orientation_next = o
        if explore(chain_done + [cube], chain_todo[1:], box, visited + [t]):
            return True

    return False

def build_chain():
    return [Cube90() if c == 'L' else Cube180() for c in 'LLLLL-L-LLLLLLLLLLL-L-LLLLL']

chain = build_chain()
box = update_box((0,0,0,0,0,0), chain[0])
visited = [tuple(chain[0].position)]
print explore([chain[0]], chain[1:], box, visited)