from __future__ import absolute_import, division, print_function


import numpy as np
import pickle
import time

class CountdownPuzzleConfig(object):

    __alphabet__ = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                    "Y", "Z"]

    __codes__ = [203, 529, 394, 481, 839, 576, 416, 729, 495, 582, 227, 605, 
                 656, 535, 811, 878, 204, 822, 316, 763, 117, 884, 777, 766, 
                 601, 787]

    def __init__(self):
        self.alphabet = self.__alphabet__
        self.codes = self.__codes__

    def code_is_correct(self, letter, code):
        return self.alphabet.index(letter) == self.codes.index(code)


