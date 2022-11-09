import numpy as np
import imageio.v2 as imageio
import glob

# looking at 1 channels
#

channels = ["Red", "Green", "Blue", "All"]


def main():
    headerHunter()



def headerHunter():
    usefulImageNotification = []
    files = [file for file in glob.glob("projectImages/*.png")]
    for file_name in files:
        try:
            img = imageio.imread(file_name)

            # num channels
            for i in range(8):
                for j in range(4):
                    
                    horizontalHeaderHeight, horizontalHeaderWidth = readFirst64BitsByChannelAndBySignificantBitHorizontally(img, j, i)
                    file_title = "HORIZONTAL " + file_name.split('/')[1]
                    text = notifyOfUsefulBasicHeaders(horizontalHeaderHeight, horizontalHeaderWidth, j, i, file_title)
                    if(len(text) > 0):
                        usefulImageNotification.append(text)

                    verticalHeaderHeight, verticalHeaderWidth = readFirst64BitsByChannelAndBySignificantBitVertically(img, j, i)
                    file_title = "VERTICAL " + file_name.split('/')[1]
                    text = notifyOfUsefulBasicHeaders(verticalHeaderHeight, verticalHeaderWidth, j, i, file_title)
                    if(len(text) > 0):
                        usefulImageNotification.append(text)

        except Exception as err:
            print(err)

    writeToFile(''.join(usefulImageNotification), "hidden-texts/images-metadata.txt")


    """
        This method is given a height,
        width, 
        channel number, 
        position of significant bit 
        and 
        file name

        It then notifies us if there's useful information 
        in that channel number and significant bit.
    """
def notifyOfUsefulBasicHeaders(innerHeight, innerWidth, channel_num, posLSB, file_name):
    text = ""
    if (innerHeight > 0 and innerHeight < 9000) or (innerWidth > 0 and innerWidth < 9000):
        text = "Potential useful TEXT on " + file_name + " CHANNEL: " + channels[channel_num] +\
            " BIT OF SIGNIFICANCE: " + str(posLSB) + " height: " + str(innerHeight) +\
             " width: " + str(innerWidth) + "\n"
        
        if innerHeight < 9000 and innerWidth < 9000:
            text = "Potential useful IMAGE on " + file_name + " CHANNEL: " + channels[channel_num] +\
            " BIT OF SIGNIFICANCE: " + str(posLSB) + " height: " + str(innerHeight) +\
             " width: " + str(innerWidth) + "\n"


    return text

    """
        img, image whose header's we're trying to read
        channel, the channel from which we want to read
        posLSB, position of the least significant bit we want to read

        Reads the first 64 bits of an image depending on channel and pos of lsb

        left to right
    """
def readFirst64BitsByChannelAndBySignificantBitHorizontally(img, channel, posLSB, header_size=64):
    if(posLSB == 0):
        return 0, 0

    numZeros = posLSB - 1
    
    zeros = '0' * (numZeros)
    binaryMask = '1' + zeros
    mask = int(binaryMask, 2)

    height, width, _ = img.shape
    image_metadata = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(image_metadata) < header_size:

                if(channel == 3):
                    image_metadata.append(str(((img[r, c, 0] & mask) >> numZeros)))
                    image_metadata.append(str(((img[r, c, 1] & mask) >> numZeros)))
                    image_metadata.append(str(((img[r, c, 2] & mask) >> numZeros)))
                else:
                    image_metadata.append(str(((img[r, c, channel] & mask) >> numZeros)))

            else:
                break_out_flag = True
                break

        if break_out_flag:
            break


    image_metadata = ''.join(image_metadata)[0:header_size]
    height, width = binaryToInt(
        image_metadata[:header_size//2]), binaryToInt(image_metadata[header_size//2:])

    return height, width


    """
        img, image whose header's we're trying to read
        channel, the channel from which we want to read
        posLSB, position of the least significant bit we want to read

        Reads the first 64 bits of an image depending on channel and pos of lsb

        left to right
    """
def readFirst64BitsByChannelAndBySignificantBitVertically(img, channel, posLSB, header_size=64):
    if(posLSB == 0):
        return 0, 0

    numZeros = posLSB - 1
    
    zeros = '0' * (numZeros)
    binaryMask = '1' + zeros
    mask = int(binaryMask, 2)

    height, width, _ = img.shape
    image_metadata = []
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if len(image_metadata) < header_size:

                if(channel == 3):
                    image_metadata.append(str(((img[r, c, 0] & mask) >> numZeros)))
                    image_metadata.append(str(((img[r, c, 1] & mask) >> numZeros)))
                    image_metadata.append(str(((img[r, c, 2] & mask) >> numZeros)))
                else:
                    image_metadata.append(str(((img[r, c, channel] & mask) >> numZeros)))

            else:
                break_out_flag = True
                break

        if break_out_flag:
            break


    image_metadata = ''.join(image_metadata)[0:header_size]
    height, width = binaryToInt(
        image_metadata[:header_size//2]), binaryToInt(image_metadata[header_size//2:])

    return height, width


    """
        Given a binary array, return an int
    """
def binaryToInt(binaryArray):
    return int(''.join(binaryArray), 2)

    """
        Given a text, write to a file of that file name.
    """
def writeToFile(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    main()