import pygame
import numpy

chunk_size = 16
block_size = 30
pixel_total = chunk_size*block_size
adj_cwods = [(0,0)]*56
chunk_book = {}

#cwods in this module refer to the top left pixel of each chunk's world origin distance. Thus, cwod[0] refers to the latitude of a chunk, while cwod[1] refers to the altitude.
#This code detects which chunks need to be generated based on the top-left pixels' locations
def det_adj_cwods(wod):
    cwod = wod[0]//pixel_total*pixel_total,-wod[1]//pixel_total*pixel_total
    chunk_lon = cwod[0]
    chunk_lat = cwod[1]
    adj_cwods[0] = chunk_lon-3*pixel_total,chunk_lat-3*pixel_total
    adj_cwods[1] = chunk_lon-3*pixel_total,chunk_lat-2*pixel_total
    adj_cwods[2] = chunk_lon-3*pixel_total,chunk_lat-pixel_total
    adj_cwods[3] = chunk_lon-3*pixel_total,chunk_lat
    adj_cwods[4] = chunk_lon-3*pixel_total,chunk_lat+pixel_total
    adj_cwods[5] = chunk_lon-3*pixel_total,chunk_lat+2*pixel_total
    adj_cwods[6] = chunk_lon-3*pixel_total,chunk_lat+3*pixel_total

    adj_cwods[7] = chunk_lon-2*pixel_total,chunk_lat-3*pixel_total
    adj_cwods[8] = chunk_lon-2*pixel_total,chunk_lat-2*pixel_total
    adj_cwods[9] = chunk_lon-2*pixel_total,chunk_lat-pixel_total
    adj_cwods[10] = chunk_lon-2*pixel_total,chunk_lat
    adj_cwods[11] = chunk_lon-2*pixel_total,chunk_lat+pixel_total
    adj_cwods[12] = chunk_lon-2*pixel_total,chunk_lat+2*pixel_total
    adj_cwods[13] = chunk_lon-2*pixel_total,chunk_lat+3*pixel_total

    adj_cwods[14] = chunk_lon-pixel_total,chunk_lat-3*pixel_total
    adj_cwods[15] = chunk_lon-pixel_total,chunk_lat-2*pixel_total
    adj_cwods[16] = chunk_lon-pixel_total,chunk_lat-pixel_total
    adj_cwods[17] = chunk_lon-pixel_total,chunk_lat
    adj_cwods[18] = chunk_lon-pixel_total,chunk_lat+pixel_total
    adj_cwods[19] = chunk_lon-pixel_total,chunk_lat+2*pixel_total
    adj_cwods[20] = chunk_lon-pixel_total,chunk_lat+3*pixel_total

    adj_cwods[21] = chunk_lon,chunk_lat-3*pixel_total
    adj_cwods[22] = chunk_lon,chunk_lat-2*pixel_total
    adj_cwods[23] = chunk_lon,chunk_lat-pixel_total
    adj_cwods[24] = chunk_lon,chunk_lat
    adj_cwods[25] = chunk_lon,chunk_lat+pixel_total
    adj_cwods[26] = chunk_lon,chunk_lat+2*pixel_total
    adj_cwods[27] = chunk_lon,chunk_lat+3*pixel_total

    adj_cwods[28] = chunk_lon+pixel_total,chunk_lat-3*pixel_total
    adj_cwods[29] = chunk_lon+pixel_total,chunk_lat-2*pixel_total
    adj_cwods[30] = chunk_lon+pixel_total,chunk_lat-pixel_total
    adj_cwods[31] = chunk_lon+pixel_total,chunk_lat
    adj_cwods[32] = chunk_lon+pixel_total,chunk_lat+pixel_total
    adj_cwods[33] = chunk_lon+pixel_total,chunk_lat+2*pixel_total
    adj_cwods[34] = chunk_lon+pixel_total,chunk_lat+3*pixel_total

    adj_cwods[35] = chunk_lon+2*pixel_total,chunk_lat-3*pixel_total
    adj_cwods[36] = chunk_lon+2*pixel_total,chunk_lat-2*pixel_total
    adj_cwods[37] = chunk_lon+2*pixel_total,chunk_lat-pixel_total
    adj_cwods[38] = chunk_lon+2*pixel_total,chunk_lat
    adj_cwods[39] = chunk_lon+2*pixel_total,chunk_lat+pixel_total
    adj_cwods[40] = chunk_lon+2*pixel_total,chunk_lat+2*pixel_total
    adj_cwods[41] = chunk_lon+2*pixel_total,chunk_lat+3*pixel_total

    adj_cwods[42] = chunk_lon+3*pixel_total,chunk_lat-3*pixel_total
    adj_cwods[43] = chunk_lon+3*pixel_total,chunk_lat-2*pixel_total
    adj_cwods[44] = chunk_lon+3*pixel_total,chunk_lat-pixel_total
    adj_cwods[45] = chunk_lon+3*pixel_total,chunk_lat
    adj_cwods[46] = chunk_lon+3*pixel_total,chunk_lat+pixel_total
    adj_cwods[47] = chunk_lon+3*pixel_total,chunk_lat+2*pixel_total
    adj_cwods[48] = chunk_lon+3*pixel_total,chunk_lat+3*pixel_total
    
    adj_cwods[49] = chunk_lon+4*pixel_total,chunk_lat-3*pixel_total
    adj_cwods[50] = chunk_lon+4*pixel_total,chunk_lat-2*pixel_total
    adj_cwods[51] = chunk_lon+4*pixel_total,chunk_lat-pixel_total
    adj_cwods[52] = chunk_lon+4*pixel_total,chunk_lat
    adj_cwods[53] = chunk_lon+4*pixel_total,chunk_lat+pixel_total
    adj_cwods[54] = chunk_lon+4*pixel_total,chunk_lat+2*pixel_total
    adj_cwods[55] = chunk_lon+4*pixel_total,chunk_lat+3*pixel_total
    
