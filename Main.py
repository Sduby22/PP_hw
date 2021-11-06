from src.ConfigLoader import *
from src.RunPy import * 

logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: [%(name)s] %(message)s'
        )

if __name__ == '__main__':
    a = ConfigLoader()
    a.load('./config.yaml')
    runpy = getInstance()
    runpy.init(a)

