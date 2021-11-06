from src.Runtime import *
import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: [%(name)s] %(message)s'
        )

if __name__ == '__main__':
    runtime = Runtime(config = './config.yaml')
