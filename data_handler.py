from base_logger import logger


class DataHandler:
    """
    Acts as a "controller".
    Gets parsed stats rows, runs quick validation and sends each row to the DB.
    """
    _EVENT_TYPE_KEY = 'event_type'
    _DATA_KEY = 'data'
    _TIMESTAMP_KEY = 'timestamp'

    def handle_data(self, stat_line, stats_db):
        try:
            stat_event_type = stat_line[self._EVENT_TYPE_KEY]
            stat_data_word = stat_line[self._DATA_KEY]
            stat_timestamp = stat_line[self._TIMESTAMP_KEY]

            stats_db.increase_event_type_count(stat_event_type)
            stats_db.increase_data_word_count(stat_data_word)
        except KeyError:
            logger.error("Stat line is missing basic key, skipping")


class StatsFakeDatabase:
    """
    Acts as a fake DB.
    Stores all the stats about event types and words counts while providing basic getters and setters methods.
    """
    def __init__(self):
        self._event_types_count = {}
        self._data_words_count = {}

    def increase_event_type_count(self, stat_event_type):
        if stat_event_type in self._event_types_count:
            self._event_types_count[stat_event_type] += 1
        else:
            self._event_types_count[stat_event_type] = 1

    def increase_data_word_count(self, stat_data_word):
        if stat_data_word in self._data_words_count:
            self._data_words_count[stat_data_word] += 1
        else:
            self._data_words_count[stat_data_word] = 1

    def get_event_types_stats(self):
        return self._event_types_count

    def get_data_words_stats(self):
        return self._data_words_count
