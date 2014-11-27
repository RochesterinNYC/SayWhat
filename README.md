SayWhat
------

####Current Status:

Basic oauth flow and prediction user flow are implemented.
User can basically oauth through GroupMe and have ~100 sentences predicted for them through webapp.

####To Use:

Until the Django framework and GroupMe oauth are implemented, the only way to authenticate and train the markov bot on a corpus composed of the messages from your GroupMe groups is to get a groupme api token for your account and set it to the 'GROUPME_API_TOKEN' system variable.

####Functionality:

Predicts text output for various social circuits like GroupMe, Twitter, Facebook, etc. given access to previous text material (corpus).

####Technical/Theoretical Considerations:

GroupMe:
- Complete sentences might be broken up into multiple messages
- No ending punctuation for most sentences probably (informal typing/text)

Observations/Issues to Fix:
- If first word selected is rare and has only been used once in a sentence of other rare words, then the original message sentence will probably be generated. (Solution: replace with rare tags for words < 5 frequency?) 
- Images, smileys, links all are usually one word and don't really represent regular words.

####To Add:
- Caching
- Refactoring of model associations/usage
- Sessioningo
- Front-end Styling
- Facebook Integration
- Twitter Integration
- Manual Text Integration
