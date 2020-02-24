def Rejuvenate(players, workforce):
    [board.reset() for board in players.boardlist]
    actions_for_upkeep = workforce.calculate_labor_for_upkeep()
    actions_for_other = workforce.calculate_labor_for_actions()
    return(actions_for_other, actions_for_upkeep)

