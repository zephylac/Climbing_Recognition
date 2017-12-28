import webcolors
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:48:50 2017

@author: zephylac
"""


def closest_color(requested_color):
    min_color = {}
    for key, name in webcolors.html4_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_color[(rd + gd + bd)] = name
    return min_color[min(min_color.keys())]

    
def get_color_name(requested_color):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        closest_name = closest_color(requested_color)
        actual_name = None
        return closest_name

def couleur_dispo():
    for i in range(len(liste6)):
        """if(int(liste[i][0]) != 0 and int(liste[i][1]) != 0 and int(liste[i][2]) != 0):"""
        if liste6[i] not in listeCouleur :
            listeCouleur.append(liste6[i])

def regroupe_couleur(couleur):
    for i in range(len(liste5)):
        if(int(liste5[i][0]) != 0 and int(liste5[i][1]) != 0 and int(liste5[i][2]) != 0 and liste6[i] == couleur):
            listePtr.append(i)
            
            
"""Attribue un nom de couleur a chaque prise"""
def traitement8():
    for i in range(len(liste5)):
        liste6.append(get_color_name(liste5[i]))

"""Determine la couleur de la prise"""
def traitement7():
    for i in range(len(liste4)):
         """ Recupere les coordonnées de la zone concernée """
         minX, maxX, minY, maxY = liste4[i]
         if(maxY - minY) == 0 :
             #Exception, la zone ne concerne qu'un pixel sur Y
             ecartY = 1
         else:
             ecartY = maxY - minY
             
         if(maxX - minX) == 0 :
             #Exception la zone ne concerne qu'un pixel sur X
             ecartX = 1
         else:
             ecartX = maxX - minX   
         
         total = ecartY * ecartX
        
        
         Rtot = 0
         Gtot = 0
         Btot = 0
         
         for j in range(minY,maxY):
             for k in range(minX,maxX):
                 (Rmoy,Gmoy,Bmoy) = pix[k,j]
                 Rtot += Rmoy
                 Gtot += Gmoy
                 Btot += Bmoy
             """    print(Rtot,Gtot,Btot)"""
         Rtot = Rtot / total                         
         Gtot = Gtot / total
         Btot = Btot / total
         liste5.append([Rtot,Gtot,Btot])
         

"""Tracage des bordures des cadres"""
def traitement6bis() :
    for i in range(len(listePtr)) :
        minX, maxX, minY, maxY = liste4[listePtr[i]]
        for j in range(minX,maxX) :
            pix[j,minY] = (int(liste5[listePtr[i]][0]),int(liste5[listePtr[i]][1]),int(liste5[listePtr[i]][2]))
            pix[j,maxY] = (int(liste5[listePtr[i]][0]),int(liste5[listePtr[i]][1]),int(liste5[listePtr[i]][2]))
            
        for k in range(minY,maxY) :
            pix[minX,k] = (int(liste5[listePtr[i]][0]),int(liste5[listePtr[i]][1]),int(liste5[listePtr[i]][2]))
            pix[maxX,k] = (int(liste5[listePtr[i]][0]),int(liste5[listePtr[i]][1]),int(liste5[listePtr[i]][2]))
            print ("Etape 5 : [",round((i/(len(liste4))* 100),0)," %]") 

         
"""Tracage des bordures des cadres"""
def traitement6() :
    for i in range(len(liste4)) :
        minX, maxX, minY, maxY = liste4[i]
        for j in range(minX,maxX) :
            pix[j,minY] = (int(liste5[i][0]),int(liste5[i][1]),int(liste5[i][2]))
            pix[j,maxY] = (int(liste5[i][0]),int(liste5[i][1]),int(liste5[i][2]))
            
        for k in range(minY,maxY) :
            pix[minX,k] = (int(liste5[i][0]),int(liste5[i][1]),int(liste5[i][2]))
            pix[maxX,k] = (int(liste5[i][0]),int(liste5[i][1]),int(liste5[i][2]))
            print ("Etape 5 : [",round((i/(len(liste4))* 100),0)," %]") 
            
            
"""encadrement des groupes"""
#@param : width : width of the image, height : height of the image
def traitement5(width,height) :
    for i in range(len(liste3)) :
        minX = width
        maxX = 0
        minY = height
        maxY = 0
        
        for j in range(len((liste3[i]))):
            Xo, Yo = (liste3[i])[j]
            if Xo > maxX :
                maxX = Xo
            if Xo < minX :
                minX = Xo
            
            if Yo > maxY :
                maxY = Yo
            if Yo < minY :
                minY = Yo
        liste4.append([minX, maxX, minY, maxY])
        print ("Etape 4 : [",round((i/(len(liste3))* 100),0)," %]")


"""identification des groupes"""
#@Param : x : Value on X axis, Y : Value on Y axis, width : width of the image, height : height of the image
def traitement4(x,y,width,height) :
    for i in range(-2,2) :
        for j in range(-2,2):
            if not(x == 0 and i < 0) and not (x == width and i > 1) and not (y == 0 and j < 0) and not (y == height and j > 1) :
                if([x+i,y+j]) in listebis:
                    """pix[x+i,y+j] = (0,255,0)"""
                    liste2.append([x+i,y+j])
                        
                    listebis.remove([x+i,y+j])
                    traitement4(x+i,y+j,width,height)
                    liste3.append(liste2.copy())
                    liste2.clear()

"""suppression arriere plan"""
def traitement3(x,y) :
    if pix[x,y] != (255,0,0):
        pix[x,y] = (255,255,255)

"""identification"""
def traitement2(x,y) :
    if not ([x,y] in liste) :
        liste.append([x,y])
        """pix[x,y] = (255, 0, 0)"""
        
    
"""reperage"""   
def traitement(x,y,width,height) :
    Ro, Go, Bo = pix[x,y]
    ecart = 110
    for i in range(-1,1) :
        for j in range(-1,1):
            if not(x == 0 and i == -1) and not (x == width and i == 1) and not (y == 0 and j == -1) and not (y == height and j == 1) : 
                Rt, Gt, Bt = pix[(x + i), (y + j)]
                if Rt == 255 and Gt == 0 and Bt == 0 : return
                if (Ro + ecart < Rt or Ro - ecart > Rt): traitement2(x,y);
                if (Go + ecart < Gt or Go - ecart > Gt): traitement2(x,y);
                if (Bo + ecart < Bt or Bo - ecart > Bt): traitement2(x,y);
            

from PIL import Image
im = Image.open("3.jpg") 
pix = im.load()
width, height = im.size
liste = []
listebis = []
liste2 = []
liste3 = []
liste4 = []
liste5 = []
liste6 = []
listeCouleur = []
listePtr = []

for i in range(width) :
    for j in range(height) : 
        traitement(i,j,width,height) 
    print ("Etape 1 : [",round(i/width * 100,0)," %]") 

"""for i in range(width) :
    for j in range(height) :
        traitement3(i,j)
        print ("Etape 2 : [",(i/width * 100)," %]") 
"""    
listebis = liste.copy()
for k in range(len(liste)) :
    m, n = liste[k]
    traitement4(m,n,width,height)
    print ("Etape 3 : [",round((k/(len(liste))* 100),0)," %]")

traitement5(width,height)

traitement7()
"""traitement6()"""
traitement8()
couleur_dispo()
regroupe_couleur('gray')
traitement6()
im.show()
im.save("test.jpg")     
                    


