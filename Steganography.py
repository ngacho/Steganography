import numpy as np
import imageio.v2 as imageio
import glob

# looking at 1 channels
#

channels = ["Red", "Green", "Blue", "All"]


def main():
    img = imageio.imread("projectImages/Castle.png")
   
    # Potential useful TEXT on HORIZONTAL Castle.png
	#  CHANNEL: Red
	#  BIT OF SIGNIFICANCE: 1
	#  first 32 bits: 4126
	#  next 32 bits: 375741274
    


def decodeCastle():
    img = imageio.imread("projectImages/Castle.png")
    hidden_height, hidden_width = readFirst64BitsByChannelAndBySignificantBitHorizontally(img, 3, 1)
    print(hidden_height, hidden_width)

    chars = readBitsAsImagesDependingOnPositionOfSignificanceHorizontally(img, hidden_height, hidden_width)
    new_image = flipChannelBits(convertBitsIntoImage(chars, hidden_width, hidden_height))
    image_name = "hidden-images/channels_ALL_LSB_1_HORIZONTALLY_Castle.png"
    imageio.imwrite(image_name, new_image)

    hidden_image = imageio.imread(image_name)
    hidden_chars = readBitsAsTextDependingOnPositionOfSignificanceVertically(hidden_image, 9000, 1, 1)
    text = binaryToAsciiString(''.join(hidden_chars))
    file_name = "hidden-texts/channel_GREEN_LSB_1_HORIZONTAL_Castle.txt"
    writeToFile(text, file_name)

def decodeChio1():
    img = imageio.imread("projectImages/Chio1.png")
    hidden_height, hidden_width = readFirst64BitsByChannelAndBySignificantBitVertically(img, 3, 1)
    print(hidden_height, hidden_width)
    imgChars = readBitsAsImagesDependingOnPositionOfSignificanceVertically(img, hidden_height, hidden_width)
    new_image = flipChannelBits(convertBitsIntoImage(imgChars, hidden_height, hidden_width))
    image_name = "hidden-images/channels_ALL_LSB_1_VERTICALLY_Chio1.png"
    imageio.imwrite(image_name, new_image)

    headerHunter([image_name])

    # Green, lsb
    hidden_image = imageio.imread(image_name)
    hidden_chars = readBitsAsTextDependingOnPositionOfSignificanceHorizontally(hidden_image, 3000, 1, 1)
    text = binaryToAsciiString(''.join(hidden_chars))
    file_name = "hidden-texts/channel_GREEN_LSB_1_HORIZONTAL_Chio1.txt"
    writeToFile(text, file_name)

    


def readBitsAsImagesDependingOnPositionOfSignificanceHorizontally(img,  hidden_height, hidden_width, channel_num=3, posLSB=1, header_size=64):

    chars = []
    if(posLSB == 0):
         return chars

    numZeros = posLSB - 1
    
    zeros = '0' * (numZeros)
    binaryMask = '1' + zeros
    mask = int(binaryMask, 2)

    height, width, _ = img.shape
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    
    break_out_flag = False
    for r in range(height):
        for c in range(width):
            if (len(chars) < total_bits):
                if channel_num == 3:
                    # get LSB of first channel
                    chars.append(str(((img[r, c, 0] & mask) >> numZeros)))
                    chars.append(str(((img[r, c, 1] & mask) >> numZeros)))
                    chars.append(str(((img[r, c, 2] & mask) >> numZeros)))
                else:
                     chars.append(str(((img[r, c, channel_num] & mask) >> numZeros)))       
            else:
                break_out_flag = True
                break

        if break_out_flag:
            break

    return chars[header_size:]

def readBitsAsImagesDependingOnPositionOfSignificanceVertically(img,  hidden_height, hidden_width, channel_num=3, posLSB=1, header_size=64):

    chars = []
    if(posLSB == 0):
         return chars

    numZeros = posLSB - 1
    
    zeros = '0' * (numZeros)
    binaryMask = '1' + zeros
    mask = int(binaryMask, 2)

    height, width, _ = img.shape
    total_bits = (header_size-1) + (24 * hidden_height * hidden_width)
    # create a new  array to store the pixels.
    
    break_out_flag = False
    for c in range(width):
        for r in range(height):
            if (len(chars) < total_bits):
                if channel_num == 3:
                    # get LSB of first channel
                    chars.append(str(((img[r, c, 0] & mask) >> numZeros)))
                    chars.append(str(((img[r, c, 1] & mask) >> numZeros)))
                    chars.append(str(((img[r, c, 2] & mask) >> numZeros)))
                else:
                     chars.append(str(((img[r, c, channel_num] & mask) >> numZeros)))       
            else:
                break_out_flag = True
                break

        if break_out_flag:
            break

    return chars[header_size:]
    





    """
        image,
        channel_num,
        position of significant bit,
        header_size = 32

        function to read bits as text based on a channel, num, position of the significant bit, 
        reads horizontally
    """
