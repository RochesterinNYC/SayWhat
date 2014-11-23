import requests
import json
import os

class GroupMeInterface:
  api_url = "https://api.groupme.com/v3/"
  access_token = os.environ['GROUPME_API_TOKEN']
  
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
    
'''
  @staticmethod  
  def get_group(access_token, group_id):

  @staticmethod  
  def get_all_messages(access_token, group_id):

  @staticmethod  
  def get_messages(access_token, group_id):

  @staticmethod  
  def get_user_info(access_token): 
'''
