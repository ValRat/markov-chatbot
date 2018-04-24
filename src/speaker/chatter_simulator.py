import markovify
import pickle
import argparse
import time
import numpy as np
from time import sleep

def main(args):
    markov_models = []
    for model in args.json_model:
        with open(model) as json_model:
            json_model_str = json_model.read(-1)
            markov_models.append(markovify.Text.from_json(json_model_str))
    if len(args.weights) == 1:
        args.weights = np.ones(len(args.json_model))
    text_model = markovify.combine(markov_models, args.weights)
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
        nargs='+',
        help='Use the json model, if more than one is specified then the models are combined'
    )
    parser.add_argument(
        '--weights',
        type=int,
        nargs='+',
        default='1',
        help='Used with multiple models, represents the weight of each model on the combined product'
    )
    args, unparsed = parser.parse_known_args()
    main(args)
