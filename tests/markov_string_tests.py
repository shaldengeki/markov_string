from nose.tools import *
import markov_string

class testMarkovModelClass(object):
  @classmethod
  def setUpClass(self):
    self.test_doc = u"A B C A B C A B D A"
    self.test_docs = [self.test_doc, self.test_doc, self.test_doc]

  def testTokenizeSingleDocument(self):
    model = markov_string.MarkovModel()
    assert model.tokenize_doc(self.test_doc) == self.test_doc.split(u' ')

  def testAddSingleDocument(self):
    model = markov_string.MarkovModel()
    model.add(self.test_doc)
    assert len(model.docs) == 1
    model.add(self.test_doc)
    assert len(model.docs) == 2
    model.add(self.test_doc)
    assert len(model.docs) == 3    

  def testAddManyDocuments(self):
    model = markov_string.MarkovModel()
    model.add_docs(self.test_docs)
    assert len(model.docs) == 3    

  @raises(markov_string.InvalidDocumentError)
  def testTokenizeInvalidDocument(self):
    model = markov_string.MarkovModel()
    model.tokenize_doc([])

  @raises(markov_string.InvalidDocumentError)
  def testTokenizeWithStoredInvalidDocument(self):
    model = markov_string.MarkovModel().add([])
    model.tokenize()

  def testTokenizeManyDocuments(self):
    model = markov_string.MarkovModel()
    model.add_docs(self.test_docs)
    model.tokenize()
    assert model.tokens(u'A') == {u'B': 9, u'': 3}
    assert model.tokens(u'B') == {u'C': 6, u'D': 3}

  def testNormalize(self):
    model = markov_string.MarkovModel()
    model.add_docs(self.test_docs)
    model.tokenize().normalize()
    assert model.frequencies(u'A') == [(u'', 0.25), (u'B', 1)]