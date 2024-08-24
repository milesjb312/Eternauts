import pygame
import numpy
import player_mod
import display_mod
window_shiftx = display_mod.window_shiftx
window_shifty = display_mod.window_shifty
chunk_size = 16
block_size = 30
pixel_total = chunk_size*block_size
adj_cwods = [(0,0)]*56
chunk_book = {}
matter_list = []

#Element colors:
zeroium = (0,0,0)
oneium = (10,255,30)
twoium = (100,120,120)
threeium = (10,30,255)
fourium = (100,100,10)
color_dict = {'0':zeroium,'1':oneium,'2':twoium,'3':threeium,'4':fourium}

#cwods in this module refer to the top left pixel of each chunk's world origin distance. Thus, cwod[0] refers to the latitude of a chunk, while cwod[1] refers to the altitude.
#This code detects which chunks need to be generated based on the top-left pixels' locations
def det_adj_cwods(wod):
    cwod = wod[0]//pixel_total*pixel_total,-wod[1]//pixel_total*pixel_total
    adj_cwods[0] = cwod[0]-3*pixel_total,cwod[1]-3*pixel_total
    adj_cwods[1] = cwod[0]-3*pixel_total,cwod[1]-2*pixel_total
    adj_cwods[2] = cwod[0]-3*pixel_total,cwod[1]-pixel_total
    adj_cwods[3] = cwod[0]-3*pixel_total,cwod[1]
    adj_cwods[4] = cwod[0]-3*pixel_total,cwod[1]+pixel_total
    adj_cwods[5] = cwod[0]-3*pixel_total,cwod[1]+2*pixel_total
    adj_cwods[6] = cwod[0]-3*pixel_total,cwod[1]+3*pixel_total

    adj_cwods[7] = cwod[0]-2*pixel_total,cwod[1]-3*pixel_total
    adj_cwods[8] = cwod[0]-2*pixel_total,cwod[1]-2*pixel_total
    adj_cwods[9] = cwod[0]-2*pixel_total,cwod[1]-pixel_total
    adj_cwods[10] = cwod[0]-2*pixel_total,cwod[1]
    adj_cwods[11] = cwod[0]-2*pixel_total,cwod[1]+pixel_total
    adj_cwods[12] = cwod[0]-2*pixel_total,cwod[1]+2*pixel_total
    adj_cwods[13] = cwod[0]-2*pixel_total,cwod[1]+3*pixel_total

    adj_cwods[14] = cwod[0]-pixel_total,cwod[1]-3*pixel_total
    adj_cwods[15] = cwod[0]-pixel_total,cwod[1]-2*pixel_total
    adj_cwods[16] = cwod[0]-pixel_total,cwod[1]-pixel_total
    adj_cwods[17] = cwod[0]-pixel_total,cwod[1]
    adj_cwods[18] = cwod[0]-pixel_total,cwod[1]+pixel_total
    adj_cwods[19] = cwod[0]-pixel_total,cwod[1]+2*pixel_total
    adj_cwods[20] = cwod[0]-pixel_total,cwod[1]+3*pixel_total

    adj_cwods[21] = cwod[0],cwod[1]-3*pixel_total
    adj_cwods[22] = cwod[0],cwod[1]-2*pixel_total
    adj_cwods[23] = cwod[0],cwod[1]-pixel_total
    adj_cwods[24] = cwod[0],cwod[1]
    adj_cwods[25] = cwod[0],cwod[1]+pixel_total
    adj_cwods[26] = cwod[0],cwod[1]+2*pixel_total
    adj_cwods[27] = cwod[0],cwod[1]+3*pixel_total

    adj_cwods[28] = cwod[0]+pixel_total,cwod[1]-3*pixel_total
    adj_cwods[29] = cwod[0]+pixel_total,cwod[1]-2*pixel_total
    adj_cwods[30] = cwod[0]+pixel_total,cwod[1]-pixel_total
    adj_cwods[31] = cwod[0]+pixel_total,cwod[1]
    adj_cwods[32] = cwod[0]+pixel_total,cwod[1]+pixel_total
    adj_cwods[33] = cwod[0]+pixel_total,cwod[1]+2*pixel_total
    adj_cwods[34] = cwod[0]+pixel_total,cwod[1]+3*pixel_total

    adj_cwods[35] = cwod[0]+2*pixel_total,cwod[1]-3*pixel_total
    adj_cwods[36] = cwod[0]+2*pixel_total,cwod[1]-2*pixel_total
    adj_cwods[37] = cwod[0]+2*pixel_total,cwod[1]-pixel_total
    adj_cwods[38] = cwod[0]+2*pixel_total,cwod[1]
    adj_cwods[39] = cwod[0]+2*pixel_total,cwod[1]+pixel_total
    adj_cwods[40] = cwod[0]+2*pixel_total,cwod[1]+2*pixel_total
    adj_cwods[41] = cwod[0]+2*pixel_total,cwod[1]+3*pixel_total

    adj_cwods[42] = cwod[0]+3*pixel_total,cwod[1]-3*pixel_total
    adj_cwods[43] = cwod[0]+3*pixel_total,cwod[1]-2*pixel_total
    adj_cwods[44] = cwod[0]+3*pixel_total,cwod[1]-pixel_total
    adj_cwods[45] = cwod[0]+3*pixel_total,cwod[1]
    adj_cwods[46] = cwod[0]+3*pixel_total,cwod[1]+pixel_total
    adj_cwods[47] = cwod[0]+3*pixel_total,cwod[1]+2*pixel_total
    adj_cwods[48] = cwod[0]+3*pixel_total,cwod[1]+3*pixel_total
    
    adj_cwods[49] = cwod[0]+4*pixel_total,cwod[1]-3*pixel_total
    adj_cwods[50] = cwod[0]+4*pixel_total,cwod[1]-2*pixel_total
    adj_cwods[51] = cwod[0]+4*pixel_total,cwod[1]-pixel_total
    adj_cwods[52] = cwod[0]+4*pixel_total,cwod[1]
    adj_cwods[53] = cwod[0]+4*pixel_total,cwod[1]+pixel_total
    adj_cwods[54] = cwod[0]+4*pixel_total,cwod[1]+2*pixel_total
    adj_cwods[55] = cwod[0]+4*pixel_total,cwod[1]+3*pixel_total
    
