import unittest
from menace import PlayMenace
import menaceUI
import pygame
import menace_setUp as mns

class MenaceTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.states = {'000000000' : mns.MenaceSetup('000000000')}
        self.pickel_path = 'traning_data.pickle'
        self.menace_display = pygame.display.set_mode((300,325))
        self.menace_board = menaceUI.init_board(self.menace_display)
        self.menace_board, self.row_val, self.col_val = menaceUI.click_board(self.menace_board)
        self.a = self.row_val*3 + self.col_val
        self.current_game_state = list('000000000')
        self.current_game_state[self.a] = '1'
        self.sys_arg = ["", 3]
        self.menace_display = pygame.display.set_mode((300,325))
        #self.argv = 3

    def test_check_state_exist(self):
        self.play_menace = PlayMenace(self.states, self.pickel_path, self.sys_arg)
        self.assertEqual(type(self.play_menace.check_state_exist(self.states, self.current_game_state)), dict)

    def test_draw_status(self):
        self.play_menace = PlayMenace(self.states, self.pickel_path, self.sys_arg)
       # print(type(self.play_menace.winning_status(self.states)))
        self.assertEqual(type(self.play_menace.draw_status(self.current_game_state)), bool)

    def test_play_menace(self):
        self.play_menace = PlayMenace(self.states, self.pickel_path, self.sys_arg)
        self.assertEqual(type(self.play_menace.play_menace(self.states, self.pickel_path)),bool)

    def test_init_board(self):
       # self.play_menace = PlayMenace(self.states, self.pickel_path, self.sys_arg)
        self.assertEqual(type(menaceUI.init_board(self.menace_display)), pygame.Surface)

    def test_start_game(self):
        self.play_menace = PlayMenace(self.states, self.pickel_path, self.sys_arg)
        self.assertEqual(type(self.play_menace.start_game()),type(None))

if __name__ == '__main__':
    unittest.main()