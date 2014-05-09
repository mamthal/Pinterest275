class Board:
    def __init__(self, board_name):
        self.board_name = board_name
def retrieve_all_boards():
    boardlist = []
    boardlist = getboardsdb()
    return boardlist                                                                                                                                                              
def retrieve_board(board_id):
    pinlist = []
    pinlist = getpinsdb(board_id)
    return pinlist
    
    