def readBitsAsTextDependingOnPositionOfSignificanceVertically(img, textSize, channel_num=3, posLSB=1):
    chars = []
    if posLSB == 0:
        return chars

    numZeros = posLSB - 1
    
    zeros = '0' * (numZeros)
    binaryMask = '1' + zeros
    mask = int(binaryMask, 2)
    print(posLSB, '-> bin: ', binaryMask, ' :actual: ', mask)
    height, width, _ = img.shape

    break_out_flag = False
    
    for c in range(width):
        for r in range(height):
            if len(chars) < textSize:
                if channel_num == 3:
                    chars.append(str((((img[r, c, 0] & mask) >> numZeros))))
                    chars.append(str((((img[r, c, 1] & mask) >> numZeros))))
                    chars.append(str((((img[r, c, 2] & mask) >> numZeros))))
                else:
                    chars.append(str((((img[r, c, channel_num] & mask) >> numZeros))))
            else:
                break_out_flag = True
        
        if break_out_flag:
            break

    return chars


"""
        image,
        channel_num,
        position of significant bit,
        header_size = 32

        function to read bits as text based on a channel, num, position of the significant bit, 
        reads horizontally
    """
def readBitsAsTextDependingOnPositionOfSignificanceHorizontally(img, textSize, channel_num=3, posLSB=1):
    chars = []
    if posLSB == 0:
        return chars

    numZeros = posLSB - 1
    
    zeros = '0' * (numZeros)
    binaryMask = '1' + zeros
    mask = int(binaryMask, 2)
    print(posLSB, '-> bin: ', binaryMask, ' :actual: ', mask)
    height, width, _ = img.shape

    break_out_flag = False
    
    for r in range(height):
        for c in range(width):

            if len(chars) < textSize:
                if(channel_num == 3):
                    chars.append(str((((img[r, c, 0] & mask) >> numZeros))))
                    chars.append(str((((img[r, c, 1] & mask) >> numZeros))))
                    chars.append(str((((img[r, c, 2] & mask) >> numZeros))))
                else:
                    chars.append(str((((img[r, c, channel_num] & mask) >> numZeros))))
            else:
                break_out_flag = True

        if break_out_flag:
            break

    return chars



def headerHunter(files = [file for file in glob.glob("projectImages/*.png")]):
    usefulImageNotification = []
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
        text = "Potential useful TEXT on " + file_name + "\n\t CHANNEL: " + channels[channel_num] +\
            "\n\t BIT OF SIGNIFICANCE: " + str(posLSB) + "\n\t first 32 bits: " + str(innerHeight) +\
             "\n\t next 32 bits: " + str(innerWidth) + "\n\n"
        
        if innerHeight < 9000 and innerWidth < 9000:
            text = "Potential useful IMAGE on " + file_name + "\n\t CHANNEL: " + channels[channel_num] +\
            "\n\t BIT OF SIGNIFICANCE: " + str(posLSB) + "\n\t first 32 bits: " + str(innerHeight) +\
             "\n\t next 32 bits: " + str(innerWidth) + "\n\n"


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
    for c in range(width):
        for r in range(height):
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
        Given a binary string, return an ascii string
    """
def binaryToAsciiString(s):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s)//8))


    """
        Given an image, flip bits because images are weird
    """
def flipChannelBits(img):
    counter = 0
    height, width, _ = img.shape
    for r in range(height):
        for c in range(width):
            img[r, c, 0] = int(format(img[r, c, 0], '08b')[::-1], 2)
            img[r, c, 1] = int(format(img[r, c, 1], '08b')[::-1], 2)
            img[r, c, 2] = int(format(img[r, c, 2], '08b')[::-1], 2)


    return img


"""
        Given a char of bits, convert into an image.
    """
def convertBitsIntoImage(arr, height, width):

    chars = ''.join(arr)
    result = []
    starter = 0
    for c in range(len(chars)):
        if c % 8 == 0:
            x = binaryToInt(chars[starter:starter + 8])
            result.append(x)
            starter += 8

    # convert 1D array to 3D array.
    # https://stackoverflow.com/questions/32591211/convert-1d-array-to-3d-array
    return np.reshape(result, (height, width, 3)).astype(np.uint8)


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