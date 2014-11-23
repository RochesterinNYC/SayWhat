import os
import pdb
from groupme import GroupMeInterface
from markov_bot import MarkovBot

access_token = os.environ['GROUPME_API_TOKEN']
s = GroupMeInterface.get_groups(access_token)
m = GroupMeInterface.get_all_messages(access_token, '10252279')
user = GroupMeInterface.get_user_info(access_token)
sen = GroupMeInterface.get_sentences(m)
bot = MarkovBot()

bot.train(sen)

print(bot.generate_sentence())
