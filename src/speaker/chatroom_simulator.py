import markovify
import pickle
import argparse
import time
import random
from pathlib import Path
from time import sleep
from multiprocessing import Process

def spawn_speaker(speaker, len_wait):
    while True:
        wait_time = random.uniform(1, len_wait)
        sleep(wait_time)
        print(speaker.speak())

class Speaker:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def speak(self):
        return '{}: {}'.format(self.name, self.model.make_sentence())


def main(args):
    text_model = None

    if args.model_dir:
        speakers = []
        files = Path(args.model_dir).glob('*.json')
        for model_def in files:
            name = model_def.name[:-len('_model.json')].replace('_', ' ')
            json_model_str = model_def.resolve().read_text()
            text_model = markovify.Text.from_json(json_model_str)
            speakers.append(Speaker(name, text_model))

        processes = []
        for speaker in speakers:
            p = Process(target=spawn_speaker, args=(speaker, args.len_wait))
            p.start()
            processes.append(p)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model_dir',
        type=str,
        default='',
        help='json model directories'
    )
    parser.add_argument(
        '--len_wait',
        type=float,
        default='',
        help='max time the model should wait to speak'
    )
    args, unparsed = parser.parse_known_args()
    main(args)
