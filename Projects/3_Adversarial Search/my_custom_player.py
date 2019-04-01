
from sample_players import DataPlayer
from isolation.isolation import _WIDTH, _HEIGHT
import random
from isolation import isolation

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
            print('empty board')
            print(random.choice(state.actions()))
            print('!-------------------------!')
            self.queue.put(random.choice(state.actions()))
        else:
            depth_limit = 5
            for depth in range(1, depth_limit + 1):
                best_move = self.alpha_beta_pruning(state, depth)
                print(depth)
                print(best_move)
            print(depth)
            print('---------------------------------------------')
            self.queue.put(best_move)  
            print(state)         
    def alpha_beta_pruning(self,state,depth):
        def max_value(state,alpha,beta,depth):
            if state.terminal_test():
                print("max value")
                print(state)
                return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            v = float("-inf")
            for a in state.actions():
                v = max(v, min_value(state.result(a),alpha,beta,depth-1))
            if v >=beta: return v
            alpha = max(alpha,v)
            return v        
        def min_value(state,alpha,beta,depth):
            if state.terminal_test():
                print("min value")
                print(state)
                return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            v = float("-inf")
            for a in state.actions():
                v = min(v, max_value(state.result(a),alpha,beta,depth-1))
            if v <= alpha:return v
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
    
    def distance(self,state):
        own_loc = state.locs[state.ply_count % 2]
        x_player, y_player = own_loc // (_WIDTH + 2), own_loc % (_WIDTH + 2)
        return min(x_player, _WIDTH + 1 - x_player, y_player, _HEIGHT - 1 - y_player)
    
    def score(self,state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        dis = self.distance(state)
        if dis >= 2:
            return 2*len(own_liberties) - len(opp_liberties)
        else:
            return len(own_liberties) - len(opp_liberties)
    