import numpy as np
import imageio.v2 as imageio
import glob

# looking at 1 channels
#

channels = ["Red", "Green", "Blue", "All"]


def main():
    print("Hello world")


def writeToFile(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    main()