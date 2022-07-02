import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import matplotlib.image as pli
import cv2

L = [
    'pleiades15.png',
    ]

for el in L:
    intensite= 0.75 #Plus c'est bas plus le bruit est fort ]0,1]
    nom_image = el
    image = (io.imread(nom_image)).astype(float)

    try:
        #Si image rgba le bruit se fera que sur rgb pas sur a
        image_bruit= np.zeros(np.shape(image))
        image_bruit[:,:,0] = np.random.poisson(image[:,:,0]*intensite)/255
        image_bruit[:,:,1] = np.random.poisson(image[:,:,1]*intensite)/255
        image_bruit[:,:,2] = np.random.poisson(image[:,:,2]*intensite)/255
        image_bruit[:,:,3] = image[:,:,3]/255
    except:
        # Si image que rgb on ne peux pas distinguer le rgb du a 
        image_bruit= np.random.poisson(image*intensite)

    plt.imshow(image_bruit)
    plt.axis('off')
    plt.tight_layout()
    #plt.savefig(nom_image[:-4]+'bruit.png')
    pli.imsave(nom_image[:-4]+'bruit.png', image_bruit)



def enlever_bruit(nom_image):
    image=cv2.imread(nom_image)
    
    dst= cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    plt.imshow(dst)
    plt.axis('off')