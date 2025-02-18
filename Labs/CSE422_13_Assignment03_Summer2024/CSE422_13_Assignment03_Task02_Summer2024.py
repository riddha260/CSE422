class GameTree:
    def __init__(self):
        self.nodes = {}
        self.root_node = None

    def add_node(self, node_id, parent_id=None, value=None):
        if not self.nodes:
            self.root_node = node_id
            self.nodes[node_id] = [parent_id, value, None, None]
        elif parent_id in self.nodes:
            if self.nodes[parent_id][2] is None:
                self.nodes[parent_id][2] = node_id
            else:
                self.nodes[parent_id][3] = node_id
            self.nodes[node_id] = [parent_id, value, None, None]

    def get_value(self, node_id):
        return self.nodes[node_id][1] if node_id in self.nodes else None

    def get_children(self, node_id):
        return [child for child in self.nodes[node_id][2:] if child is not None]

    def display_tree(self):
        return self.nodes


def ab_pruning(tree, current_node, alpha, beta, depth_level, is_maximizing_player):
    if depth_level == 0:
        return tree.get_value(current_node)

    if is_maximizing_player:
        max_eval = float('-inf')
        for child_node in tree.get_children(current_node):
            max_eval = max(max_eval, ab_pruning(tree, child_node, alpha, beta, depth_level - 1, False))
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child_node in tree.get_children(current_node):
            min_eval = min(min_eval, ab_pruning(tree, child_node, alpha, beta, depth_level - 1, True))
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval


def pacman_simulation(magic_cost):
    # Create the tree structure
    game_tree = GameTree()

    # Level 0 (Root)
    game_tree.add_node("Root", None)  # Pacman plays (Maximizing Player)

    # Level 1
    game_tree.add_node("Node1", "Root")  # Ghost's Move (Minimizing Player)
    game_tree.add_node("Node2", "Root")  # Ghost's Move (Minimizing Player)

    # Level 2
    game_tree.add_node("Node3", "Node1")  # Pacman's Move (Maximizing Player)
    game_tree.add_node("Node4", "Node1")  # Pacman's Move (Maximizing Player)
    game_tree.add_node("Node5", "Node2")  # Pacman's Move (Maximizing Player)
    game_tree.add_node("Node6", "Node2")  # Pacman's Move (Maximizing Player)

    # Level 3 (Leaf Nodes with outcomes)
    game_tree.add_node("Leaf1", "Node3", 3)
    game_tree.add_node("Leaf2", "Node3", 6)
    game_tree.add_node("Leaf3", "Node4", 2)
    game_tree.add_node("Leaf4", "Node4", 3)
    game_tree.add_node("Leaf5", "Node5", 7)
    game_tree.add_node("Leaf6", "Node5", 1)
    game_tree.add_node("Leaf7", "Node6", 2)
    game_tree.add_node("Leaf8", "Node6", 0)

    # Minimax value without dark magic using alpha-beta pruning
    minimax_without_magic = ab_pruning(game_tree, "Root", alpha=float('-inf'), beta=float('inf'), depth_level=3, is_maximizing_player=True)

    # Max values from both subtrees
    max_left_subtree = max(game_tree.get_value("Leaf1"), game_tree.get_value("Leaf2"), game_tree.get_value("Leaf3"), game_tree.get_value("Leaf4"))
    max_right_subtree = max(game_tree.get_value("Leaf5"), game_tree.get_value("Leaf6"), game_tree.get_value("Leaf7"), game_tree.get_value("Leaf8"))

    # Pacman's potential score with dark magic applied
    score_left_magic = max_left_subtree - magic_cost
    score_right_magic = max_right_subtree - magic_cost

    # Determine which move is better with magic
    if score_left_magic > score_right_magic:
        best_magic_score = score_left_magic
        direction_choice = "left"
    else:
        best_magic_score = score_right_magic
        direction_choice = "right"

    # Compare minimax without magic and the best outcome with magic
    if minimax_without_magic < best_magic_score:
        print(f"The new minimax value is {best_magic_score}. Pacman goes {direction_choice} and uses dark magic")
    else:
        print(f"The minimax value is {minimax_without_magic}. Pacman does not use dark magic")


#if __name__ == "__main__":
#    # User input for the cost of using dark magic
#    magic_cost_input = int(input("Enter the cost of dark magic: "))
#    pacman_simulation(magic_cost_input)

def start_game():
    try:
        # Take user input for the cost of dark magic
        magic_cost = int(input("Please provide the cost of using dark magic (integer): "))
        # Call the Pacman simulation function with the input value
        pacman_simulation(magic_cost)
    except ValueError:
        # Handle invalid input
        print("Invalid input! Please enter an integer value for the magic cost.")

# Starting point of the game
def main():
    print("Welcome to the Pacman decision game!")
    start_game()

# Run the game
main()
