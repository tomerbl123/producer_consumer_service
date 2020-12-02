import subprocess
import json
import threading
import logging
import flask

from queue import Queue

from data_handler import DataHandler, StatsFakeDatabase
from configuration import EXE_FILE_PATH

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


def producer(stats_queue, exe_file_path):
    process = subprocess.Popen(exe_file_path, stdout=subprocess.PIPE)

    for index, line in enumerate(iter(process.stdout.readline, b''), start=1):
        try:
            parsed_stat_line = json.loads(line)
            stats_queue.put(parsed_stat_line)
        except Exception:  # There are few possible decoding exceptions here, predicting all of them atm is overkill.
            logging.info(f"Stat line number {index} is not a valid JSON, skipping")


def consumer(stats_queue, data_handler_object, data_class_object):
    while True:
        if not stats_queue.empty():
            stat = stats_queue.get()
            data_handler_object.handle_data(stat_line=stat, data_class=data_class_object)


@app.route('/', methods=['GET'])
def home():
    event_types_total_count = stats_fake_db.get_event_types_stats()
    data_words_total_count = stats_fake_db.get_data_words_stats()
    return "Events stats: " + event_types_total_count + ", Data words stats :" + data_words_total_count


if __name__ == '__main__':
    queue = Queue()
    stats_fake_db = StatsFakeDatabase()
    data_handler = DataHandler()

    f = "%(asctime)s: %(message)s"
    logging.basicConfig(format=f, level=logging.INFO, datefmt="%H:%M:%S")

    p = threading.Thread(target=producer, args=(queue, EXE_FILE_PATH), daemon=True)
    c = threading.Thread(target=consumer, args=(queue, data_handler, stats_fake_db), daemon=True)

    logging.info("Starting producer thread")
    p.start()
    logging.info("Starting consumer thread")
    c.start()

    app.run()
