from copyreg import pickle
import logging
import sys
import time
import pygame
import menaceUI
import menace_setUp as mns
import pickle
from tqdm import tqdm
  

class PlayMenace:
    def __init__(self, states, filepath, sys_arg):
        self.states = states
        self.filepath = filepath
        self.sys_arg = sys_arg
        self.change_in_number_beads = 0
        self.winning_states = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

        if len(self.sys_arg) == 3:
            self.game_mode = self.sys_arg[1]
            self.num_iterations = int(self.sys_arg[2])
            
        elif len(self.sys_arg) == 2:
            self.game_mode = self.sys_arg[1]
            self.num_iterations = 1000
        else:
            self.game_mode = "playervsMenace"
        

    def print_game_state(self, curr_game_st):
        print(curr_game_st)


    def check_state_exist(self, states, current_game_state):
        if ''.join(current_game_state) in states:
            return states
        states[''.join(current_game_state)] = mns.MenaceSetup(current_game_state)
        return states

    def reward_beads(self, state, menace_state, menace_step, reward ):
        # self.change_in_number_beads+=reward
        for indx, i in enumerate(menace_state):
            state[''.join(list(i))].set_num_beads(menace_step[indx], reward)

    def check_winning_cases(self, state, val):
        if(state[val[0]] == state[val[1]] and state[val[0]] == state[val[2]] and state[val[0]] != '0'):
            return True

    def winning_status(self, state):
        status = False
        for i in self.winning_states:
            if self.check_winning_cases(state, i):
                status = True
        return status

    def draw_status(self, states):
        if states.count('0') == 0:
            return True
        return False


    def play_menace(self, states, path):
        logging.debug("Entered the function :  play_menace()")
        try:
            logging.debug("Loading training file")
            pickle_read = open(path, "rb")
            states = pickle.load(pickle_read)
            logging.debug("Training file loaded")
            print("We have a traied menace")
        except FileNotFoundError:
            logging.debug("Training file not found.")
            print("Menace has not been trained yet")
            pass
        quit_game = False
        while(not quit_game):
            logging.debug("Game on between human and Menace")
            current_game_state = list('000000000')
            self.print_game_state(current_game_state)
            steps_menace = []
            menace_game_state = []
            pygame.init()
            menaceUI.board_grid = [ [ None ]*3, \
                                    [ None ]*3, \
                                    [ None]*3 ]
            menaceUI.winner_status = None
            menace_display = pygame.display.set_mode((400,400))
            pygame.display.set_caption("MENACE")
            menace_board = menaceUI.init_board(menace_display)
            new_game = False
            while(not new_game):
                try:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit_game = True
                            new_game = True
                            break
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            menace_board, row_val, col_val = menaceUI.click_board(menace_board)
                            menaceUI.winning_games(menace_board)
                            menaceUI.show_board(menace_display, menace_board)
                            if row_val is None:
                                continue
                            a = row_val*3 + col_val
                            if current_game_state[a] == '0':
                                current_game_state[a] = '1'
                                states = self.check_state_exist(states, current_game_state)
                            else:
                                # messagebox.showerror("Please select the empty space")
                                print("Please select the empty space")
                                continue
                            if self.winning_status(current_game_state):
                                self.reward_beads(states, menace_game_state, steps_menace, -1 )
                                # self.print_game_state(current_game_state)
                                logging.debug("Human Won")

                                time.sleep(1)
                                new_game = True
                                break
                            if self.draw_status(current_game_state):
                                self.reward_beads(states, menace_game_state, steps_menace, 1)
                                # self.print_game_state(current_game_state)
                                logging.debug("Game draw")
                                time.sleep(1)
                                new_game = True
                                break

                            menace_game_state.append(tuple(current_game_state))
                            current_num_beads = states[''.join(current_game_state)].get_num_beads()
                            steps_menace.append(current_num_beads)
                            row_bead = int(current_num_beads/3)
                            column_bead = current_num_beads % 3
                            menaceUI.place_move(menace_board, row_bead, column_bead, "O")
                            menaceUI.winning_games(menace_board)
                            menaceUI.show_board(menace_display, menace_board)
                            if current_game_state[current_num_beads] == '0':
                                current_game_state[current_num_beads] = '2'
                                states = self.check_state_exist(states, current_game_state)
                            else:
                                print("Please select the empty space")
                                break
                            if self.winning_status(current_game_state):
                                self.reward_beads(states, menace_game_state, steps_menace, 3)
                                # self.print_game_state(current_game_state)
                                logging.debug("Menace won")
                                time.sleep(1)
                                new_game = True
                                break
                            if self.draw_status(current_game_state):
                                self.reward_beads(states, menace_game_state, steps_menace, 1)
                                self.print_game_state(current_game_state)
                                logging.debug("Game Draw")
                                time.sleep(1)
                                break
                            self.print_game_state(current_game_state)
                            menaceUI.show_board(menace_display, menace_board)
                        menaceUI.show_board(menace_display, menace_board)
                                                    
                except ValueError as e:
                    logging.debug("Exception occured : ValueError - selected occupied box")
                    # messagebox.showerror("Please select the empty box")
                    print("Please select the empty space")
                    continue           
    
            


    def train_menace(self, states, path, num_iterations):
        logging.debug("Training started : Menace1 vs Menace2")
        self.menace_1_wins = 0
        self.menace_2_wins = 0
        self.menace_draws = 0
        
        for i in tqdm(range(num_iterations)):
            current_game_state = list('000000000')
            # self.print_game_state(current_game_state)   
            menace1_steps = []
            menace1_game_state = []
            menace2_steps = []
            menace2_game_state = []
            pygame.init()
            menaceUI.board_grid = [ [ None ]*3, \
                                    [ None ]*3, \
                                    [ None]*3 ]
            menaceUI.winner_status = None
            menace_display = pygame.display.set_mode((500,500))
            pygame.display.set_caption("MENACE")
            menace_board = menaceUI.init_board(menace_display)
            while(True):
                try:
                    menaceUI.winning_games(menace_board)
                    menaceUI.show_board(menace_display, menace_board, "menacetrain", str(self.menace_1_wins), str(self.menace_2_wins), str(self.menace_draws))
                    menace1_game_state.append(tuple(current_game_state))
                    current_num_beads = states[''.join(current_game_state)].get_num_beads()
                    # print(current_num_beads)
                    menace1_steps.append(current_num_beads)
                    row_bead = int(current_num_beads/3)
                    column_bead = current_num_beads % 3
                    menaceUI.place_move(menace_board, row_bead, column_bead, "X")
                    menaceUI.winning_games(menace_board)
                    current_game_state[current_num_beads] = '1'
                    states = self.check_state_exist(states, current_game_state)

                    if self.winning_status(current_game_state):
                        self.reward_beads(states, menace1_game_state, menace1_steps, 3)
                        self.reward_beads(states, menace2_game_state, menace2_steps, -1)
                        self.menace_1_wins+=1
                        # time.sleep(0.3)
                        break

                    if self.draw_status(current_game_state):
                        self.reward_beads(states, menace1_game_state, menace1_steps, 1)
                        self.reward_beads(states, menace2_game_state, menace2_steps, 1)
                        self.menace_draws+=1
                        # time.sleep(0.3)
                        break
                    
                    menace2_game_state.append(tuple(current_game_state))
                    current_num_beads = states[''.join(current_game_state)].get_num_beads()
                    menace2_steps.append(current_num_beads)
                    row_bead = int(current_num_beads/3)
                    column_bead = current_num_beads % 3
                    menaceUI.place_move(menace_board, row_bead, column_bead, "O")
                    menaceUI.winning_games(menace_board)
                    current_game_state[current_num_beads] = '2'
                    states = self.check_state_exist(states, current_game_state)

                    if self.winning_status(current_game_state):
                        self.reward_beads(states, menace1_game_state, menace1_steps, -1)
                        self.reward_beads(states, menace2_game_state, menace2_steps, 3)
                        self.menace_2_wins+=1
                        # time.sleep(0.3)
                        break

                    if self.draw_status(current_game_state):
                        self.reward_beads(states, menace1_game_state, menace1_steps, 1)
                        self.reward_beads(states, menace2_game_state, menace2_steps, 1)
                        self.menace_draws+=1
                        # time.sleep(0.3)
                        break
                
                except ValueError:
                    logging.debug("Exception occured : ValueError - selected occupied box")
                    print("Please select the empty space")
                    continue
            

        logging.debug("Menace is trained")
        write_pickle = open(path, "wb")
        pickle.dump(states, write_pickle)
        write_pickle.close()

    def start_game(self):
        if self.game_mode == 'playervsMenace':
            logging.debug("Game started : Menace vs Human")
            self.play_menace(self.states, self.filepath)
        else:
            logging.debug("Starting Training : Menace vs Menace")
            self.train_menace(self.states, self.filepath, self.num_iterations )


    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Welcome to menace")
    argv = sys.argv
    board_state = {'000000000' : mns.MenaceSetup('000000000')}
    print(board_state)
    logging.debug("Board states has been set up")
    pickel_path = 'traning_data.pickle'
    playmenace = PlayMenace(board_state, pickel_path,argv)
    playmenace.start_game()


