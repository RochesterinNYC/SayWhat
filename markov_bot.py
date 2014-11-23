
class MarkovBot:
  def __init__(self):
    self.trigram_counts = {}
    self.bigram_counts = {}

  #corpus is an array of sentences
  #q(w|u, v) = c(u, v, w) / c(u, v)
  #START START test me now END
  def train(self, corpus):
    for sentence in corpus:
      words = sentence.split(" ")
      index = 2 #first word is at index 2 because of 2 start tags
      while(index < len(words)):
        u = words[index - 2]
        v = words[index - 1]
        w = words[index]
        #Update trigram count
        if u not in self.trigram_counts: self.trigram_counts[u] = {}
        if v not in self.trigram_counts[u]: self.trigram_counts[u][v] = {}
        if w not in self.trigram_counts[u][v]: self.trigram_counts[u][v][w] = 0
        self.trigram_counts[u][v][w] += 1
        #Update bigram count
        if u not in self.bigram_counts: self.bigram_counts[u] = {}
        if v not in self.bigram_counts[u]: self.bigram_counts[u][v] = 0
        self.bigram_counts[u][v] += 1
        index += 1