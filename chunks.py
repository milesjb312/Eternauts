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
    
def gen_chunk(cwod): #generate a chunk, given its top left pixel location
    chunk_lon = cwod[0]
    chunk_lat = cwod[1]
    chunk_array = numpy.random.poisson(.005,size=(chunk_size,chunk_size))
    right_chunk_array = None
    left_chunk_array = None
    if cwod not in chunk_book:
        if chunk_lat == 0:
            right_chunk_array = numpy.zeros((chunk_size,chunk_size))
            left_chunk_array = numpy.zeros((chunk_size,chunk_size))
            chunk_type = numpy.random.random_integers(0,10)
            for row in range(chunk_size):
                for column in range(chunk_size):
                    if chunk_array[row,column] == 1:
                        #Following is the generation code for ground-level chunks:
                        for rows_rem in range(chunk_size): #this calculates how far out a hill should be generated
                            right_row = row + rows_rem #this is how far to the right the hill should extend
                            right_column = column + rows_rem #this is how far down the hill should extend
                            right_height = chunk_size-right_row
                            if right_row < chunk_size:
                                if 0 < right_column < chunk_size:
                                    chunk_array[right_row,right_column] = 2
                                    for height in range(right_height):
                                        chunk_array[right_row+height,right_column] = 2
                                elif right_column >= chunk_size:
                                    right_chunk_array[right_row,right_column-chunk_size] = 2
                                    for height in range(right_height):
                                        right_chunk_array[right_row-chunk_size+height,right_column-chunk_size] = 2
                        for rows_rem in range(chunk_size):
                            left_row = row + rows_rem
                            left_column = column - rows_rem
                            left_height = chunk_size - left_row
                            if left_row < chunk_size:
                                if 0 <= left_column < chunk_size:
                                    chunk_array[left_row,left_column] = 2
                                    for height in range(left_height):
                                        chunk_array[left_row+height,left_column] = 2
                                elif left_column < 0:
                                    left_chunk_array[left_row,left_column] = 2
                                    for height in range(left_height):
                                        left_chunk_array[left_row+height,left_column] = 2
            
        #Following is the generation code for sky chunks:
        elif chunk_lat < 0 and chunk_lat > -10000:
            for row in range(chunk_size):
                for column in range(chunk_size):
                    chunk_array[row,column] = 1
            
        elif chunk_lat > 0:
            chunk_type = numpy.random.random_integers(0,3)
            if chunk_type == 0:
                chunk_array = numpy.array([(numpy.full((chunk_size),2)) for _ in range(chunk_size)])
            elif chunk_type == 1:
                #right_chunk_array = numpy.zeros((chunk_size,chunk_size))
                #left_chunk_array = numpy.zeros((chunk_size,chunk_size))
                for row in range(chunk_size):
                    for column in range(chunk_size):
                        if chunk_array[row,column] == 1:
                            chunk_array[row,column] = 3
                            water_len = numpy.random.random_integers(0,chunk_size/4)
                            if row <= column:
                                for row_rem_above in range(row+1):
                                    if column+water_len <= chunk_size-1 and column-water_len >=0:
                                        water_len+=1
                                    else:
                                        break
                                    for column_rem_right in range(water_len):
                                        chunk_array[row-row_rem_above,column+column_rem_right] = 3
                                    for column_rem_left in range(water_len):
                                        chunk_array[row-row_rem_above,column-column_rem_left] = 3

                            else:
                                for row_rem_above in range(row+1):
                                    if column+water_len <= chunk_size-1 and column-water_len >=0:
                                        water_len+=1
                                    else:
                                        break
                                    for column_rem_right in range(water_len):
                                        chunk_array[row-row_rem_above,column+column_rem_right] = 3
                                    for column_rem_left in range(water_len):
                                        chunk_array[row-row_rem_above,column-column_rem_left] = 3
                
                for row in range(chunk_size):
                    for column in range(chunk_size):
                        if chunk_array[row,column] != 3:
                            chunk_array[row,column] = 2
                
            else:
                chunk_array = numpy.random.random_integers(0,10,size=(chunk_size,chunk_size))
                for row in range(chunk_size):
                    for column in range(chunk_size):
                        if chunk_array[row,column] != 5:
                            chunk_array[row,column] = 2

        print(f'{chunk_array}')
        chunk_book[cwod] = chunk_array

    if right_chunk_array is not None and (cwod[0]+pixel_total,cwod[1]) in chunk_book:
        chunk = chunk_book[(cwod[0]+pixel_total, cwod[1])]
        numpy.copyto(chunk, right_chunk_array, where=(right_chunk_array > 0))
    elif right_chunk_array is not None:
        chunk_book[(cwod[0]+pixel_total, cwod[1])] = right_chunk_array.copy()

    if left_chunk_array is not None and (cwod[0]-pixel_total,cwod[1]) in chunk_book:
        chunk = chunk_book[(cwod[0]-pixel_total, cwod[1])]
        numpy.copyto(chunk, left_chunk_array, where=(left_chunk_array > 0))
    elif left_chunk_array is not None:
        chunk_book[(cwod[0]-pixel_total, cwod[1])] = left_chunk_array.copy()

def make_chunks(wod,display):
    det_adj_cwods(wod)
    block_rects = {}
    block_rects['solid'] = {'all':[],'oneium':[],'twoium':[]}
    block_rects['liquid'] = {'all':[]}
    block_rects['gas'] = {'all':[]}
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

                if block_value in [2,5]:
                    block_rects['solid']['all'].append(block_rect)
                    if block_value == 2:
                        block_rects['solid']['oneium'].append(block_rect)
                    else:
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
        pygame.draw.rect(display, (10,20,10),block_rect)