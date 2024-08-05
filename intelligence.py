from utils import *
from matplotlib import pyplot as mpl
import numpy as np

def find_red_pixels(map_filename="./data/map.png", upper_threshold=100, lower_threshold=50):
    """
    -Locates all definitively red pixels in an image and outputs a black and white image with the red pixels from the original highlighted in white
    :params:
        =map_filename - the filepath for the image
        =thresholds - the colour to look for (i.e. red) must have a higher score than the upper threshold
            while the other 2 colour channels must have a lower score than the lower threshold in order to have
            the pixel highlighted as being definitively one colour
    :return: a 2D numpy array representing the binary image, with this written into a .jpg file
        named map-red-pixels.jpg
    """
    rgb_img = mpl.imread(map_filename) * 255
    output_file = np.zeros((len(rgb_img), len(rgb_img[0])))    #same dimensions as the image file but it is a 2D array rather than 3D as each pixel is only 1 or 0 instead of being represented by 3 colour channels and opacity
    for i in range(0, len(rgb_img)):
        for j in range(0, len(rgb_img[i])):
            #looking for red pixels
            if rgb_img[i, j][0] > upper_threshold and rgb_img[i, j][1] < lower_threshold and rgb_img[i, j][2] < lower_threshold:
                #red pixel found - pixel is to be highlighted white, so given a value of 1
                output_file[i, j] = 1   #the same pixel on the output file is located and coloured accordingly
            #if the 'if' block doesn't run, the pixel is not definitively red so it must be blacked out and have a value of 0. As the output file is instantiated as a zeros numpy array then no change is made as all the values are 0 by default
    mpl.imsave("./data/map-red-pixels.jpg", output_file, cmap='gray')
    mpl.imshow(output_file)
    return output_file

def find_cyan_pixels(map_filename="./data/map.png", upper_threshold=100, lower_threshold=50):
    """
    -Locates all definitively cyan pixels in an image and outputs a black and white image with the cyan pixels from the original highlighted in white
    :params:
        =map_filename - the filepath for the image
        =thresholds - the colour to look for (i.e. cyan) must have a higher score than the upper threshold
            while the other 2 colour channels must have a lower score than the lower threshold in order to have
            the pixel highlighted as being definitively one colour
    :return: a 2D numpy array representing the binary image, with this also being written into a .jpg file
        named map-cyan-pixels.jpg"""
    rgb_img = mpl.imread(map_filename) * 255
    output_file = np.zeros((len(rgb_img), len(rgb_img[0])))    #same dimensions as the image file but it is a 2D array rather than 3D as each pixel is only 1 or 0 instead of being represented by 3 colour channels and opacity
    for i in range(0, len(rgb_img)):
        for j in range(0, len(rgb_img[i])):
            #looking for cyan pixels
            if rgb_img[i, j][1] > upper_threshold and rgb_img[i, j][2] > upper_threshold and rgb_img[i, j][0] < lower_threshold:    #for cyan, both the green and blue colour channels need to be greater tham the upper threshold
                #cyan pixel found - pixel is to be highlighted white, so given a value of 1
                output_file[i, j] = 1   #the same pixel on the output file is located and coloured accordingly
            #if the 'if' block doesn't run, the pixel is not definitively cyan so it must be blacked out and have a value of 0. As the output file is instantiated as a zeros numpy array then no change is made as all the values are 0 by default
    mpl.imsave("./data/map-cyan-pixels.jpg", output_file, cmap='gray')
    mpl.imshow(output_file)
    return output_file