#MY NEXT STEP IS TO SWITCH THE NAMING SYSTEM HERE. I want to make it so that the temp_ prefix refers to chunks that are currently sampling randomly. The chunk_arrays will start as empty arrays that are then written into after the temp_chunk_arrays go through filtering methods. I think this will make the code more readable, and hopefully easier to debug.
def gen_chunk(cwod): #generate a chunk, given its top left pixel location (I need to change it so that gas forms in blobs, some ores can be found appearing in veins, and the base element always gets placed instead of nothing.)
    #chunk_lon = cwod[0]
    chunk_lat = cwod[1]
    temp_chunk_array = numpy.random.random_integers(0,numpy.random.random_integers(1,48)*10,size=(chunk_size,chunk_size)) #the 48 here is intended to represent the number of different elements (oneium, twoium, etc.) I want to have. These elements are randomly sampled, then filtered based on the latitude of the chunk, so that heavier elements don't show up too high in the world.
    temp_right_chunk_array = numpy.random.random_integers(0,numpy.random.random_integers(1,48)*10,size=(chunk_size,chunk_size))
    temp_left_chunk_array = numpy.random.random_integers(0,numpy.random.random_integers(1,48)*10,size=(chunk_size,chunk_size))
    right_chunk_updated = False
    left_chunk_updated = False
    chunk_array = numpy.zeros((chunk_size,chunk_size))
    right_chunk_array = numpy.zeros((chunk_size,chunk_size))
    left_chunk_array = numpy.zeros((chunk_size,chunk_size))
    biome_stability = 8 #This number allows a world to be built with varying biome randomness-stability. Higher numbers indicate higher biome stability, since a greater range is sampled, and only numbers attributed to a coded element can become chunks. All others default to the latitudinal gradient filter (explained below).

    if cwod not in chunk_book:
        if chunk_lat >= 0: #this conditional is used to keep the world separated between sky and ground
            chunk_type = numpy.random.random_integers(0,4*biome_stability) #This ensures that some chunks on any latitude can be comprised of any element. It is the random longitudinal biome generator. The 3 should represent the number of elements that have been coded.
            if chunk_type != 3: #currently this will always be called. Later, I'll make biomes.
                chunk_base_element = max(1,min(4,chunk_lat//5000)) #This is the latitudinal gradient filter. Having every chunk totally unique is rather odd. But having no unique chunks is rather boring. It only gets called when the longitudinal biome generator picks a number outside a certain range determined by the biome_stability. Currently, for every 5000 pixels traveled, the chunk_base_element increases by one, though it can be no smaller than 1.
            else:
                chunk_base_element = chunk_type-1

            #Hill generation
            for row in range(chunk_size):
                for column in range(chunk_size):
                    if temp_chunk_array[row,column] in [0,1]: #checking for 1 is arbitrary. It doesn't code for an element, so it's nice to have it act as a hill-seed. It also makes it so that, as more and heavier elements are sampled, the hill count should go down considerably, which sort of imitates the real world.
                        #I don't understand why the following line puts random blocks all over the place, instead of just at the tip of each hill, but it does. The rest of the function works fine without it. But I'm leaving it in the code because one day I'd like to know the answer.
                        #chunk_array[row,column] = 1
                        plateu_len = numpy.random.random_integers(0,chunk_size/8) #This randomly samples for hill-heights based on how large the last plateu level should be, imagining that hills are made up of a stack of plateus.
                        plateu_len_inc = 0
                        #The following code creates varying levels of plateus to create realistic hills.
                        for row_rem_below in range(chunk_size-row):
                            plateu_len = plateu_len + plateu_len_inc
                            plateu_len_inc = 0
                            for column_rem_right in range(plateu_len):
                                if column+column_rem_right <= chunk_size-1:
                                    chunk_array[row+row_rem_below,column+column_rem_right] = chunk_base_element
                                    plateu_len_inc = 1
                                else:
                                    right_chunk_array[row+row_rem_below,column+column_rem_right-chunk_size] = chunk_base_element
                                    plateu_len_inc = 1
                                    right_chunk_updated = True
                            for column_rem_left in range(plateu_len):
                                if column-column_rem_left >= 0:
                                    chunk_array[row+row_rem_below,column-column_rem_left] = chunk_base_element
                                    plateu_len_inc = 1
                                else:
                                    left_chunk_array[row+row_rem_below,column-column_rem_left+chunk_size] = chunk_base_element
                                    plateu_len_inc = 1
                                    left_chunk_updated = True

        #Following is the generation code for sky chunks:
        elif chunk_lat < 0 and chunk_lat > -10000:
            for row in range(chunk_size):
                for column in range(chunk_size):
                    chunk_array[row,column] = 0
            
        elif chunk_lat < -10000: #This will be for space chunks eventually.
            for row in range(chunk_size):
                for column in range(chunk_size):
                    if chunk_array[row,column] not in [0,1,2,3,4]:
                        chunk_array[row,column] = 0

        if chunk_lat > 0:
            for row in range(chunk_size):
                for column in range(chunk_size):
                    #Water generation
                    if temp_chunk_array[row,column] == 3: #checking for 1 as a water-seed is also arbitrary. In reality, the chunk will be re-checked for randomness later on.
                        temp_chunk_array[row,column] = 3
                        chunk_array[row,column] = 3
                        water_len = numpy.random.random_integers(0,chunk_size/4) #This randomly samples for hill-heights based on how large the last plateu level should be, imagining that hills are made up of a stack of plateus.
                        water_len_dec = 0
                        #The following code creates varying levels of water depth to create realistic pools.
                        for row_rem_below in range(chunk_size-row):
                            water_len = water_len - water_len_dec  #this is the line that says water gets smaller
                            water_len_dec = 0
                            for column_rem_right in range(water_len):
                                if column+column_rem_right <= chunk_size-1:
                                    chunk_array[row+row_rem_below,column+column_rem_right] = 3
                                    water_len_dec = 1
                                else:
                                    right_chunk_array[row+row_rem_below,column+column_rem_right-chunk_size] = 3
                                    water_len_dec = 1
                                    right_chunk_updated = True
                            for column_rem_left in range(water_len):
                                if column-column_rem_left >= 0:
                                    chunk_array[row+row_rem_below,column-column_rem_left] = 3
                                    water_len_dec = 1
                                else:
                                    left_chunk_array[row+row_rem_below,column-column_rem_left+chunk_size] = 3
                                    water_len_dec = 1
                                    left_chunk_updated = True    
                    #Eventually, instead of having all of this code, I want to have each element that shows up become a potential seed for a deposit, pocket, or layer.
                    if chunk_array[row,column] == 0:
                        chunk_array[row,column] = chunk_base_element
                    if temp_chunk_array[row,column] in [1,2,4]:
                        chunk_array[row,column] = temp_chunk_array[row,column]
                    if right_chunk_array[row,column] == 0:
                        right_chunk_array[row,column] = chunk_base_element
                    if temp_right_chunk_array[row,column] in [1,2,4]:
                        right_chunk_array[row,column] = temp_right_chunk_array[row,column]
                    if left_chunk_array[row,column] == 0:
                        left_chunk_array[row,column] = chunk_base_element
                    if temp_left_chunk_array[row,column] in [1,2,4]:
                        left_chunk_array[row,column] = temp_left_chunk_array[row,column]

        chunk_book[cwod] = chunk_array

    if right_chunk_updated and (cwod[0]+pixel_total,cwod[1]) in chunk_book:
        chunk = chunk_book[(cwod[0]+pixel_total, cwod[1])]
        numpy.copyto(chunk, right_chunk_array, where=(right_chunk_array > 0))
    elif right_chunk_updated:
        chunk_book[(cwod[0]+pixel_total, cwod[1])] = right_chunk_array.copy()

    if left_chunk_updated and (cwod[0]-pixel_total,cwod[1]) in chunk_book:
        chunk = chunk_book[(cwod[0]-pixel_total, cwod[1])]
        numpy.copyto(chunk, left_chunk_array, where=(left_chunk_array > 0)) 
    elif left_chunk_updated:
        chunk_book[(cwod[0]-pixel_total, cwod[1])] = left_chunk_array.copy()

def make_chunks(wod,display):
    det_adj_cwods(wod)
    block_rects = {}
    block_rects['solid'] = {'all':[],'oneium':[],'twoium':[]}
    block_rects['liquid'] = {'all':[]}
    block_rects['gas'] = {'all':[]}
    #example of this construction: block_rects = {'solid':{'all':[<rect(0,0,30,30)>,...],'oneium':[<rect(0,0,30,30)>]},...}
    for adj_cwod in range(len(adj_cwods)):
        gen_chunk(adj_cwods[adj_cwod]) #create chunk arrays for all empty chunks within the adjacent range
        chunk_array = chunk_book[adj_cwods[adj_cwod]] #access each chunk_array within the chunk_book dictionary
        cloc = (adj_cwods[adj_cwod][0] - wod[0],adj_cwods[adj_cwod][1] + wod[1]) #translate all the arrays as you move

        #Create the actual blocks from the chunk recorded in the dictionary.
        for column in range(chunk_size):
            for row in range(chunk_size):
                block_value = chunk_array[row,column]
                block_loc = (int(cloc[0] + column * block_size),int(cloc[1] + row * block_size))
                block_rect = pygame.Rect(block_loc[0],block_loc[1],block_size,block_size)

                if block_value in [1,2]:
                    block_rects['solid']['all'].append(block_rect)
                    if block_value == 1:
                        block_rects['solid']['oneium'].append(block_rect)
                    elif block_value == 2:
                        block_rects['solid']['twoium'].append(block_rect)
                elif block_value == 3:
                    block_rects['liquid']['all'].append(block_rect)
                elif block_value == 4:
                    block_rects['gas']['all'].append(block_rect)
    return block_rects

def draw_chunks(block_rects,display):
    for block_rect in block_rects['solid']['oneium']:
        pygame.draw.rect(display, (10,255,30),block_rect)
    for block_rect in block_rects['solid']['twoium']:
        pygame.draw.rect(display, (100,120,120),block_rect)
    for block_rect in block_rects['liquid']['all']:
        pygame.draw.rect(display, (10,30,255),block_rect)
    for block_rect in block_rects['gas']['all']:
        pygame.draw.rect(display, (100,100,10),block_rect)