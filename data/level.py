## @file levels.py
#  Source file for levels
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/21/18


## @class Levels
#  @brief TBD
class Level:

    ## Constructor
    def __init__(self):
        self.win = False

    ## Abstract method; Updates constants for level
    def set_constants(self):
        pass
