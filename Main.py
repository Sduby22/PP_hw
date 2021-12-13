from src import *
import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: [%(name)s] %(message)s'
        )

if __name__ == '__main__':
    conf = ConfigLoader('./config.yaml')
    runtime = Runtime('1841232132', conf)
    interpreter = Interpreter(conf)
    interpreter.setRuntime(runtime)
    interpreter.run()
