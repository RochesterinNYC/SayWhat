import requests
import json
import re

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