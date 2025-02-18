import heapq

def read_heuristic(file_path):
    heuristic_values = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            node = parts[0]
            h_value = int(parts[1])
            heuristic_values[node] = h_value
    return heuristic_values

def read_graph(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            node = parts[0]
            neighbors = [(parts[i], int(parts[i+1])) for i in range(2, len(parts), 2)]
            graph[node] = neighbors
    return graph

def astar(graph, heuristic, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    came_from = {}
    cost_so_far = {node: float('inf') for node in graph}
    cost_so_far[start] = 0

    while priority_queue:
        current_priority, current_node = heapq.heappop(priority_queue)

        if current_node == goal:
            break

        for neighbor, cost in graph[current_node]:
            new_cost = cost_so_far[current_node] + cost
            if new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic[neighbor]
                heapq.heappush(priority_queue, (priority, neighbor))
                came_from[neighbor] = current_node

    return reconstruct_path(came_from, start, goal), cost_so_far[goal]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


input_file = 'input.txt'
output_file = open('output.txt', 'w')
heuristic = read_heuristic(input_file)
graph = read_graph(input_file)

start_node = input('Enter the start node: ')
goal_node = input('Enter the goal node: ')

if start_node not in heuristic or goal_node not in heuristic:
    output_file.write(f"Start or goal node not found in the heuristic data.")

path, total_cost = astar(graph, heuristic, start_node, goal_node)

if path:
    output_file.write(f"Path:  {' -> ' .join(path)}")
    output_file.write('\n')
    output_file.write(f"Total Distance: {total_cost} km")
else:
    output_file.write("No path found")


