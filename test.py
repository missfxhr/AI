execfile("SudokuStarter.py")
#sb = init_board("input_puzzles/easy/4_4.sudoku")
#sb = init_board("input_puzzles/easy/9_9.sudoku")
sb = init_board("input_puzzles/easy/16_16.sudoku")
#sb = init_board("input_puzzles/easy/25_25.sudoku")
sb.print_board()

fb = solve(sb, False, False, True, False)

