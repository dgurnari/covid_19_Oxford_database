import numpy as np
import pandas as pd

from sys import argv


if __name__ == "__main__":
    if len(argv) < 4:
        raise ValueError('please specify in which variable do you want to aggregate [V2, V256, V256B, V256C]')

    WVS_path = ""
