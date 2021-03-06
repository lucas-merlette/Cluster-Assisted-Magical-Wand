#!/usr/bin/python

import os
import sys
import logging
import argparse
from random import randint

from . import DEBUG, get_debug
from .neural_network.super_neuron import SuperNeuron
from .processing.processing import Processing, Image, PIL, re

# DEBUG = get_debug()
# DEBUG = 1
LOGGER = logging.getLogger(__name__)


def get_arguments(arguments):
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-f', '--file', help='The image file to process',
                        required=True)
    parser.add_argument('-c', '--clusters', help='Number of clusters',
                        required=True)
    parser.add_argument('-d', '--debug', help='Specify debug mode (0 or 1)',
                        required=False)
    arguments = vars(parser.parse_args())

    if os.path.isfile(arguments['file']) == False:
        sys.stderr.write('FileError: Given file doesn\'t not found\n')
        parser.print_help()
        sys.exit()

    if arguments['clusters'].isdigit() == False:
        sys.stderr.write('ArgumentError: Clusters must be a number\n')
        parser.print_help()
        sys.exit()

    try:
        arguments['clusters'] = int(arguments['clusters'])
    except ValueError:
        sys.stderr.write('ArgumentError: Clusters must be a number\n')
        parser.print_help()
        sys.exit()

    if arguments['debug'] is not None:
        if arguments['debug'] not in ('0', '1'):
            parser.print_help()
            sys.exit()
        os.environ['DEBUG'] = arguments['debug']
        global DEBUG
        DEBUG = get_debug()

    return arguments


def main():
    if os.path.isfile(sys.argv[1]) == False:
        print "File [" + sys.argv[1] + "] not found!"
        return
    image = Processing(sys.argv[1])
    image.norm_data()
    ref_histogram = []
    im_size = float(image.width * image.height)
    tolerance = im_size * 0.02
    print "Image Size: " + str(im_size)
    print "Histogram of size: " + str(len(image.histogram))
    print "Tolerance of: " + str(tolerance)
    print "#############################################"
    for i in image.histogram:
        if i[1] > tolerance:
            ref_histogram.append(i)
            print i
    print "##############################################"
    for i in image.histogram:
        if i[1] != 0:
            print i

    super_neuron = SuperNeuron(image.output, (image.height, image.width), ref_histogram)
    super_neuron.merge_neurons()

#    sys.exit()

    display = []

    print "Neural Network determines: "
    print str(len(super_neuron.neurons)) + " clusters in the image"

    for neuron in super_neuron.neurons:
        cl_pxl = [(0, 0, 0)] * image.height * image.width

        for pixel in neuron.pixels:
            pos = (pixel[0] * image.width) + pixel[1]
            cl_pxl[pos] = image.ptr[pos]
        cluster = Image.new("RGB", image.main_picture.size)
        cluster.putdata(cl_pxl)
        display.append(cluster)
    for i in display:
        i.show()

### DEPRECATED
    # arguments = get_arguments(sys.argv[1:])

    # image = arguments['file']
    # number_of_clusters = arguments['clusters']

    # if DEBUG:
    #     LOGGER.info('image -> %s' % image)
    #     LOGGER.info('number_of_clusters -> %s' % number_of_clusters)

    # from .core import Core
    # core = Core(number_of_clusters)
    # core.run()
    # if DEBUG:
    #     core.info()
#    image = []
#
#    for y in range(5):
#        image.append([])
#        for x in range(5):
#            image[y].append(randint(0, 9))

#    if DEBUG:
#        print 'Displaying image:\n'
#        for y in range(len(image)):
#            for x in range(len(image[y])):
#                sys.stdout.write('%d, ' % image[y][x] if x < len(image[y]) - 1 else '%d\n' % image[y][x])
#        print '\n-----\n'

#    super_neuron = SuperNeuron(image, (5, 5), None)
#    super_neuron.merge_neighbour_neurons()

if __name__ == '__main__':
    main(sys.argv)
