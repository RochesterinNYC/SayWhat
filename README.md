SayWhat
------

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
- Django Framework context
- Facebook Integration
- Twitter Integration
- Manual Text Integration
- Oauth