import random
import time

from main import Go, print_state, determine_previous_player, determine_next_player, Player


def main():
    def new_game():
        print('New game:')
        print('')
        state = Go.create_new_game()
        print_state(state)
        return state

    state = new_game()

    while True:
        action = choose_action(state)
        state = state.step(action)
        done = state.is_done()
        print_state(state)

        if done:
            winner = state.determine_result()
            print('Player ' + str(winner.value) + ' won.')
            print('')
            return


def choose_action(state):
    action = mcts(state, duration=10)
    return action


NUMBER_OF_PLAYERS = len(Player)


def mcts(state, duration):
    start_time = time.time()
    current_node = Node(determine_previous_player(state.current_player), None, state)
    while time.time() - start_time < duration:
        node = current_node
        while not is_terminal_node(node):
            available_actions = node.state.determine_available_actions()
            if len(available_actions) >= 1:
                parent = node
                player = determine_next_player(parent.player)
                action = random.choice(available_actions)
                state = parent.state.step(action)
                try:
                    node = next(node for node in parent.children if node.action == action)
                except StopIteration:
                    node = Node(player, action, state, parent)
                    parent.children.add(node)
            else:
                raise Exception('0 available states')
        winner = node.state.determine_result()
        if winner:
            reward = [
                node.state.determine_reward(player)
                for player
                in Player
            ]
            while node:
                for index in range(NUMBER_OF_PLAYERS):
                    node.reward[index] += reward[index]
                node.playouts += 1
                node = node.parent

    player = determine_next_player(current_node.player)
    if current_node.playouts >= 1:
        node = max(
            current_node.children,
            key=lambda node: node.reward[player - 1] / float(node.playouts) if node.playouts >= 1 else 0)
        action = node.action
    else:
        action = choose_random_action(current_node.state)

    return action


def choose_random_action(state):
    available_actions = state.determine_available_actions()
    if len(available_actions) >= 1:
        action = random.choice(available_actions)
    else:
        raise Exception('All columns seem to be full.')
    return action


def is_terminal_node(node):
    return node.state.is_done()


class Node:
    def __init__(self, player, action, state, parent=None):
        self.player = player
        self.action = action
        self.state = state
        self.reward = [0, 0]
        self.playouts = 0
        self.parent = parent
        self.children = set()


if __name__ == '__main__':
    main()
