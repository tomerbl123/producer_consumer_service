import subprocess
import json
import threading
import flask

from queue import Queue
from flask import jsonify

from base_logger import logger
from data_handler import DataHandler, StatsFakeDatabase

app = flask.Flask(__name__)


def producer(stats_queue, exe_file_path):
    process = subprocess.Popen(exe_file_path, stdout=subprocess.PIPE)

    for index, line in enumerate(iter(process.stdout.readline, b''), start=1):
        try:
            logger.debug(f"about to parse line number {index}")
            parsed_stat_line = json.loads(line)
            stats_queue.put(parsed_stat_line)
        except Exception:  # There are few possible decoding exceptions here, predicting all of them will be an overkill
            logger.error(f"Stat line number {index} is not a valid JSON, skipping")


def consumer(stats_queue, data_handler, stats_db):
    while True:
        if not stats_queue.empty():
            stat = stats_queue.get()
            data_handler.handle_data(stat_line=stat, stats_db=stats_db)


@app.route('/big_panda_home_test/api/event_types', methods=['GET'])
def get_event_types_stats():
    return jsonify({'event_types': stats_fake_db.get_event_types_stats()})


@app.route('/big_panda_home_test/api/words', methods=['GET'])
def get_words_stats():
    return jsonify({'words': stats_fake_db.get_data_words_stats()})


if __name__ == '__main__':
    # Queue in python3 is thread-safe, implementing all the required locking semantics.
    queue = Queue()

    # Instantiate BL objects
    stats_fake_db = StatsFakeDatabase()
    data_handler_object = DataHandler()

    # Fetch global configuration
    with open('config.json', 'r') as conf:
        config = json.load(conf)

    # There is no need to .join() the threads because they never really stop running, daemon will do the job.
    for p in range(config['NUM_OF_PRODUCERS']):
        logger.info(f"Starting producer thread number {p + 1}")
        threading.Thread(target=producer, args=(queue, config['EXE_FILE_PATH']), daemon=True).start()

    for c in range(config['NUM_OF_CONSUMERS']):
        logger.info(f"Starting consumer thread number {c + 1}")
        threading.Thread(target=consumer, args=(queue, data_handler_object, stats_fake_db), daemon=True).start()

    app.run(debug=False)
