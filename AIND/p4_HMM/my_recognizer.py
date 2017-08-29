import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    
    # raise NotImplementedError
    
    for index in range(len(test_set.wordlist)):
      X,lengths = test_set._hmm_data[index]
      prob_dic ={}
      prob = float("-inf")
      guess = "guess"
      for key in models:
        model = models[key]
        prob_dic[key] = float("-inf")
        try:
          logL = model.score(X, lengths)
          prob_dic[key] = logL
          if logL > prob:
            prob = logL
            guess = key
            
        except:
          # print("scoring fail")
          continue
      probabilities.append(prob_dic)
      guesses.append(guess)
    return probabilities, guesses

