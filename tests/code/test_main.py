from main import update_winner_map, get_winners, report_winners_per_category
import pytest


test_inputs_update_winner_map = [
    (['1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n'], ['2','3','5','7','9'], {2: 0, 3: 3, 4: 0, 5: 0}),
    (['1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n'], ['7','8','9','10','11'], {2: 0, 3: 0, 4: 0, 5: 1}),
    (['1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n'], ['17','18','19','12','13'], {2: 0, 3: 0, 4: 0, 5: 0}),
    ]
@pytest.mark.parametrize("players, committee_lottery_numbers, winners_per_category", test_inputs_update_winner_map)
def test_update_winner_map(players, committee_lottery_numbers, winners_per_category):
    assert update_winner_map(players, committee_lottery_numbers) == winners_per_category


test_inputs_get_winners = [
    (
        ['1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n', '1 2 3 4 5\n'], 
        ['2','3','5','7','9'],
        [
            {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, 
            {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, 
            {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}
        ]),
    (
        ['1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n', '1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n', '1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n'], 
        ['7','8','9','10','11'], 
        [
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 1},
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 1},
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 1},
        ]),
    (
        ['1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n', '1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n', '1 2 3 4 5\n', '1 2 3 4 6\n', '7 8 9 10 11\n'], 
        ['17','18','19','12','13'], 
        [
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, 
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, 
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, 
        ]),
    ]
@pytest.mark.parametrize("players, committee_lottery_numbers, winners_per_batch", test_inputs_get_winners)
def test_get_winners(players, committee_lottery_numbers, winners_per_batch):
    assert get_winners(players, committee_lottery_numbers) == winners_per_batch


test_inputs_report_winners_per_category = [
    (
        [
            {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, 
            {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, 
            {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}, {2: 0, 3: 1, 4: 0, 5: 0}
        ],
        '0 9 0 0'
        ),
    (
        [
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, 
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, 
            {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}, {2: 0, 3: 0, 4: 0, 5: 0}
        ], 
        '0 0 0 0'
        ),
    ]
@pytest.mark.parametrize("winners_per_batch, formatted_output", test_inputs_report_winners_per_category)
def test_report_winners_per_category(winners_per_batch, formatted_output):
    assert report_winners_per_category(winners_per_batch) == formatted_output