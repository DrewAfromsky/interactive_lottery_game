import argparse
import multiprocessing as mp
import time
from typing import List


def read_input_file(file_path) -> List[str]:    
    """
    Read the input file and return a list of all players numbers
    :param file_path: path to the input file
    :return: list of all players numbers
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines


def update_winner_map(players: List[str], committee_lottery_numbers: List[str]) -> dict:
    """
    Update the map with the number of winners per category for each batch of players
    :param players: list of players numbers
    :param committee_lottery_numbers: list of committee lottery numbers
    :return: dictionary with the number of winners per category for the batch
    """
    # Each spawned process will have its own copy of the map
    process_winner_map = {matches: 0 for matches in range(2,6)}  # init with {2: 0, 3: 0, 4: 0, 5: 0}
    for player in players:  # O(n) where n is the number of players in the batch
        # O(1) space per player
        matches = 0  # number of matches between player and committee lottery numbers
        # O(N=5) for each player, since always have 5 numbers for each player
        for number in player.split():  # player has format 'int int int int int\n' from the players list
            if number in committee_lottery_numbers: # O(5) scan in committee_lottery_numbers
                matches += 1
        # Check happens once per player, so O(1) for each player
        if matches >= 2:  # require at least 2 matches to win
            process_winner_map[matches] += 1
    return process_winner_map


def get_winners(players: List[str], committee_lottery_numbers: List[str]) -> List[dict]:
    """
    Get the number of winners per category using batched parallel processing
    Assigns a batch of players to each process and returns a list of dictionaries
    where each dictioanry represents the number of winners per category for each batch
    :param players: list of players numbers
    :param committee_lottery_numbers: list of committee lottery numbers
    :return: list of dictionaries, each representing the number of winners per category for a batch
    """
    cpu_count = mp.cpu_count()  # Maximum number of processes we can run at a time
    
    if len(players) < cpu_count:
        raise ValueError("Number of players must be greater than the number of processes available to create batches")
    
    batch_size = round(len(players)/cpu_count)  # 10_000_000 / cpu_count for the machine

    batches = []
    for index in range(0, len(players), batch_size):
        batch = players[index:index+batch_size]
        batches.append(batch)

    with mp.Pool(processes=cpu_count) as p:
        winners_per_batch = p.starmap(update_winner_map, zip(batches, [committee_lottery_numbers]*len(batches)))
    return winners_per_batch


def report_winners_per_category(winners_per_batch: List[dict]):
    """
    Process the dictionary generated for each batch of players and 
    print the total number of winners per category in the format '2 3 4 5'
    """
    all_winners = {matches: 0 for matches in range(2,6)}
    for winners in winners_per_batch:
        for category, number_of_winners in winners.items():
            all_winners[category] += number_of_winners

    winners_per_match_category = [str(value) + " " for value in all_winners.values()]
    return ''.join(winners_per_match_category).rstrip()


def calculate_runtime(players: List[str], committee_lottery_numbers: List[str], file_path: str):
    """Calculates the execution runtime for the get_winners function and report_winners_per_category function"""
    start = time.time()
    read_input_file(file_path)
    winners_per_batch = get_winners(players, committee_lottery_numbers)  # multi-processing in batches
    winners = report_winners_per_category(winners_per_batch)
    end = time.time()
    print(winners)
    print("Program Runtime: ", end - start)


def validate_user_input(numbers: List[str]) -> bool:
    """
    Validate the user input
    :param numbers: list of characters
    :return: True if the input is valid, False otherwise
    """
    if len(numbers) == 5 and \
        all([number.isdigit() for number in numbers]) and \
        all([int(number) in range(1,91) for number in numbers]) and \
        len(set(numbers)) == 5:
        return True
    return False


if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input", type=str, help="Path to the test file")
    args = args.parse_args()

    players = read_input_file(args.input)  # return list of all players numbers
    while(True):
        print("READY")
        numbers = input(">>> ").split()
        if validate_user_input(numbers):
            calculate_runtime(players, numbers, args.input)  # print the program execution runtime
        else:
            print("Invalid input. Please enter 5 distinct numbers in the inclusive range [1,90], separated by spaces")

    # # SINGLE PROCESS (~ 1 second slower than Multi-Processing)
    # start_single_proc = time.time()
    # process_winner_map = update_winner_map(players, committee_lottery_numbers)
    # winners_per_match_category = [str(value) + " " for value in process_winner_map.values()]
    # print(''.join(winners_per_match_category).rstrip())
    # end_single_proc = time.time()
    # print("Single Process runtime: ", end_single_proc - start_single_proc)