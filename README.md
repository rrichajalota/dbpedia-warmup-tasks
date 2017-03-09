# Dbpedia Warm-Up Tasks

* [Arabic number to Roman number Chatbot] (#Arabic-number-to-Roman-number-Chatbot) 
* Access QA system via API

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

