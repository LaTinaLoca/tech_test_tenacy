from unittest import TestCase
from play_score import PlayScore
import itertools
from config import *


class TestPlayScore(TestCase):
    def setUp(self) -> None:
        self.play_score = PlayScore()
        self.combinations = list(itertools.combinations([measure for measure 
                                                    in self.play_score.measures_list if measure.get("identifier") in 
                                                        ["MEAS-28", "MEAS-25", "MEAS-32", "MEAS-19"]], 
                                                    COMBINATION_LENGTH)
                            )
    def test_get_combination_score(self):
        combination_score_dict, error_msg = self.play_score.get_combinations_score(self.combinations)
        self.assertEqual(error_msg, "")
        self.assertEqual(combination_score_dict["MEAS-25/MEAS-28/MEAS-32"].get("score"), 95.7)
        self.assertEqual(combination_score_dict["MEAS-25/MEAS-28/MEAS-32"].get("cost"), 107)
    

    def test_get_best_combination_ids_no_combs(self):
        self.play_score.measures_list = []
        ids_list, error_msg = self.play_score.get_best_combination_ids()
        self.assertFalse(error_msg == "")
        self.assertEqual(ids_list, [])
    
    
    def test_get_best_combination_ids(self):
        ids_list, error_msg = self.play_score.get_best_combination_ids()
        self.assertEqual(error_msg, "")
        self.assertEqual(sorted(ids_list), ['MEAS-19', 'MEAS-25', 'MEAS-28'])