from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)


''' ==================== Work Below ==================== '''
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# traversal_path = ["n", "n", "s", "s", "w", "w",
#                   "e", "e", "e", "e", "w", "w", "s", "s"]
# print("player's current room:", player.current_room, "------------------")
# print(player.current_room.get_room_in_direction("n"))

# moves = ["n", "s", "e", "w"]


# def get_next_rooms():
#     available_rooms = []
#     current = player.current_room
#     for move in moves:
#         if current.get_room_in_direction(move):
#             available_rooms.append(move)
#     return available_rooms

# def find_shortest_path(start):
#     stack = Stack()
#     stack.push([start])
#     visited = []
#     while stack.size() > 0:
#         path = stack.pop()
#         # current = path[-1]
#         print(path)
#         visited.append(path)
#         traversal_path.append(path)
#         # if stack.size() > 1:
#         player.travel(path)
#         # print("current:", current)
#         for room in get_next_rooms():
#             if room not in visited:
#                 stack.push(room)
#                 visited.append(room)


#         print("Stack:", stack.size())
#     print("Visited:", len(visited), visited)


room_map = {}


def find_shortest_path(player, moves):
    # initialize queue with the player in the first room
    queue = Queue()
    queue.enqueue([player.current_room.id])
    visited = set()
    while queue.size() > 0:
        # start the path by dequeing the room
        path = queue.dequeue()
        current = path[-1]
        # the room was now visited
        if current not in visited:
            visited.add(current)
            # for room in next available rooms from current location:
            for room in room_map[current]:
                # if the room has not yet been traveled to
                if room_map[current][room] == "?":
                    return path
                else:
                    new_path = list(path)
                    new_path.append(room_map[current][room])
                    queue.enqueue(new_path)
    return []


more_moves = Queue()


def find_more_rooms(player, more_moves):
    # grab the current room from the room map
    curr_room = room_map[player.current_room.id]
    # track new rooms
    new_rooms = []
    for room in curr_room:
        # if there is an unvisited room as one of the exit paths add it
        if curr_room[room] == "?":
            new_rooms.append(room)
    # if there are no new rooms
    if len(new_rooms) == 0:
        # run the path finding function
        traverse_path = find_shortest_path(player, more_moves)
        # track a the new current room for the player
        new_curr_room = player.current_room.id
        # for each room in the path finding function
        for room in traverse_path:
            # and for each path available to the current room
            for path in room_map[new_curr_room]:
                if room_map[new_curr_room][path] == room:
                    more_moves.enqueue(path)
                    new_curr_room = room
                    break
    else:
        # add a new room to the more moves queue
        more_moves.enqueue(new_rooms[random.randint(0, len(new_rooms) - 1)])


unexplored_room = {}

# use room function get exits to check if there are unexplored rooms available
for room in player.current_room.get_exits():
    unexplored_room[room] = "?"
# set the new world starting room to the unexplored rooms
room_map[world.starting_room.id] = unexplored_room

find_more_rooms(player, more_moves)

reverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

# while there are still more moves to be made
while more_moves.size() > 0:
    # track current room
    current = player.current_room.id
    # move the player using the moves available
    move = more_moves.dequeue()
    player.travel(move)
    # add the player movements to the traversal path
    traversal_path.append(move)
    # track the player's new room after moving
    next_room = player.current_room.id
    room_map[current][move] = next_room
    if next_room not in room_map:
        room_map[next_room] = {}
        # check if any available rooms after the move are unvisited
        for room in player.current_room.get_exits():
            room_map[next_room][room] = "?"
    # set the connection to the room we just came from as the reverse of the move to get to this current room and NOT "?" so we know it has been visited
    room_map[next_room][reverse_directions[move]] = current
    # if there are no more moves right now, look for more
    if more_moves.size() == 0:
        find_more_rooms(player, more_moves)


# print("-------TESTING-------\n", get_next_rooms(), "\n-------TESTING-------")
# print("-------TESTING-------\n",
#       find_shortest_path(player, moves), "\n-------TESTING-------")
# print("-------TESTING-------\n", "Traversal Path:",
#       traversal_path, "\n-------TESTING-------")


# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a '?' for an exit. If you use the bfs code from the homework, you will need to make a few modifications.
# Instead of searching for a target vertex, you are searching for an exit with a '?' as the value. If an exit has been explored, you can put it in your BFS queue like normal.
'''
? for an available direction == NOT visited the room in that direction
'''

# BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.


# ** NOTES **
# ** using only dft that explores the whole thing and tracks paths will be enough to reach mvp **
# ** IDEAS **
# dft until hitting dead end
# if hit dead end, use bft until we find an unvisited node then go back to dft
# if while using dft we find a node we have already visited, use bft
# once, we find another non-visited node, go back to dft


''' ==================== Work ABOVE ==================== '''

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
