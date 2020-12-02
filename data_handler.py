import json
import logging

# f = "%(asctime)s: %(message)s"
# logging.basicConfig(format=f, level=logging.INFO, datefmt="%H:%M:%S")


class DataHandler:
    _EVENT_TYPE_KEY = 'event_type'
    _DATA_KEY = 'data'
    _TIMESTAMP_KEY = 'timestamp'

    def handle_data(self, stat_line, data_class):
        try:
            stat_event_type = stat_line[self._EVENT_TYPE_KEY]
            stat_data_word = stat_line[self._DATA_KEY]
            stat_timestamp = stat_line[self._TIMESTAMP_KEY]

            data_class.increase_event_type_count(stat_event_type)
            data_class.increase_data_word_count(stat_data_word)
        except KeyError:
            logging.info("Stat line is missing basic key, skipping stat")


class StatsFakeDatabase:
    def __init__(self):
        self.event_types_count = {}
        self.data_words_count = {}

    def increase_event_type_count(self, stat_event_type):
        if stat_event_type in self.event_types_count:
            self.event_types_count[stat_event_type] += 1
        else:
            self.event_types_count[stat_event_type] = 1

    def increase_data_word_count(self, stat_data_word):
        if stat_data_word in self.data_words_count:
            self.data_words_count[stat_data_word] += 1
        else:
            self.data_words_count[stat_data_word] = 1

    def get_event_types_stats(self):
        return json.dumps(self.event_types_count)

    def get_data_words_stats(self):
        return json.dumps(self.data_words_count)
