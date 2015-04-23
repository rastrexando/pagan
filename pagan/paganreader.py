import math

DEBUG = True



# This screams for an auxiliuary module.
OCTET_LENGTH = 4
MAX_DIGIT = 255

fixed_pixel = 'o'
optional_pixel = '+'

# TODO: Split into two methods - Finding fixed pixels and optional pixels?
# Less efficient but does not damage my brain. Or generate a tupel of two lists in a seperate method
# and handle them differently.
def parsepaganfile(filename, ip):
    fd = open(filename, 'r')

    drawmap = []
    optmap = []

    i = 0
    for line in fd:
        j = 0
        for char in line:
            if (char == fixed_pixel):
                drawmap.append((i - 1, j - 1))
            if (char == optional_pixel):
                optmap.append((i - 1, j - 1))
            j += 1
        i += 1

    fd.close()

    # TODO: Decide for each optional pixel to be displayed
    # in respect of the optmap-size and an the third ip octet.
    # Merge the result with drawmap.
    print (optmap)
    print (len(optmap))

    extmap = decideoptionalpixels(optmap, ip)

    return sorted(drawmap + extmap)


# Use one of the octets to determine if a pixel is shown or not.
def decideoptionalpixels(optmap, ip):
    # At least four optional pixels are expected. One
    # for each ip octet. If there are less, there is
    # only one chunk to handle.
    #if (len(optmap) >= 4):

    resmap = []
    chunksize = int(math.ceil(len(optmap) / float(OCTET_LENGTH)))
    #else:
    #    chunksize = 1
    #
    #print (int(math.ceil(len(optmap) / 4.0)))

    # Split the given IP4 adress into octets.
    octets = ip.split('.')

    i = 0

    # For each octet in the ip address, split the
    # optional pixels in smaller chunks. Base the
    # decision to draw them on each different octet.
    for oct in octets:
        chunk = optmap[i:i + chunksize]
        oct = int(oct)
        # Decide for each chunk which pixels are drawn.
        resmap += decidechunk(chunk, oct)
        i += chunksize


    return resmap

# Decides for each chunk if its pixels should be drawn
# based on its octet.
def decidechunk(chunk, octet):
    # Debug message
    if DEBUG:
        print ("Chunk: %r     Octet: %r" % (chunk, octet))
    chunkresult = []
    # i = 1
    for pixel in chunk:
        #print (len(chunk))
        pixelval = pixel[0] + pixel[1]

        # Make sure the pixel values do not outclass the resolution.
        # This wont take effect on the odd or even outcome.
        currentmax = 1000 + octet
        # When pixel values are still bigger add another padding
        # even if the initial version of pagan will be stuck to 16x16.
        if (pixelval > currentmax):
            currentmax += 1000
        # Throw the current pixels values in the mix.
        decider = currentmax / pixelval
        # An even result will have the pixel to be drawn.
        if ((decider % 2) == 0):
            chunkresult.append(pixel)

        # Debug message
        if DEBUG:
            print ("This is what happened: Decider %r  Result: %r" % (decider, (decider % 2)))

    return chunkresult


# Returns the highest of the ip's octets.
def get_max_octet(ip):
    octets = ip.split('.')
    max = 0
    for oct in octets:
        if oct >= max:
            max = oct
    return max




if __name__ == "__main__" :

    filename = 'example_weapon_short.pgn'


    # Test: None optional pixels are drawn with this address.
    ip = "113.227.182.122"

    # Test: All optional pixels are drawn with this address.
    # ip = "98.12.255.10"

    dmap = parsepaganfile(filename, ip)

    print ("Drawmap: %r" %dmap)
