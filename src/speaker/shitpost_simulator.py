import markovify
import pickle
import argparse
import time
from time import sleep

def main(args):
    text_model = None

    if args.json_model:
        with open(args.json_model) as json_model:
            json_model_str = json_model.read(-1)
            text_model = markovify.Text.from_json(json_model_str)
    i = 0
    while True:
        print('{}: {}'.format(i, text_model.make_sentence()))
        i += 1
        sleep(1)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json_model',
        type=str,
        default='',
        help='Use the json model'
    )
    args, unparsed = parser.parse_known_args()
    main(args)
