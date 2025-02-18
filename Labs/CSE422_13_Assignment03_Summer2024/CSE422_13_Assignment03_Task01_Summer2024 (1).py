class TREE:
    def __init__(self):
        self.tree = {}
        self.root = None

    def addNode(self, node, parent, value=None):
        if not self.tree:
            self.root = node
            self.tree[node] = [parent, value, None, None]
        elif parent in self.tree:
            if self.tree[parent][2] is None:
                self.tree[parent][2] = node
            else:
                self.tree[parent][3] = node
            self.tree[node] = [parent, value, None, None]

    def getValue(self, node):
        return self.tree[node][1] if node in self.tree else None

    def getChildren(self, node):
        return [child for child in self.tree[node][2:] if child is not None]

    def getTree(self):
        return self.tree


def alpha_beta_pruning(tree, node, alpha, beta, depth, maximizePlayer):
    if depth == 0:
        return tree.getValue(node)
    
    if maximizePlayer:
        value = float('-inf')
        for child in tree.getChildren(node):
            value = max(value, alpha_beta_pruning(tree, child, alpha, beta, depth - 1, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in tree.getChildren(node):
            value = min(value, alpha_beta_pruning(tree, child, alpha, beta, depth - 1, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def create_game_tree():
    tree = TREE()

    # Level 0 (Root)
    tree.addNode("A", None)  # Root node

    # Level 1
    tree.addNode("B", "A")
    tree.addNode("C", "A")

    # Level 2
    tree.addNode("D", "B")
    tree.addNode("E", "B")
    tree.addNode("F", "C")
    tree.addNode("G", "C")

    # Level 3 (Leaf nodes with utility values)
    tree.addNode("H", "D", -1)  # Scorpion wins
    tree.addNode("I", "D", 1)   # Sub-Zero wins
    tree.addNode("J", "E", -1)  # Scorpion wins
    tree.addNode("K", "E", 1)   # Sub-Zero wins
    tree.addNode("L", "F", -1)  # Scorpion wins
    tree.addNode("M", "F", 1)   # Sub-Zero wins
    tree.addNode("N", "G", -1)  # Scorpion wins
    tree.addNode("O", "G", 1)   # Sub-Zero wins

    return tree


def main():
    starter = int(input("Enter 0 for Scorpion or 1 for Sub-Zero to start: "))
    rounds = 3  # Fixed number of rounds (max depth = 3)
    players = ["Scorpion", "Sub-Zero"]

    # Create the game tree
    tree = create_game_tree()

    # Determine the game winner using alpha-beta pruning
    result = alpha_beta_pruning(tree, "A", alpha=float('-inf'), beta=float('inf'), depth=3, maximizePlayer=(starter == 1))

    # Determine the game winner based on result
    game_winner = "Sub-Zero" if result == 1 else "Scorpion"

    # Simulate the rounds
    round_winners = []
    current_player = starter

    for i in range(1, rounds + 1):
        # Use alpha-beta pruning to determine winner of the round
        round_result = alpha_beta_pruning(tree, "A", alpha=float('-inf'), beta=float('inf'), depth=3, maximizePlayer=(current_player == 1))
        if round_result == 1:
            round_winners.append("Sub-Zero")
        else:
            round_winners.append("Scorpion")

        # Alternate the starting player for the next round
        current_player = 1 - current_player

    # Output the results
    print(f"Game Winner: {game_winner}")
    print(f"Total Rounds Played: {rounds}")
    for i, winner in enumerate(round_winners, start=1):
        print(f"Winner of Round {i}: {winner}")


if __name__ == "__main__":
    main()
