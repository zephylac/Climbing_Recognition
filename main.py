import random
import webcolors
from PIL import Image



# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:48:50 2017
@author: zephylac

In this version we try to locate the holds, identify their colors.
"""


# Find the closest color for an RGB value 
# Returns the color found in plain text
# @param
# requested_color : [R,G,B]
def closest_color(requested_color):
    # init dict
    min_color = {}
    for key, name in webcolors.html4_hex_to_names.items():
        # Saving RGB value for the color being treated
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        
        # We substract the color treated with the unknown value
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        
        # We fill the the dict with the sum of the the RBG value
        # from the previous substraction
        # The dict is filled with all the colors with the color deviation 
        # between the color know and the one we are trying to find
        min_color[(rd + gd + bd)] = name
        
    # We return the name of the color which has the minimum deviation    
    return min_color[min(min_color.keys())]

    
# Retrieve color from an RGB value
def get_color_name(requested_color):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        closest_name = closest_color(requested_color)
        return closest_name

# Return an array containing all the colors name 
# which are available on the picture
# @param :
#   holds_array : array containing dicts, each dict represent a single hold
def available_color(holds_array):
    # init the array which will contain all the color available
    color_array = []
    
    for i in range(len(holds_array)):
        if holds_array[i].get('color') not in color_array :
            color_array.append(holds_array[i])
    return color_array


# Return an array containing all the holds matching the color filter
# @param :
#   color : the color we want to filter on
#   holds_array : array containing dicts, each dict represent a single hold
def color_regroup(color, holds_array):
    # init the array which will contain all the holds matching the color
    array = []
    
    for i in range(len(holds_array)):
        if holds_array[i].get('color') == color:
            array.append(i)
    return array

# Retrieve the RGB median value of each hold and update the dict with
# the color name of the hold
# @param :
#   holds_array : array containing dicts, each dict represent a single hold            
def hold_RGBToName(holds_array):
    for i in range(len(holds_array)):
        # Convert RGB to color name
        color = get_color_name(holds_array[i].get('RGB'))
        # update dict
        holds_array[i].update({'color':color})   


# This function take an array of dict in parameters (array containing all the holds)
# It process each hold and update their dict adding to them the color of the hold
# value is the median value of all the pixel constituting the hold
# It's stored as an RGB value 
# @param :
#   holds_array : array containing dicts, each dict represent a single hold
def color_finder(holds_array):
    for i in range(len(holds_array)):
         
        Rtot = 0
        Gtot = 0
        Btot = 0
        total = len(holds_array[i].get('hold'))
        if total != 0 :
            for l in range(total) :
                (R,G,B) = pix[holds_array[i].get('hold')[l][0],holds_array[i].get('hold')[l][1]]
                Rtot += R
                Gtot += G
                Btot += B
            
       
            Rtot = Rtot / total                         
            Gtot = Gtot / total
            Btot = Btot / total
        
            # Cast the median into int because float value does not exist in RGB
            holds_array[i].update({'RGB':[int(Rtot),int(Gtot),int(Btot)]})         
        else :
            holds_array[i].update({'RGB':[0,0,0]})
        
# This function is drawing a frame around each hold, the color of the frame
# is the median color of the hold
# @param :
#   holds_array : array containing dicts, each dict represent a single hold
def drawing_frame(holds_array) :
    for i in range(len(holds_array)) :
        minX, maxX, minY, maxY = holds_array[i].get('corner')
        #R, G, B = holds_array[i].get('RGB')
        R, G, B = 255, 0, 0
        for j in range(minX,maxX) :
            pix[j,minY] = R, G, B 
            pix[j,maxY] = R, G, B            
        for k in range(minY,maxY) :
            pix[minX,k] = R, G, B
            pix[maxX,k] = R, G, B
            print ("Drawing frame : [",round((i/(len(holds_array))* 100),0)," %]") 
            
            


# @param :
#   width : width of the image
#   height : height of the image
#   holds_array : array containing dicts, each dict represent a single hold
def framing(width, height, holds_array) :
    for i in range(len(holds_array)) :
        minX = width
        maxX = 0
        minY = height
        maxY = 0
        
        for j in range(len((holds_array[i].get('hold')))):
            Xo, Yo = (holds_array[i].get('hold')[j])
            if Xo > maxX :
                maxX = Xo
            if Xo < minX :
                minX = Xo
            
            if Yo > maxY :
                maxY = Yo
            if Yo < minY :
                minY = Yo
        holds_array[i].update({'corner':[minX, maxX, minY, maxY]})
        print ("Framing : [",round((i/(len(holds_array))* 100),0)," %]")
    return holds_array


# Returns True or False wether if the color deviation between the two pixel
# is tolerated or not
# @param :
#   x1, y1 : coordinates of the first pixel
#   x2, y2 : coordinates of the second pixel
def color_deviation_accepted(x1, y1, x2, y2) :

        # Retrieve RGB value from a pixel identified with x1 and y1
        Ro, Go, Bo = pix[x1,y1]
    
        # Retrieve RGB value from a pixel identified with x1 and y1    
        Rt, Gt, Bt = pix[x2, y2]

        # Maximum color deviation to identify a hold
        # increasing its size may reduce the noise but may also not be able
        # to identify close color (I.E green and light green)
    
        # reducing its value allow to identify holds better but increase the noise
        ecart = 110
    
        
        # DEBUG LINE - not identifying the color which identify holds
        # if Rt == 255 and Gt == 0 and Bt == 0 : return
    
        # If the color deviation is inside the interval of tolerance
        # We add the pixel coordinates to hold array
        if (Ro + ecart < Rt or Ro - ecart > Rt or Go + ecart < Gt or Go - ecart > Gt or Bo + ecart < Bt or Bo - ecart > Bt):
            return True
        else :
            return False
        
        
# Return an array containing all the holds found in the picture, 
# Each holds is represented by an array which contains all the pixels
# which are forming the holds
# @param : 
#   width : width of the image
#   height : height of the image
#   primary_array : array containing all pixel that have been spotted
def grouping_image( width, height, primary_array ) :
    # init the array which will contain all the holds found on the picture
    holds_array = []
    
    primary_bis = primary_array.copy()
    for k in range(len(primary_array)) :
        x, y = primary_array[k]
        
        hold_array = grouping(x, y, width, height, primary_array, primary_bis)
        
        # if hold_array is 'not' it means that the array is empty
        # It also means that the pixel has already been grouped.
        if hold_array :
            # We add the array representing a single hold to the array containing
            # all the holds that has been found in the picture 
            holds_array.append({'hold':hold_array})
        print ("Grouping image : [",round((k/(len(primary_array))* 100),0)," %]")
        

     
    return holds_array

# Group all pixel from same hold
# @param : 
#   x : Value on X axis
#   y : Value on Y axis
#   width : width of the image
#   height : height of the image
#   primary_array : array containing all pixel that have been spotted
#   primary_bis : copy of primary_array
def grouping(x,y,width,height,primary, primary_bis) :
    # init the array to empty
    single_hold_array = []
    
    for i in range(-2,2) :
        for j in range(-2,2):
            if not(x == 0 and i < 0) and not (x == width and i > 1) and not (y == 0 and j < 0) and not (y == height and j > 1) :
                if([x+i,y+j]) in primary_bis:
                    # after testing verfying color seems to broke the alorithm
                    #if(color_deviation_accepted(x, y, x+i, y+j) == True) :
                    
                    # A pixel around the specified one has been identified 
                    # as part of the same hold, we add it to the array
                    single_hold_array.append([x+i,y+j])
                        
                    # We remove the value from the array so we don't add it again
                    # an we avoid infinite loop between to pixel neighbooring each other
                    primary_bis.remove([x+i,y+j])
                        
                    # Pixel around the one we added might also be from the same hold
                    # We recursively call them
                    temp_array = grouping(x+i,y+j,width,height,primary,primary_bis)
                        
                    # We add the pixel from the neighboor of the neighboor......
                    # to the array
                    single_hold_array += temp_array
                        
    return single_hold_array

# Removes the background
# @param : 
#   width : width of the image
#   height : height of the image
def remove_background(width, height) :
    
    temp_pix = pix[0,0]
    
    Rtot = 0
    Gtot = 0
    Btot = 0
        
    for i in range(1000):
        x = random.randint(0,width-1) 
        y = random.randint(0,height-1)
        
        R, G, B = pix[x,y]
        
        Rtot += R
        Gtot += G
        Btot += B
        
       
    Rtot = Rtot / 1000                        
    Gtot = Gtot / 1000
    Btot = Btot / 1000
    
    pix[0,0] = int(Rtot), int(Gtot), int(Btot)
    
    for i in range(width) :
        for j in range(height) : 
            if(color_deviation_accepted(i, j, 0, 0) == False) :
               pix[i,j] = (255,255,255)
        print ("Removing background : [",round(i/width * 100)," %]")
    pix[0,0] = temp_pix

# This function try to spot pixel belonging to holds. When a pixel is spotted
# It's added to the primary array
# @param : 
#   width : width of the image
#   height : height of the image
def spotting_image(width, height) :
    
        # init the array which contain every pixel forming all the holds
    primary_array = []
    
    for i in range(width) :
        for j in range(height) : 
            spotting(i, j, width, height, primary_array) 
        print ("Spotting image : [",round(i/width * 100,0)," %]")
    
    return primary_array 
    
    
# For a specified pixel, we check pixels around it  to see if they have
# the same color
# @param : 
#   x : Value on X axis
#   y : Value on Y axis
#   width : width of the image
#   height : height of the image
#   primary_array : array containing all pixel that have been spotted
def spotting(x,y,width,height,primary_array) :
    # We look around the single pixel and try to connect it to other
    # pixels if they have the same-ish color 
    

        for i in range(-1,1) :
            for j in range(-1,1):
                # avoid invalid coordinates (outside the picture)
                if not(x == 0 and i == -1) and not (x == width and i == 1) and not (y == 0 and j == -1) and not (y == height and j == 1) : 
                    # retrieve the value of a pixel around the one selected
                    
                    if(color_deviation_accepted(x, y, x+i, y+j) == True) :
                        # If it's not already inside
                        # Complexity to look if value is inside is not really a problem
                        # Since the size of a hold is not that big (max ~100 * 100)                    
                        if not ([x,y] in primary_array) :
                            
                            primary_array.append([x,y])
                            
    
    
# Regrouping allow to regroup holds if they have the same color and are too close.
# We consider them as one hold because it will be easier to display them
# @param :
#   holds_array : array containing dicts, each dict represent a single hold
def regrouping(holds_array) :
    new_array = []
    
    for i in range(len(holds_array)) :
        hold = holds_array[i]
        minX, maxX, minY, maxY = hold.get('corner')
        color = hold.get('color')
        for j in range(len(holds_array)):
            if hold != holds_array[j] :
                min2X, max2X, min2Y, max2Y = holds_array[j].get('corner')
                if(holds_array[j].get('color') == color) :
                    if((minX <= min2X <= maxX or minX <= max2X <= maxX) and (minY <= min2Y <= maxY or minY <= max2Y <= maxY)) :
                        minX = min(minX, min2X)
                        maxX = max(maxX, max2X)
                        minY = min(minY, min2Y)
                        maxY = max(maxY, max2Y) 
                        RGB = [x + y for x,y in zip(hold.get('RGB'),holds_array[j].get('RGB'))]
                        pixel = hold.get('hold') + holds_array[j].get('hold')
                        new_array.append({'RGB':RGB,'color':hold.get('color'),'corner':[minX,maxX,minY,maxY],'hold':pixel})
    return new_array

#INPUT
# create FilePointer for the img specified
img = Image.open("5.jpg")
    

# Fill pix with the array containing the picture
pix = img.load()
# Retrieving width and height 
width, height = img.size
 
#Spot all pixel belonging to holds
primary_array = spotting_image(width, height)
        
#Group pixel to form holds
holds_array = grouping_image(width, height, primary_array)
        
#Calculate and add frame for each hold(minX,maxX,minY,maxY)
framing(width,height, holds_array)
    
#Add RGB value for each hold
color_finder(holds_array)
        
#Add color name for each hold
hold_RGBToName(holds_array)
    
#Return an array of hold (but only those who have been combined)
new = regrouping(holds_array)
        
# Return an array of all color available for the holds
color_array = available_color(holds_array)
        
#Drawing holds
drawing_frame(holds_array)

#Drawing holds that has been combined
drawing_frame(new)
    
#remove_background(width, height)
        
#color_array = color_regroup('gray',holds_array)
 
#show results   
img.show()
img.save("test.jpg")
