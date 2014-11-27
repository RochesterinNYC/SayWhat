SayWhat
------

####Current Status:

- HEROKU DEPLOYMENT in progress. (R10 Timeout Error)
- Basic oauth flow and prediction user flow are implemented.
- User can basically oauth through GroupMe and have ~100 sentences predicted for them through webapp.

####To Use:

Until the Heroku deployment is complete, a GroupMe API client ID is required and should be stored as the 'GROUPME_API_TOKEN' system variable.

####To Run:

    pip install -r requirements.txt
    python manage.py runserver

or:

    foreman start

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