def detect_connected_components(IMG : np.ndarray):
    """
    -Find all the connected components in a binary image file (black and white) with the assumption
    of 8-adjacency (a pixel that isn't on an edge will have 8 neighbours). The algorithm below creates a duplicate of the image's binary array (called MARK) in terms of
    its dimensions and sets all values in it to 0 which represents an entirely unvisited node. The algorithm loops through the rows and columns in a nested 'for' loop 
    (in the ith row and jth column), checking if a pixel in the original binary image's array which is part of the pavement (meaning it is white in the image and has a value of 1)
    has been visited in MARK's corresponding pixel for those coordinates, i.e. in the same row and column. If it hasn't been visited, the component_id variable which is used to 
    count how many connected components there are gets incremented and the value in MARK at row i and column j is set to be the component_id instead of 0. The coordinates for this
    node are added to a queue, implemented using a 2D array. While the queue isn't empty, it means there are still nodes to check through, i.e. find the neighbours of the node we just enqueued. 
    First, we dequeue the value at the front of the queue and then we have to find the neighbours. To find the neighbours of a node N:
                    [n5][n6][n7]
                    [n4][N ][n0]
                    [n3][n2][n1]
                    if i represents row and j represents column and N is in row i and column j then this is shown as:
                    [i-1, j-1] [i-1, j] [i-1, j+1]
                    [i,   j-1] [i,   j] [i,   j+1]
                    [i+1, j-1] [i+1, j] [i+1, j+1]
    Thus, we use another set of nested 'for' loops checking the xth row and yth column in a 3x3 grid centred at the current node from the queue, checking if they have been marked in
    the MARK array. If they haven't and the corresponding pixel in the original binary image is 1 (representing a pavement), they are marked as visited with the same component_id
    as the node we are checking so that later they get grouped as the same connected component. They also get enqueued so the queue is not empty, thus the WHILE loop runs again,
    checking for the neighbours of all the original node's neighbours that are part of the pavement and eventually marking them with the same component_id. When there are no more
    neighbours which are valued as 1 in the original file, the queue is empty so the WHILE loop is exited, bringing us to the next pixel to check going from top left to bottom following
    the ith row, jth column system for coordinates. If a white pixel (1) has been marked as visited and grouped as a component in MARK then it doesn't need regrouping or its neighbours checking
    but eventually when we do come to a pixel that hasn't been put into a component and is on the pavement, we increment the component_id and perform all the checks on its neighbours using the
    localised nested 'for' loops (xth row, yth column) and the WHILE loop etc.
    Once the whole image has been scanned and connected components stored in MARK, a dictionary is then created so that we can easily find out how many pixels belong to each component. This is done
    by checking each pixel row in each column and seeing if it is not equal to 0 - if a pixel is equal to 0 in MARK then it means it wasn't highlighted so it doesn't belong to a component and thus
    doesn't need counting. If it isn't equal to 0 then it needs to be counted in the dictionary so if a key for the component that the pixel belongs to exists, this key's corresponding value is incremented
    by 1; if no key exists for this component group then a new key is established with a value of 1. This process is done until every pixel in the MARK array has been accounted for with the dictionary containing
    all the connected components and their total number of pixels. Next, the data is written to a text file located in the data directory called cc-output-2a.txt.

    It is improved and modified from the original algorithm in the way that it uniquely marks each component to each other component while also marking them all as being visited. It uses exception handling to manage
    boundary pixels so that no errors arise from trying to make comparisons on pixels that do not exist. It has a nice localised neighbour finding algorithm outlined above and below again in the code, giving more depth
    on how the algorithm works.

    :params:
        =IMG - a binary image whereby each pixel is either white (1) for pavements or black (0)
            for the background region. It is to be read as a numpy array and looped through. 
            The functions find_red_pixels and find_cyan_pixels are intended to be passed directly as the input for this function
    :return: outputs a textfile named cc-output-2a.txt which gives all the connected components found
        and the number of pixels in each component, with the last line giving the total number of connected
        components located in the image file
        -It also returns a 2D numpy array representing the connected components, MARK
    """
    image = IMG
    MARK = np.zeros((len(image), len(image[0])), dtype=int)
    Q = []   #Q needs to be a queue of coordinates for finding neighbours recursively
    component_id = 0
    for i in range(0, len(image)):
        for j in range(0, len(image[i])):
            if image[i, j] == 1 and MARK[i, j] == 0:    #if it isn't 0 then it has already been marked with another component
                component_id += 1   #by incrementing this each time, the next component's pixels will have a different value and thus easy to find all pixels that belong to the same component
                MARK[i, j] = component_id
                Q.append([i,j])
                while len(Q) != 0:
                    first_item = Q[0]
                    del Q[0]
                    '''neighbour nodes from a node N are found in the following way
                    [n5][n6][n7]
                    [n4][N ][n0]
                    [n3][n2][n1]
                    if i represents row and j represents column and N is in row i and column j then this is shown as:
                    [i-1, j-1] [i-1, j] [i-1, j+1]
                    [i,   j-1] [i,   j] [i,   j+1]
                    [i+1, j-1] [i+1, j] [i+1, j+1]
                    Some of these won't exist on the edges and corners of an image so we need to use try-except blocks to check first for neighbours
                    '''
                    for x in range(first_item[0]-1, first_item[0]+2):
                        for y in range(first_item[1]-1, first_item[1]+2):
                            try:    #runs if the pixel has 8 neighbours
                                if image[x, y] == 1 and MARK[x, y] == 0:
                                    MARK[x, y] = component_id
                                    Q.append([x,y])
                            except: #pixel is on an edge or corner so it is missing some neighbours, thus no checks can be run
                                a = 1   #filler code 
    components = get_components_as_dictionary(MARK)
    file = open("./data/cc-output-2a.txt", "w")
    for key in components:
        file.writelines(f"Connected component {key}, number of pixels = {components[key]}\n")
    file.writelines(f"Total number of connected components = {len(components)}")
    file.close()
    return MARK

