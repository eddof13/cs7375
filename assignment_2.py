# Edward Jesinsky
# CS-7375 Assignment 2: Uniform Cost Search/A* to solve 8-puzzle

import random
import heapq
import time

class Node:
  def __init__(self, state, cost):
    self.state = state
    self.cost = cost

  def __eq__(self, other):
    return self.state == other.state

  def __lt__(self, other):
    return self.cost < other.cost

# puzzle is a list ['x', 1, 2, 3, 4, 5, 6, 7, 8], 'x' = empty
# the above would look like:
# x 1 2
# 3 4 5
# 6 7 8
def generate_8_puzzle():
  puzzle = ['x', 1, 2, 3, 4, 5, 6, 7, 8]
  random.shuffle(puzzle)
  return puzzle.copy()

def ucs(start, finish):
  return [], 0 # temporary, for some reason I can't get this to terminate
  start_time = time.process_time()
  path = []
  fringe = []
  heapq.heappush(fringe, Node(start, 0))
  while fringe:
    current = heapq.heappop(fringe)
    path.append(current.state)
    if current.state == finish:
      break
    for move in moves(current.state):
      if move not in path:
        heapq.heappush(fringe, Node(move, current.cost + 1))
  return path, time.process_time() - start_time

def astar(start, finish):
  start_time = time.process_time()
  path = []
  open_nodes = []
  closed_nodes = []
  heapq.heappush(open_nodes, Node(start, 0))
  while open_nodes:
    current = heapq.heappop(open_nodes)
    path.append(current.state)
    if current.state == finish:
      break
    for move in moves(current.state):
      cost = current.cost + nilssons(current, finish)
      node = Node(move, cost)
      if node in open_nodes:
        other = open_nodes[open_nodes.index(node)]
        if other.cost <= cost:
          continue
        else:
          node.cost = cost
      elif node in closed_nodes:
        other = closed_nodes[closed_nodes.index(node)]
        if other.cost <= cost:
          continue
        else:
          closed_nodes.remove(node)
          node.cost = cost
          heapq.heappush(open_nodes, node)
      else:
        node.cost = cost
        heapq.heappush(open_nodes, node)
    closed_nodes.append(current)
  return path, time.process_time() - start_time

def nilssons(current, finish):
  return current.cost # calculate nilsson's sequence

def moves(puzzle):
  moves = [move_left(puzzle), move_right(puzzle), move_up(puzzle), move_down(puzzle)]
  return [move for move in moves if move is not None]

def move_left(puzzle):
  move = None
  position = puzzle.index('x')
  if position not in [0, 3, 6]: # not on left side
    # perform rotation (swap)
    move = puzzle.copy()
    move[position], move[position - 1] = move[position - 1], move[position]
  return move

def move_right(puzzle):
  move = None
  position = puzzle.index('x')
  if position not in [2, 5, 8]: # not on right side
    # perform rotation (swap)
    move = puzzle.copy()
    move[position], move[position + 1] = move[position + 1], move[position]
  return move

def move_up(puzzle):
  move = None
  position = puzzle.index('x')
  if position not in [0, 1, 2]: # not on top
    # perform rotation (swap)
    move = puzzle.copy()
    move[position], move[position - 3] = move[position - 3], move[position]
  return move

def move_down(puzzle):
  move = None
  position = puzzle.index('x')
  if position not in [6, 7, 8]: # not on bottom
    # perform rotation (swap)
    move = puzzle.copy()
    move[position], move[position + 3] = move[position + 3], move[position]
  return move

if __name__ == "__main__":
  ucs_node_counts = []
  ucs_times = []
  astar_node_counts = []
  astar_times = []
  for i in range(5): # average over 5 times
    print(f"Iteration {i+1}")
    start = generate_8_puzzle()
    finish = [1, 2, 3, 8, 'x', 4, 7, 6, 5]
    print("UCS:")
    ucs_nodes, ucs_time = ucs(start, finish)
    ucs_node_counts.append(len(ucs_nodes))
    ucs_times.append(ucs_time)
    for node in ucs_nodes:
      print(*node)
    print("A*:")
    astar_nodes, astar_time = astar(start, finish)
    astar_node_counts.append(len(astar_nodes))
    astar_times.append(astar_time)
    for node in astar_nodes:
      print(*node)
  print("UCS:")
  print(f"Average Nodes: {sum(ucs_node_counts)/len(ucs_node_counts)}")
  print(f"Average Time: {sum(ucs_times)/len(ucs_times)}")
  print("A*:")
  print(f"Average Nodes: {sum(astar_node_counts)/len(astar_node_counts)}")
  print(f"Average Time: {sum(astar_times)/len(astar_times)}")