#MY NEXT STEP IS TO SWITCH THE NAMING SYSTEM HERE. I want to make it so that the temp_ prefix refers to chunks that are currently sampling randomly. The chunk_arrays will start as empty arrays that are then written into after the temp_chunk_arrays go through filtering methods. I think this will make the code more readable, and hopefully easier to debug.
def gen_chunk(cwod): #generate a chunk, given its top left pixel location (I need to change it so that gas forms in blobs, some ores can be found appearing in veins, and the base element always gets placed instead of nothing.)
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
        if cwod[1] >= 0: #this conditional is used to keep the world separated between sky and ground
            chunk_type = numpy.random.random_integers(0,4*biome_stability) #This ensures that some chunks on any latitude can be comprised of any element. It is the random longitudinal biome generator. The 3 should represent the number of elements that have been coded.
            if chunk_type != 3: #currently this will always be called. Later, I'll make biomes.
                chunk_base_element = max(1,min(4,cwod[1]//5000)) #This is the latitudinal gradient filter. Having every chunk totally unique is rather odd. But having no unique chunks is rather boring. It only gets called when the longitudinal biome generator picks a number outside a certain range determined by the biome_stability. Currently, for every 5000 pixels traveled, the chunk_base_element increases by one, though it can be no smaller than 1.
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
        elif cwod[1] < 0 and cwod[1] > -10000:
            for row in range(chunk_size):
                for column in range(chunk_size):
                    chunk_array[row,column] = 0
            
        elif cwod[1] < -10000: #This will be for space chunks eventually.
            for row in range(chunk_size):
                for column in range(chunk_size):
                    if chunk_array[row,column] not in [0,1,2,3,4]:
                        chunk_array[row,column] = 0

        if cwod[1] > 0:
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

def make_chunks(wod,window_shiftx,window_shifty):
    det_adj_cwods(wod) #detect the key numbers for all nearby cwods
    block_rects = {}
    block_rects['solid'] = {'all':[],'oneium':[],'twoium':[]}
    block_rects['liquid'] = {'all':[]}
    block_rects['gas'] = {'all':[]}
    block_rects['matter'] = {'all':[],'oneium':[],'twoium':[]}
    #example of this construction: block_rects = {'solid':{'all':[<rect(0,0,30,30)>,...],'oneium':[<rect(0,0,30,30)>]},...}
    for adj_cwod in range(len(adj_cwods)):
        gen_chunk(adj_cwods[adj_cwod]) #create chunk arrays for all empty chunks within the adjacent range
        chunk_array = chunk_book[adj_cwods[adj_cwod]] #access each chunk_array within the chunk_book dictionary
        cloc = (adj_cwods[adj_cwod][0] - wod[0] + window_shiftx + block_size*16.1725,adj_cwods[adj_cwod][1] + wod[1] - window_shifty + block_size*10.5) #translate all the arrays as you move or when the window is resized

        #Create the actual blocks from the chunk recorded in the dictionary.
        for column in range(chunk_size):
            for row in range(chunk_size):
                element = chunk_array[row,column]
                block_loc = (int(cloc[0] + column * block_size),int(cloc[1] + row * block_size))
                block_rect = pygame.Rect(block_loc[0],block_loc[1],block_size,block_size)
                #if adj_cwods[adj_cwod] == (0,0):
                #    block_rects['liquid']['all'].append(block_rect)
                if element in [1,2]:
                    block_rects['solid']['all'].append(block_rect)
                    if element == 1:
                        block_rects['solid']['oneium'].append(block_rect)
                    elif element == 2:
                        block_rects['solid']['twoium'].append(block_rect)
                elif element == 3:
                    block_rects['liquid']['all'].append(block_rect)
                elif element == 4:
                    block_rects['gas']['all'].append(block_rect)
    return block_rects

def draw_blocks(block_rects,display):
    for block_rect in block_rects['solid']['oneium']:
        pygame.draw.rect(display,oneium,block_rect)
    for block_rect in block_rects['solid']['twoium']:
        pygame.draw.rect(display,twoium,block_rect)
    for block_rect in block_rects['liquid']['all']:
        pygame.draw.rect(display,threeium,block_rect)
    for block_rect in block_rects['gas']['all']:
        pygame.draw.rect(display,fourium,block_rect)
    #may want to eventually change this to be more like the drawing handler for matter so it's easier to read.

def break_block(break_block_tup,window_center,wod):
    global window_shiftx
    global window_shifty
    #first, find the wod plus the distance from the center of the screen to the pointer (call this the bwod). Then, find the chunk_wod, then find the distance from the chunk_wod to the bwod, then do the break.
    #bwod = [wod[0] + break_block_tup[0] - window_center[0] + block_size*0.5, -wod[1] + break_block_tup[1] + window_center[1] - pixel_total - block_size*5.5]
    bwod = [wod[0] + break_block_tup[0] - window_center[0] + window_shiftx + block_size*0.5, -wod[1] + break_block_tup[1] - window_center[1] - window_shifty - block_size*0.5]
    bwodc = [bwod[0]//pixel_total*pixel_total,bwod[1]//pixel_total*pixel_total]
    bloc = [int((bwod[0]-bwodc[0])//block_size),int((bwod[1]-bwodc[1])//block_size)]
    element = chunk_book[bwodc[0],bwodc[1]][bloc[1]][bloc[0]]
    chunk_book[bwodc[0],bwodc[1]][bloc[1]][bloc[0]] = 0
    mwod = [bwod[0] - wod[0] + window_center[0] - block_size, bwod[1] + wod[1] + window_center[1]]
    matter_rect = pygame.Rect(mwod[0],mwod[1],block_size*0.9,block_size*0.9)
    state = 0
    if element != 0:
        matter_list.append({'rect':matter_rect,'element':element,'state':state,'movement_x':0,'movement_y':0})

#Next, change this to have everything done and updated immediately in the matter_list itself, then draw things from the matter_list directly.
#After that, make it so that the matter also gets checked for collisions with other matter. May need to split the matter into its resident chunks or something so that the program doesn't get exhausted.
def move_matter(wod,block_rects,gravity,window_center):
    for matter in matter_list:
        matter['movement_x'] = 0
        matter['movment_y'] = 0
        if matter['element'] in [0,1]:
            lb = False
            tb = False
            rb = False
            bb = False
            mrlb = pygame.Rect(matter['rect'].left-1,matter['rect'].top,1,matter['rect'].height)
            mrtb = pygame.Rect(matter['rect'].left,matter['rect'].top+1,matter['rect'].width,1)
            mrrb = pygame.Rect(matter['rect'].right,matter['rect'].top,1,matter['rect'].height)
            mrbb = pygame.Rect(matter['rect'].left,matter['rect'].bottom,matter['rect'].width,1)
            if matter['rect'].collidelist(block_rects['solid']['all']):
                for block in block_rects['solid']['all']:
                    if mrlb.colliderect(block):
                        lb = True
                    if mrrb.colliderect(block):
                        rb = True
                    if mrtb.colliderect(block):
                        tb = True
                    if mrbb.colliderect(block):
                        bb = True
                for block in block_rects['solid']['all']:
                    if mrlb.colliderect(block):
                        if block.right > mrlb.left:
                            matter['movement_x'] = matter['movement_x']*0.9
                            matter['movement_x'] += min(matter['rect'].clip(block).width//5,block_size//5)
                    if mrrb.colliderect(block):
                        if block.left < mrrb.right:
                            matter['movement_x'] = matter['movement_x']*0.9
                            matter['movement_x'] += -min(matter['rect'].clip(block).width//5,block_size//5)
                    if mrtb.colliderect(block):
                        if block.bottom < mrtb.top:
                            matter['movement_y'] = matter['movement_y']*0.9
                            matter['movement_y'] += min(matter['rect'].clip(block).height//5,block_size//5)
                    if mrbb.colliderect(block):
                        if block.top < mrbb.bottom:
                            matter['movement_y'] = matter['movement_y']*0.9
                            matter['movement_y'] -= min(matter['rect'].clip(block).height//5,block_size//5)
            if not bb:
                if matter['movement_y'] <= block_size//5:
                    matter['movement_y'] += gravity
            #elif bb:
                #make a list of the blocks underneath the matter_rect and do a mass center determination to know whether it should tumble. This should only be done later, when things can actually rotate and store rotational momentum.

        matter['rect'].centerx += round(matter['movement_x'],2)
        matter['rect'].centery += round(matter['movement_y'],2)
        
def draw_matter(matter_list,display):
    for matter in matter_list:
        pygame.draw.rect(display,color_dict[str.split(str(matter['element']),'.')[0]],matter['rect'])

    #Next, come up with some way to check all the matter in the world's current location, then only bother rendering the ones within the adj_cwod range.
    #Not sure how to incorporate these next 2 lines, but these translations will have to happen if I want the objects to coordinate with the chunks.
    #cloc = (adj_cwods[adj_cwod][0] - wod[0] + window_shiftx + block_size*16.1725,adj_cwods[adj_cwod][1] + wod[1] - window_shifty + block_size*10.5) #translate all the arrays as you move or when the window is resized
    #block_loc = (int(cloc[0] + column * block_size),int(cloc[1] + row * block_size))
    #block_rect = pygame.Rect(block_loc[0],block_loc[1],block_size,block_size)
    
    return matter_list