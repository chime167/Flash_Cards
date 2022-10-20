#!/usr/bin/env python3
import json
import random
from io import StringIO
import argparse


'''CLI parameters:
        -import_from: file you want to import cards from to this session
        -export_to: file you want to write to when done
    Input parameters:
        -add: you will be prompted to write first a term and then its definition
        -remove: you will be prompted to write the term of the card you want to delete
        -import: enter the file of flash cards you want imported to the session
        -export: enter the file you want to write this session's flash cards to
        -ask: enter the number of times you want to guess a card
        -log: enter the name of the file you want to write a log of the entire session to
        -hardest card: tells you which card(s) you've missed the most
        -reset stats: resets the count for how many times you've missed cards'''


parser = argparse.ArgumentParser()
parser.add_argument('--import_from', help='Enter file to import flashcards from')
parser.add_argument('--export_to', help='Enter file to export new flashcards to')
args = parser.parse_args()
flash_dict = {}
output = StringIO()
import_file = args.import_from
export_file = args.export_to


def printf(text):
    print(text, end='\n', file=output)
    print(text)


def inputf(text):
    output.write(text)
    return input(text)


def add_card():
    card = inputf(f'The card:\n')
    output.write(f'{card}\n')
    while card in flash_dict:
        card = inputf(f'The term "{card}" already exists. Try again:\n')
        output.write(f'{card}\n')
    answer = inputf(f'The definition of the card:\n')
    output.write(f'{answer}\n')
    while answer in [value['definition'] for value in flash_dict.values()]:
        answer = inputf(f'The definition "{answer}" already exists. Try again:\n')
        output.write(f'{card}\n')
    flash_dict.update({card: {'definition': answer, 'times_missed': 0}})
    printf(f'("{card}":"{answer}") has been added.')
    return


def remove_card():
    card = inputf('Which card?\n')
    output.write(f'{card}\n')
    if card not in flash_dict:
        printf(f'Can\'t remove "{card}": there is no such card.')
        return
    flash_dict.pop(card)
    printf('The card has been removed.')
    return


def export_cards():
    file = inputf('File name:\n')
    output.write(f'{file}\n')
    with open(file, 'w') as f:
        f.write(json.dumps(flash_dict))
    printf(f'{len(flash_dict)} cards have been saved.')
    return


def import_cards():
    file = inputf('File name:\n')
    output.write(f'{file}\n')
    try:
        with open(file, 'r') as f:
            flash_dict.update(json.load(f))
        printf(f'{len(flash_dict)} cards have been loaded.')
    except FileNotFoundError:
        printf('File not found.')
    finally:
        return


def ask_cards():
    terms = [*flash_dict.keys()]
    how_many = inputf('How many times to ask?\n')
    output.write(f'{how_many}\n')
    for _ in range(int(how_many)):
        term = random.choice(terms)
        guess = inputf(f'Print the definition of "{term}":\n')
        output.write(f'{guess}\n')
        correct_answer = flash_dict.get(term).get('definition')
        if guess == correct_answer:
            printf('Correct!')
        elif guess in [value['definition'] for value in flash_dict.values()]:
            flash_dict.get(term)['times_missed'] += 1
            other_ans = ''.join({k for k, v in flash_dict.items() if v['definition'] == guess})
            printf(f'Wrong. The right answer is "{correct_answer}", but your definition is correct for "{other_ans}".')
        else:
            flash_dict.get(term)['times_missed'] += 1
            printf(f'Wrong. The right answer is "{correct_answer}".')


def log():
    file = inputf('File name:\n')
    output.write(f'{file}\n')
    full = output.getvalue().split('\n')
    with open(file, 'w') as f:
        for line in full:
            f.write(line)
    printf('The log has been saved.')
    return


def hardest_card():
    if not flash_dict or max(v['times_missed'] for k, v in flash_dict.items()) == 0:
        printf('There are no cards with errors.')
        return
    hardest_number = max(v['times_missed'] for v in flash_dict.values())
    hardest = {k for k, v in flash_dict.items() if v['times_missed'] == hardest_number}
    if len(hardest) == 1:
        hardest = ''.join(hardest)
        printf(f'The hardest card is "{hardest}". You have {hardest_number} errors answering it')
    else:
        printf(f"The hardest cards are \"{', '.join(hardest)}\". You have {hardest_number} errors answering them.")
    return


def reset_stats():
    for v in flash_dict.values():
        v['times_missed'] = 0
    printf('Card statistics have been reset.')


def import_func():
    output.write(f'{import_file}\n')
    try:
        with open(import_file, 'r') as f:
            flash_dict.update(json.load(f))
        printf(f'{len(flash_dict)} cards have been loaded.')
    except FileNotFoundError:
        printf('File not found.')
    finally:
        return


def export_func():
    output.write(f'{export_file}\n')
    with open(export_file, 'w') as f:
        f.write(json.dumps(flash_dict))
    printf(f'{len(flash_dict)} cards have been saved.')
    return


commands = {'add': add_card, 'remove': remove_card, 'import': import_cards, 'export': export_cards, 'ask': ask_cards,
            'log': log, 'hardest card': hardest_card, 'reset stats': reset_stats}

if import_file:
    import_func()

while True:
    action = inputf('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
    output.write(f'{action}\n')
    if action == 'exit':
        if export_file:
            export_func()
        printf('Bye bye!')
        exit()
    elif action not in commands:
        printf('Not a valid command.')
        exit()
    commands[action]()


