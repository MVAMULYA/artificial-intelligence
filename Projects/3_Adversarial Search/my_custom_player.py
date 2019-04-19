
from sample_players import DataPlayer
import random
from isolation import isolation
import random, math, copy
CNST = 1.0


class CustomPlayer(DataPlayer):
    
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        import random      
        
        if state.ply_count < 2:
            if state in self.data:
                best_move = self.data[state]
                self.queue.put(best_move)
            else:
                best_move = random.choice(state.actions())
                self.queue.put(best_move)             
        else:
            depth_limit = 75
            for depth in range(0, depth_limit):
                best_move = self.alpha_beta_pruning(state, depth)
                self.queue.put(best_move) 
        self.context = best_move
    
      
    def my_moves(self,state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return 2*len(own_liberties) - len(opp_liberties)
   
    def alpha_beta_pruning(self,state,depth):
        def max_value(state,alpha,beta,depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.my_moves(state)
            v = float("-inf")
            for a in state.actions():
                v = max(v, min_value(state.result(a),alpha,beta,depth-1))
            if v >= beta:
                return v
            alpha = max(alpha,v)
            return v        
        def min_value(state,alpha,beta,depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.my_moves(state)
            v = float("inf")
            for a in state.actions():
                v = min(v, max_value(state.result(a),alpha,beta,depth-1))
            if v <= alpha:
                return v
            beta = min(beta,v)
            return v
        
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in state.actions():
            v = min_value(state.result(a),alpha,beta,depth-1)
            if v > best_score:
                best_score = v
                best_move = a
        
        return best_move
        
        
        
class CustomPlayer_MCTS(DataPlayer):
    
    def get_action(self, state):
        if state.ply_count < 2:
            best_move = random.choice(state.actions())
            self.queue.put(best_move)             
        else:
            computational_limit = 75
            best_move = self.mct_search(state,computational_limit)
            self.queue.put(best_move) 
        self.context = best_move
    
    def mct_search(self,state,computational_limit):
        root = Node(state)
        if root.state.terminal_test():
            return random.choice(state.actions())
        for i in range(computational_limit):
            child = tree_policy(root)
            if not child:
                continue
            reward = default_policy(child.state)
            backup(child,reward)
        best_child_index = root.children.index(best_child(root))
        return root.child_actions[best_child_index]

class Node():
    def __init__(self, state,parent=None):
        self.visits = 1
        self.action = 1
        self.reward = 0.0
        self.state = state
        self.parent = parent
        self.children = []
        self.child_actions = []
        
    def update(self,reward):
        self.reward += reward
        self.visits += 1
            
    def add_child(self, child_state,action):
        child = Node(child_state, self)
        self.children.append(child)
        self.child_actions.append(action)
        
    def fully_expanded(self):
        return len(self.child_actions) == len(self.state.actions())
        
def expand(node):
    for s_action in node.state.actions():
        if s_action not in node.child_actions:
            e_state = node.state.result(s_action)
            node.add_child(e_state, s_action)
            return node.children[-1]
        
def best_child(node):
    best_score = float("-inf")
    best_children = []
    for child in node.children:
        UCT_score = (child.reward / child.visits) + CNST * (math.sqrt(2.0 * math.log(node.visits) / child.visits))
        if UCT_score == best_score:
            best_children.append(child)
        elif UCT_score > best_score:
            best_children = [child]
            best_score = UCT_score
    return random.choice(best_children)
    
def tree_policy(node):
    while not node.state.terminal_test():
        if not node.fully_expanded():
            return expand(node)
        else:
            node = best_child(node)
    return node


def default_policy(state):
    cur_state = copy.deepcopy(state)
    while not state.terminal_test():
        action = random.choice(state.actions())
        state = state.result(action)
    if state._has_liberties(cur_state.player()):
        return -1
    else:
        return 1

def backup(node, reward):
    while node != None:
        node.update(reward)
        node = node.parent
        reward *= -1
               
        
    
            
            
                    
                    
            
            
        
    


    
    

    
    