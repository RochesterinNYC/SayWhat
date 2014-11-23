from __future__ import division
import random

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

  def generate_sentence(self):
    current = ["_START_TAG_", "_START_TAG_"]
    words = []
    while current[1] != "_STOP_TAG_":
      next_word = self.generate_word(current)
      words.append(next_word)
      current[0] = current[1]
      current[1] = next_word
    words.pop()
    return (" ").join(words)

  def generate_word(self, current):
    possible = self.trigram_counts[current[0]][current[1]]
    bigram_count = self.bigram_counts[current[0]][current[1]]

    words = []
    probabilities = []
    total = 0
    for possible_word in possible.keys():
      prob = possible[possible_word] / bigram_count
      total += prob
      words.append(possible_word)
      probabilities.append(total)
      #0.1 0.2 0.3
      #0.1, 0.3, 0.6
      #0.4 generated
    #Randomly generate word, more likely words have larger chances of being generated
    randFloat = random.uniform(0, 1)
    index = 0
    while(randFloat > probabilities[index]):
      index += 1
    return words[index]