# Dbpedia Warm-Up Tasks

* [Arabic number to Roman number Chatbot](#arabic-number-to-roman-number-chatbot) 
* [Access QA system via API](#access-qa-system-via-api)

### Arabic number to Roman number Chatbot
Run the script as: python chatbot_warmup_task.py 

#### Example Snippet
>> Hi! This is a simple chatbot which translates arabic numbers to roman numbers.

>> Enter your query (press e to exit): Convert 23 into roman number<br>
XXII

>> Enter your query (press e to exit): Convert 23, 34 and 760<br>
XXIII XXXIV DCCLX

>> Enter your query (press e to exit): 42, 8, 90<br>
XLII VIII XC

>> Enter your query (press e to exit): Hey! <br>
Invalid query

#### Working of the bot
The bot accepts a query from the user. It extracts numbers from the query and converts them into their corresponding roman number. If there are no numbers in the query, it prompts the user to enter a valid query!

***

### Access QA system via API
**About:** This is a telegram bot which accesses the QA system of WolframAlpha. <br>
To run this bot, a telegram account would be required. Make a new bot by sending the message "/newbot" to @BotFather on telegram. Store the token received in a secrets.py file (in the same directory where question_answering_bot.py is stored). This token will be used to access the Telegram Bot API.  

Now, to access WolframApha's API, get registered on the site and request for a new APP_ID. Store the APP_ID in the secrets.py file where bot's token was saved. 

Finally, run the script as: python question_answering_bot.py from the terminal.

#### Dependencies to be installed:
* requests
* urllib

#### Example Snippet
Start the conversation with the bot by typing: <br>
q: `/start` <br>
>> Hi! I'm a simple Question-Answering bot. Send /commands to check which commands I accept or just ask me anything you want to!

q: `/commands` <br>
>> Type: <br>
 /history - to see your search queries
 
q: What is Brexit?
>> Looking for a short answer.. <br>
 No short answer available  <br>
 Let me search for a descriptive one.. <br>
 ![Image of Query Response](https://github.com/rrichajalota/dbpedia_warmup_tasks/blob/master/brexit.jpg)


