markov_string
=============

A small, minimally-efficient Markov string generator.

Installation
------------

After cloning this repository, just run `python setup.py install`.


Sample Usage
------------

    # import and initialize model.
    import markov_string
    model = markov_string.MarkovModel()

    # read input file, line by line, into markov model.
    with open('sample-text.txt', 'r') as input_file:
      for line in input_file:
        model.add(line)
    
    # generate text, ensuring that the generated text is not a stem or leaf of one of the input lines.
    for phrase in model.generate(num=10, new_only=True):
      print phrase