def get_components_as_dictionary(MARK):
    '''
    -Gets the components in the 2D-array MARK into a dictionary format whereby each unique component is numbered and serves as a key in the dictionary, with their corresponding values being the number of pixels
        that belong to that component
    -The reason for making this a function is because both detect_connected_components and detect_connected_components_sorted need the data in a dictionary format but the data that detect_connected_components
        has to return as an output due to the specification is MARK. The input for detect_connected_components_sorted also has to be MARK due to the specification.
    :params: MARK - the 2D-numpy-array representing the connected components
    :return: a dictionary with each connected component as a key and the values being their respective number of pixels
    '''
    components = {} #need to add up all the pixels in each connected component, hence using a hashing algorithm to add them to a dictionary and incrementing each time a member of the same connecting component is found is an effective way
    for row in MARK:
        for pixel in row:
            if pixel != 0:
                if pixel not in components:
                    components[pixel] = 1
                else:
                    components[pixel] = components[pixel] + 1
    return components

def detect_connected_components_sorted(MARK):
    """reads MARK returned from detect_connected_components, writes all connected components in decreasing order into a text file cc-output-2b.txt, and
        writes the top two largest connected components into a file named as cc-top-2.jpg
    :params: MARK - the 2D numpy array representing the connected components
    :return: outputs two files - one is a text file stating the components and their number of pixels from largest to smallest and the other is an image file
        in black and white with the white representing the two largest connected components. The function itself doesn't return a value, it simply outputs two files.
    """
    components = get_components_as_dictionary(MARK)
    collection = list(zip(components.keys(), components.values()))  #zips up the dictionary's key-value pairs in a list
    sorted_by_size = bubble_sort(collection, True, 1, False)   #applies bubble sort on the zipped up list of key-value pairs from the dictionary, using each pair's values to make the comparisons; the fourth parameter is false as we know the list only contains numbers so we don't need to waste time searching for non-numerical values and removing them
    top_two_components = [sorted_by_size[-1][0], sorted_by_size[-2][0]]     #gets the IDs of the two largest components - originally the keys in the dictionary
    print(top_two_components)
    file = open("./data/cc-output-2b.txt", "w")
    for i in range(len(sorted_by_size)-1, -1, -1):
        file.writelines(f"Connected component {sorted_by_size[i][0]}, number of pixels = {sorted_by_size[i][1]}\n")
    file.close()
    for i in range(0, len(MARK)):
        for j in range(0, len(MARK[0])):
            if MARK[i, j] in top_two_components:
                MARK[i, j] = 1
            else:
                MARK[i, j] = 0
    mpl.imsave("./data/cc-top-2.jpg", MARK, cmap='gray')