### What is this?
This is an implementation of a Non-Blocking Producer-Consumer stream processing service.

### How it is implemented?
Using Python Threads and an infinite Queue (which is thread-safe).  
The producer/s gets the data from the .exe file, validates it and inserts it into the Queue, while the consumer/s  
takes this data from the Queue and sends it to the BL layer.  
Inside this layer the data is being validated again and saved into the DB (fake, object).  
The data is exposed using a simple HTTP interface, implemented with Flask.

### What is being calculated?
Statistics about events (formed as JSONs) generated live using an .exe file.
The stats are (formed as JSONs):
* The number of times each event appears (by type).
* The number of times each word appears under the data field.

### How to use it?
* Clone the project into your working environment.
* Download the .exe file that generates events and locate it in a path of your desire.
* Navigate to the config.json configuration file and insert the path of the .exe file.
* If you'd like to change the amount of producers/consumers, do this in the configuration file as well (default is 1).
* Install the dependencies using pip install -r requirements.txt.
* Navigate to the main.py file and execute it.
* Open a browser and navigate to your localhost/big_panda_home_test/api/event_types or  
  localhost/big_panda_home_test/api/words to see the statistics.

### Bonus suggestion
Reminder: add an option to get the stats from the last 60 seconds.  

Use 2 stacks!  
* Take all the valid data and insert it into a stack (in parallel to the regular database).
* When the last 60 seconds data is requested:
    * Verify the stack is not empty.
    * Peek every item and check:
        * If now - timestamp > 60 seconds:
            * Pop the item.
            * Add stats to general dictionary (if already exists increment, else create new one).
            * Enqueue the item into temp Stack.
        * When no more items are left from the last 60 seconds:
            * Pop item from the temp Stack.
            * Enqueue item to original Stack.
        * When temp Stack is empty, return results.
