import math
from Graph import Graph
from evolutionsystem.EvolutionSystem import EvolutionSystem

def line_eq(point1, point2):
  if point2[0] - point1[0] == 0:
    return 9999, -9999

  slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
  intercept = (point2[1] - (slope * point2[0]))
  return slope, intercept

def lines_intersect(points1, points2):
  slope1, intercept1 = line_eq(points1[0], points1[1])
  slope2, intercept2 = line_eq(points2[0], points2[1])
  if slope1 == slope2:
    return False

  x = (intercept2 - intercept1) / (slope1 - slope2)

  min_1 = min(points1[0][0], points1[1][0])
  max_1 = max(points1[0][0], points1[1][0])
  min_2 = min(points2[0][0], points2[1][0])
  max_2 = max(points2[0][0], points2[1][0])

  return x >= min_1 and x <= max_1 and x >= min_2 and x <= max_2


def get_intersecting_edges(solution, edges):
  mapping = {
    'Jeju': 0,
    'Busan': 1,
    'SeoulMetro': 2,
    'Pohang': 3,
    'Seoul': 4,
    'Cheongju': 5,
    'Sacheon': 6,
    'Daegu': 7
  }

  ls = set()

  num = 0
  for node1 in edges.keys():
    for node2 in edges[node1]:
      points = (solution[mapping[node1]], solution[mapping[node2]])
      ls.add(points)

  for points1 in ls:
    for points2 in ls:
      same = points1 == points2 or points1[0] in points2 or points1[1] in points2
      if not same and lines_intersect(points1, points2):
        num += 1

  return num


def get_average_distance_between_nodes(solution):
  min_dist = float('inf')
  dist = 0
  for i in solution:
    for j in solution:
      if i != j:
        dist += math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        if dist < min_dist:
          min_dist = dist
  return (dist / len(solution), min_dist)
  

def prnt(grid):
  print(' ' + '_' * len(grid))
  for row in grid:
    print('|' + ''.join(row) + '|')
  print(' ' + '-' * len(grid))


def draw_line(grid, start, end):
  slope, _ = line_eq(start, end)

  x_mov = 1
  if slope > len(grid):
    slope = 1
    x_mov = 0

  if start[0] > end[0]:
    x_mov *= -1

  if start[1] < end[1]:
    slope = abs(slope)
  else:
    slope = -abs(slope)

  x = start[0] + x_mov
  y = math.floor(start[1] + slope)

  while x <= max(start[0], end[0]) and x >= min(start[0], end[0]) and y <= max(start[1], end[1]) and y >= min(start[1], end[1]):
    if grid[math.floor(y)][x] == ' ':
      grid[math.floor(y)][x] = '*'
    x += x_mov
    y += slope


def draw(solution, edges):
  mapping = {
    'Jeju': 0,
    'Busan': 1,
    'SeoulMetro': 2,
    'Pohang': 3,
    'Seoul': 4,
    'Cheongju': 5,
    'Sacheon': 6,
    'Daegu': 7
  }

  grid_size = 50
  grid = []
  for i in range(grid_size):
    grid.append([])
    for j in range(grid_size):
      grid[i].append(' ')

  xs = list(map(lambda s: s[0], solution))
  ys = list(map(lambda s: s[1], solution))
  min_x, max_x = min(xs), max(xs)
  min_y, max_y = min(ys), max(ys)

  updated_solution = []
  for i, p in enumerate(solution):
    perc_x = (p[0] - min_x) / (max_x - min_x)
    perc_y = (p[1] - min_y) / (max_y - min_y)

    x = math.floor((len(grid) - 1) * perc_x)
    y = math.floor((len(grid) - 1) * perc_y)
    updated_solution.append((x, y))
    grid[y][x] = str(i)

  for node1 in edges.keys():
    for node2 in edges[node1]:
      draw_line(grid, updated_solution[mapping[node1]], updated_solution[mapping[node2]])

  prnt(grid)




# TODO
# Clean up
# Incorporate into Graph
# Figure out mapping between node and index
# Add angles of edges in fitness
# Do lines intersect after adjusting size of grid?
# Line equation for infinite slope?
# Use other repo for evolutionsystem
if __name__ == '__main__':
  graph = Graph()
  graph.add_node('Jeju')
  graph.add_node('Busan')
  graph.add_node('SeoulMetro')
  graph.add_node('Pohang')
  graph.add_node('Seoul')
  graph.add_node('Cheongju')
  graph.add_node('Sacheon')
  graph.add_node('Daegu')

  graph.add_edge('Jeju', 'Cheongju', undirected=True)
  graph.add_edge('Jeju', 'Busan', undirected=True)
  graph.add_edge('Jeju', 'Daegu', undirected=True)
  graph.add_edge('Jeju', 'Sacheon', undirected=True)
  graph.add_edge('Busan', 'SeoulMetro', undirected=True)
  graph.add_edge('Busan', 'Seoul', undirected=True)
  graph.add_edge('Pohang', 'Seoul', undirected=True)
  graph.add_edge('Sacheon', 'Seoul', undirected=True)
  graph.add_edge('Seoul', 'Daegu', undirected=True)
  graph.add_edge('SeoulMetro', 'Daegu', undirected=True)

  def fitness_fn(solution):
    # Don't allow overlapping nodes
    for i, s1 in enumerate(solution):
      for j, s2 in enumerate(solution):
        if i != j and s1[0] == s2[0] and s1[1] == s2[1]:
          return 0

    # Incorporate minimum angle between edges
    number_of_intersecting_edges = get_intersecting_edges(solution, graph._edges)
    dist, min_dist = get_average_distance_between_nodes(solution)
    return (dist * min_dist) / (number_of_intersecting_edges + 1)

  number_of_individuals = 250
  number_of_genes = len(graph._edges.keys())
  number_of_generations = 25
  p_mutation = .25
  mutation_dev = 3

  ea = EvolutionSystem(fitness_fn, number_of_individuals, number_of_genes, p_mutation, mutation_dev)
  ea.evolve(number_of_generations)
  ind = ea.get_best_evolved_individuals()

  draw(ind[0].get_genes(), graph._edges)