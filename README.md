In progress:

Markov Chain testing using fb messages
```
.
├── README.md
└── src
    ├── parser
    │   ├── model_generator.py
    │   └── parser.py           
    └── speaker
        ├── chatroom_simulator.py
        ├── chatter_simulator.py
        └── models
```


A small little project using personal chat data downloaded from Facebook.

## parser.py
This file crawls through all the embedded html messages and saves each user and their messages as a key value pair.
The resulting dictionary can then be saved as a pickle (to save time from re-parsing) if the `--save_dict` flag is passed
with the filename as the argument.

For one file:
```
python parser.py --file_in conversations_with_steve.html
```

For an entire directory:
```
python parser.py --dir facebook_chats/messages --save_dict messages.pkl
```

## model_generator.py
Uses [markovify](https://github.com/jsvine/markovify) to create models from the dictionary generated by `parser.py`.
It saves each model as `.json` file to be used in other applications.

```
python model_generator.py --message_file messages.pkl 
```

## chatter_simulator.py
Takes in one or more models in a `.json` format as well as optional weights for each model and create sentences from the resulting model.
One model:
```
python chatter_simulator.py --json_model models/Steve_Irwin.json
```

Multiple models with weights:
```
python chatter_simulator.py --json_model models/Steve_Irwin.json models/Steve_Jobs.json --weights 1 10
```


## chatroom_simulator.py
Takes in a directory containing models in a `.json` format and imitates a chatroom. The `len_wait` is the amount of time a model waits before speaking again (controls the chatroom speed).
```
python chatroom_simulator.py --model_dir models --len_wait=100
```





