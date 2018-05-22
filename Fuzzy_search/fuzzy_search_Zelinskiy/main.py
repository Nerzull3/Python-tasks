import argparse
import os
import re

from levenshteins_distance import get_distance

PREMISSIBLE_DIST = 1  # permissible Levenshtein distance


def search_for_entries(text, words, filename):
    if not text:
        raise ValueError('Text is absent in file!')
    if not words:
        raise ValueError('No search words!')

    result = []
    regex = re.compile(r'[\w\d\'-]+')

    for word in words:
        number_of_line = 1

        for j in range(len(text)):
            text_words = get_words(text[j].split(), regex)

            if text_words and text_words[-1][-1] == '-':  # check on line break
                temp = get_words(text[j + 1].split(), regex)
                if temp:
                    text_words[-1] = text_words[-1][0:-1] + temp[0]

            for i in range(len(text_words)):
                distance = get_distance(word.lower(), text_words[i].lower())  # case-insensitivity
                if distance <= PREMISSIBLE_DIST:
                    print(f'Word: \"{text_words[i]}\", '
                          f'filename: \"{filename}\", '
                          f'line: {number_of_line}, '
                          f'place: {i + 1}, '
                          f'mistakes: {distance}'
                          )
                    result.append((text_words[i], number_of_line, i + 1, distance))

            number_of_line += 1

    return result


def get_words(words, regex):
    res = []
    for word in words:
        for match in re.finditer(regex, word):
            res.append(word[match.start():match.end()])
    return res


def __create_parser():
    parser = argparse.ArgumentParser(
        usage='-tf [paths to text files in a space] -wf [path to word files in a space] [-w [words]]'
    )
    parser.add_argument(
        '-tf',
        '--text_files',
        required=True,
        nargs='+',
        help='enter text files after this function'
    )
    parser.add_argument(
        '-wf',
        '--word_files',
        required=True,
        nargs='+',
        help='enter word files after this function'
    )
    parser.add_argument(
        '-w',
        '--words',
        required=False,
        nargs='+',
        help='enter words after this function'
    )

    return parser


def parser_of_words(files):
    searching_words = []
    regex = re.compile(r'[\w\'-]+')

    for file in files:
        with open(file) as f:
            for line in f.readlines():
                searching_words.extend(re.findall(regex, line))

    return searching_words


if __name__ == '__main__':
    parser = __create_parser()
    args = parser.parse_args()

    text_files = args.text_files  # All paths to files
    searching_words = parser_of_words(args.word_files)  # Searching words
    words = args.words
    if words:
        searching_words.extend(words)  # Full searching words

    for file in text_files:
        filename = os.path.splitext(os.path.basename(file))[0]
        with open(file, 'r') as f:
            search_for_entries(f.readlines(), searching_words, filename)
