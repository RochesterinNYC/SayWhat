from __future__ import division
from django.db import models
import random
import requests
import json
import re


class User(models.Model):
  groupme_uid = models.CharField(max_length=100)
  access_token = models.CharField(max_length=100)
  name = models.CharField(max_length=200)
  def __str__(self):  
    return "{} {}".format(self.groupme_uid, self.name)

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
    #Length screening to prevent weird generated stuff
    if 2 < len(words) < 15:
      return (" ").join(words) 
    else:
      return self.generate_sentence()

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
    #Refactor later with nonlinear, O(logn) search
    while(randFloat > probabilities[index]):
      index += 1
    return words[index]

class GroupMeInterface:
  api_url = "https://api.groupme.com/v3/"
  
  @staticmethod  
  def get_groups(access_token):
    #Pagination in returning of group data by GroupMe API
    page_to_get = 1
    all_groups_present = False
    all_groups = []
    while not all_groups_present:    
      params = {'token': access_token, 'page': page_to_get, 'per_page': 25}
      r = requests.get(GroupMeInterface.api_url + 'groups', params=params)
      if r.status_code is 200:
        content = json.loads(r._content)
        groups_array = content['response']         
        if groups_array:
          all_groups_present = True
        else:
          all_groups.extend(groups_array)
    return groups_array

  @staticmethod  
  def get_group(access_token, group_id, groups=None):
    if groups is None: groups = GroupMeInterface.get_groups(access_token)
    group = None
    index = 0
    while group == None and index < len(groups):
      current_group = groups[index]
      if current_group['id'] == group_id: group = current_group
      index += 1
    return group


  @staticmethod  
  def get_all_messages(access_token, group_id):
    all_messages_present = False
    last_message_id = None
    all_messages = []
    limit = 100
    #Keep collecting messages until a get_messages call returns less than the limit
    while not all_messages_present:
      current_messages = GroupMeInterface.get_messages(access_token, group_id, limit, last_message_id) 
      all_messages.extend(current_messages)
      last_message_id = all_messages[len(all_messages) - 1]['id']
      if len(current_messages) < limit: all_messages_present = True 
    return all_messages

  @staticmethod  
  def get_messages(access_token, group_id, limit, before_id):
    messages = []
    params = {'token': access_token, 'limit': limit}
    if before_id is not None: params['before_id'] = before_id
    r = requests.get(GroupMeInterface.api_url + 'groups/{}/messages'.format(group_id), params=params)
    if r.status_code is 200:
      content = json.loads(r._content)
      messages = content['response']['messages']
    return messages

  @staticmethod  
  def get_user_info(access_token): 
    params = {'token': access_token}  
    r = requests.get(GroupMeInterface.api_url + 'users/me', params=params)
    user_info = None
    if r.status_code is 200:
      content = json.loads(r._content)
      user_info = content['response']
    return user_info

  @staticmethod
  def get_sentences(messages):
    sentences = []
    for message in messages:
      #Ignore system generated messages like "User was added"
      if not message['system'] and message['name'] != 'GroupMe': 
        if message['text'] is not None:
          text = message['text'].strip()
          for sentence in re.split('[.?!]', text):
            #Generate start and end tags
            if sentence != '': sentences.append("_START_TAG_ _START_TAG_ {} _STOP_TAG_".format(sentence.strip().encode('ascii', 'ignore')))
    return sentences