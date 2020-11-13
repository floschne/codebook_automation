import tempfile

import pytest
import tensorflow as tf

from backend import Trainer
from logger import backend_logger


@pytest.fixture
def trainer():
    return Trainer()


def test_redirect_output(trainer: Trainer):
    log_file = tempfile.NamedTemporaryFile(delete=False)
    buffer = open(log_file.name, 'w')

    inout = ["Hello World!",
             "Hello Info!",
             "Hello Warning!",
             "Hello Error!",
             "Hello Info from Tensorflow!",
             "Hello Warning from Tensorflow!",
             "Hello Error from Tensorflow!"]

    @trainer.redirect_output(buffer)
    def print_fn():
        print(inout[0])

    @trainer.redirect_output(buffer)
    def log_fn():
        backend_logger.info(inout[1])
        backend_logger.warning(inout[2])
        backend_logger.error(inout[3])

        tf.get_logger().info(inout[4])
        tf.get_logger().warning(inout[5])
        tf.get_logger().error(inout[6])

    print_fn()
    log_fn()

    print("Hello to stdout")
    backend_logger.info("Hello to stdout")
    backend_logger.warning("Hello to stdout")
    backend_logger.error("Hello to stdout")
    tf.get_logger().info("Hello to stdout")
    tf.get_logger().warning("Hello to stdout")
    tf.get_logger().error("Hello to stdout")

    file_lines = log_file.read().splitlines()
    file_lines = [line.decode('utf-8') for line in file_lines]

    assert inout == file_lines

    buffer.close()
    log_file.close()
