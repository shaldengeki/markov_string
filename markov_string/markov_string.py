import random

class InvalidDocumentError(Exception):
  pass

class TokenNotFoundError(Exception):
  pass

class MarkovModel(object):
  """
    Markov chain model as applied to documents as bag-of-words.
    Generates strings probabilistically based on documents stored using .store() or .add().
  """
  def __init__(self, min_freq=0.01):
    """
      min_freq determines the minimum frequency of a subsequent word before it's ignored in normalize()
    """
    self.min_freq = float(min_freq)
    self.reset()
  def reset(self):
    """
      Resets model.
    """
    self.docs = []
    self._tokens = self._freqs = self._model = None
    return self
  def add(self, doc):
    """
      Adds a document to the store.
    """
    self.docs.append(doc)
    return self
  def add_docs(self, docs):
    """
      Stores a list of documents.
    """
    for doc in docs:
      self.add(doc)
    return self
  def tokenize_doc(self, doc):
    """
      Splits a document into tokens.
    """
    try:
      return doc.split(u' ')
    except AttributeError:
      raise InvalidDocumentError(doc)
  def tokenize(self):
    """
      Tokenizes the model's currently-stored docs.
    """
    self._tokens = {}
    for doc in self.docs:
      tokens = self.tokenize_doc(doc)
      numTokens = len(tokens)
      if numTokens < 1:
        continue
      for i in xrange(numTokens):
        if i == 0:
          prevWord = ''
        else:
          prevWord = tokens[i-1]
        if prevWord in self._tokens:
          if tokens[i] in self._tokens[prevWord]:
            self._tokens[prevWord][tokens[i]] += 1
          else:
            self._tokens[prevWord][tokens[i]] = 1
        else:
          self._tokens[prevWord] = {tokens[i]: 1}
      if tokens[numTokens-1] not in self._tokens:
        self._tokens[tokens[numTokens-1]] = {}
      if '' in self._tokens[tokens[numTokens-1]]:
        self._tokens[tokens[numTokens-1]][''] += 1
      else:
        self._tokens[tokens[numTokens-1]][''] = 1
    return self
  def tokens(self, prev_word=None):
    """
      Returns a dict of token: count that come after a given word,
      If prev_tokens is not given, return entire tokens dict.
    """
    if prev_word is None:
      return self._tokens
    if prev_word not in self._tokens:
      raise TokenNotFoundError(prev_word)
    return self._tokens[prev_word]
  def normalize(self, min_freq=None):
    """
      Goes through a dict of tokens, converting raw counts to frequencies.
      Skips any leaf nodes that fall under min_freq.
    """
    if min_freq is None:
      min_freq = self.min_freq
    if self._tokens is None:
      self.tokenize()
    self._freqs = {}
    for word in self._tokens:
      self._freqs[word] = []
      word_sum = sum([self._tokens[word][leaf_word] for leaf_word in self._tokens[word]])
      min_count = int(min_freq * word_sum)
      # we have to recalculate the sum while we delete before we normalize.
      word_sum = float(0)
      filtered_words = []
      for leaf_word in self._tokens[word]:
        if self._tokens[word][leaf_word] >= min_count:
          word_sum += self._tokens[word][leaf_word]
          filtered_words.append(leaf_word)
      partial_sum = 0.0
      for leaf_word in filtered_words:
        partial_sum += self._tokens[word][leaf_word]
        self._freqs[word].append((leaf_word, partial_sum / word_sum))
    return self
  def frequencies(self, prev_word=None):
    """
      Returns a list of (token, freq_max) that come after a given word, ordered by increasing probability.
      If prev_tokens is not given, return entire frequencies dict.
    """
    if prev_word is None:
      return self._freqs
    if prev_word not in self._freqs:
      raise TokenNotFoundError(prev_word)
    return self._freqs[prev_word]
  def generate(self, num=1, seed_word=None, new_only=False):
    """
      Generates markov docs.
      Returns a generator.
    """
    if self._freqs is None:
      self.normalize()
    random.seed()
    phrase_num = 0
    while phrase_num < num:
      thisWord = seed_word
      if thisWord is None:
        while thisWord is None:
          randNum = random.random()
          for (model_word, freq) in self._freqs[u'']:
            if randNum <= freq:
              thisWord = model_word
              break
      sentence = [thisWord]
      while ' '.join(sentence) == '' or thisWord != u'':
        if thisWord not in self._freqs:
          break;
        randNum = random.random()
        for (model_word, freq) in self._freqs[thisWord]:
          if randNum < freq:
            sentence.append(model_word)
            thisWord = model_word
            break
      phrase = u' '.join(sentence).strip()
      # if new_only is set, make sure that this isn't in the training set (and it's not a stem/leaf of something in there)
      if new_only:
        stemmed = False
        for doc in self.docs:
          if phrase is doc or doc.startswith(phrase) or doc.endswith(phrase):
            stemmed = True
            break
        if stemmed:
          continue
      yield phrase
      phrase_num += 1