import markovify
import pickle
import argparse
import time
from time import sleep

def main(args):
    text_model = None

    if args.use_json_model:
        with open(args.use_json_model) as json_model:
            json_model_str = json_model.read(-1)
            text_model = markovify.Text.from_json(json_model_str)
    else:
        with open(args.message_file, 'rb') as msgs:
            messages_dictionary = pickle.load(msgs)
            for name, message in messages_dictionary.items():
                # Not enough messages 
                if (len(message) < 1000): continue

                print('Making model for: {}'.format(name))
                t0 = time.time()
                message = '. '.join(message)
                json_filename = name.replace(' ', '_') + '_model.json'
                text_model = markovify.Text(message)
                t1 = time.time()
                print('    Model creation time: {:0.2f}'.format(t1 - t0))

                with open(json_filename, 'w+') as out_json_file:
                    model_json = text_model.to_json()
                    out_json_file.write(model_json)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--message_file',
        type=str,
        default='',
        help='Path to the pickle file'
    )
    parser.add_argument(
        '--save_json_filename',
        type=str,
        default='',
        help='Save the model as JSON'
    )
    parser.add_argument(
        '--use_json_model',
        type=str,
        default='',
        help='Use the json model rather than creating a new model'
    )
    args, unparsed = parser.parse_known_args()
    main(args)
