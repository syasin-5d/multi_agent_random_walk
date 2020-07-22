import argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', type=str, required=True)
    parser.add_argument('-n', type=int)
    parser.add_argument('-a', '--request', type=int, required=True)
    parser.add_argument('-b', '--target', type=int, required=True)
    parser.add_argument('--nagents', type=int, required=True)
    parser.add_argument('-T', '--tries', type=int, required=True)
    args = parser.parse_args()
    return args


class Agent():
    def __init__(self, start, end):
        self.start = start
        self.now = start
        self.end = end

    def init(self):
        self.now = self.start

    def walk(self, network):
        # move neighbor node from now randomly
        self.now = np.random.choice(list(network.get_neighbors(self.now)))

    def is_goal(self):
        return self.now == self.end


class Network():
    def __init__(self, path, n_agents, request_node, target_node):
        self.time = 0
        self.is_goal = False
        self.neighbor = self.read_network_graph(path)
        self.n_agents = n_agents
        self.request_node = request_node
        self.target_node = target_node
        self.agents = [
            Agent(request_node, target_node) for _ in range(n_agents)
        ]

    def init(self):
        self.time = 0
        self.is_goal = False
        for agent in self.agents:
            agent.init()

    def read_network_graph(self, path):
        neighbor = {}
        with open(path, 'r') as f:
            for line in f:
                i, j, w = map(int, line.split())
                if i not in neighbor:
                    neighbor[i] = {}
                if j not in neighbor:
                    neighbor[j] = {}
                neighbor[i][j] = w
                neighbor[j][i] = w
        return neighbor

    def get_neighbors(self, node):
        return set(self.neighbor[node].keys())

    def advance(self):
        self.time += 1
        for agent in self.agents:
            agent.walk(self)
            if agent.is_goal():
                self.is_goal = True


def main():
    args = parse_args()
    path = args.file_name
    n_agents = args.nagents
    request_node = args.request
    target_node = args.target
    n_tries = args.tries
    network = Network(path, n_agents, request_node, target_node)

    search_times = []
    for t in range(n_tries):
        network.init()
        while not network.is_goal:
            network.advance()
        search_times.append(network.time)
    mu_hat = np.average(search_times)
    print(f"average_search_time: {mu_hat}[hops]")
    print(f"node {target_node}'s weighted_degree:",
          len(network.get_neighbors(target_node)))


if __name__ == "__main__":
    main()
"""
# class 使わず実装するなら以下？
poses = [start for _ in range(N_agents)]
goal = False
time = 0
while not goal:
    time += 1
    for p in poses:
        p = np.choice(p.get_neighbors())
        if p == goal:
            goal = True
"""
