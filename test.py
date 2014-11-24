import os
import pdb
from groupme import GroupMeInterface
from markov_bot import MarkovBot

access_token = os.environ['GROUPME_API_TOKEN']
groups = GroupMeInterface.get_groups(access_token)
#Train on messages from all groups
m = []
for group in groups:
  m.extend(GroupMeInterface.get_all_messages(access_token, group['id'])) 
user = GroupMeInterface.get_user_info(access_token)
sen = GroupMeInterface.get_sentences(m)
bot = MarkovBot()

bot.train(sen)


input = raw_input("Press enter to generate sentences. Type 'quit' and press enter to quit.\n")
while input != 'quit': 
  print(bot.generate_sentence()) 
  input = raw_input("Press enter to generate sentences. Type 'quit' and press enter to quit.\n")


