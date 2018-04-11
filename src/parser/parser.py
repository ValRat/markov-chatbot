from html.parser import HTMLParser
from collections import defaultdict
from pathlib import Path
import glob
import argparse
import os
import pickle

class HTMLMessageParser(HTMLParser):

    def __init__(self, convert_charrefs=True):
        super().__init__()
        self.conversations = defaultdict(list)
        self.current_speaker = None
        self.in_user_tag = False
        self.in_message_tag = False

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'class' and attr[1] == 'user':
                self.in_user_tag = True
                continue
            else:
                self.in_user_tag = False
        if (tag == 'p'):
            self.in_message_tag = True
        else:
            self.in_message_tag = False


    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if (self.in_user_tag):
            self.current_speaker = data
            self.in_user_tag = False
        if (self.in_message_tag):
            self.conversations[self.current_speaker].append(data)
            self.in_message_tag = False


def validate_args(args):
    if not args.file_in and not args.dir:
        raise ValueError('Please have file or directory specified')
        
def process(parser, input_file):
    msg = input_file.read_text()
    parser.feed(msg)
    
        

def main(args):
    parser = HTMLMessageParser()
    if (args.file_in): 
        file_in = Path(args.file_in)
        process(parser, file_in)
    if (args.dir):
        files =  Path(args.dir).glob('*.html')
        print(files)
        for input_file in files:
            process(parser, input_file.resolve())
            print('Processed {}'.format(input_file))
    if (args.save_dict):
        Path(args.save_dict).touch()
        file_out = Path(args.save_dict).open(mode='wb')
        pickle.dump(parser.conversations, file_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file_in',
        type=str,
        default='',
        help='Path to the file'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='',
        help='Directory containing html files'
    )
    parser.add_argument(
        '--save_dict',
        type=str,
        default='',
        help='A file to save the dictionary of messages to, doesn\'t save if unspecified'
    )
    args, unparsed = parser.parse_known_args()
    validate_args(args)
    main(args)

