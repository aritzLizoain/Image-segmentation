# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 17:44:17 2020

@author: Aritz Lizoain

MASK IMAGE

This code creates the masks and labels

Idea explained in: https://www.jeremyjordan.me/semantic-segmentation/#advanced_unet

PROCESS:    
    *(n_images, x size, y size, 3(rgb)) -------- Takes training image dataset
    
    *(n_images, x size, y size, 1(mean)) ------- Makes it monochrome inside get_mask
    
    *(n_images, x size, y size, n_classes) ----- Creates the mask with get_class in get_mask
    Checks for threshold pixel values 
    E.g.: [background, glowing, hot pixel, cluster] --> n_classes = 4
    get_mask checks every pixel and for each pixel get_class determines the class
    For example for a hot pixel, get_class gets class=2, then n_classes=[0,0,1,0]
    
    *(n_images, x size, y size, 1(max_mask)) --- Gets the maximum value position in mask
    With the previous example: max_mask=2
    
    *(n_images, x size, y size, 3(rgb)) -------- Creates the label with mask_to_label
    Depending on which class it is, it will color it with the corresponding multiplier
    
It plots a random example and shows statistics (n_classes and percentage of each class) 
Different functions are created to convert data, for example: output_to_label()

"""

import os
import sys
import numpy as np
import cv2
from skimage.transform import resize
import random
import matplotlib.pyplot as plt
from load_dataset import *
import matplotlib.patches as mpatches

##############################################################################

# TRAIN_PATH = 'C://Path/' #training images dataset path
# TEST_PATH  = 'C://Path/' #testing images dataset path
# TEST_PREDICTIONS_PATH = 'C://Path/' #testing outputs path
# IMG_WIDTH = 258
# IMG_HEIGHT = 258
IMG_CHANNELS = 4

# images, test_images = load_images(TRAIN_PATH, TEST_PATH, TEST_PREDICTIONS_PATH, IMG_WIDTH = 258, IMG_HEIGHT = 258)

#-----------------------------------------------------------------------------

#Converts the input image (n_img, h, w, 3(rgb)) in (n_img, h, w, 1)
def get_monochrome (images):
    monochrome = images.mean(axis=3)
    return monochrome
  
#-----------------------------------------------------------------------------
    
#Checks all pixels of image monochrome and decide which class it is, with pixel value thresholds
def get_class(value): #All pixels are checked one by one with 3 for loops inget_maks 
    
    #thresholds are pixel values of each color. Could be energies as well
    #need to check these on Xtrain_monochrome. WARNING: some pixels might fail
    background_threshold = 53.01
    glowing_min_threshold = 91
    glowing_max_threshold = 101.01
    hot_pixel_threshold = 78
    #cluster_threshold = no need   
    
    #they need to be in order
    if value < background_threshold:
        return 0
    elif glowing_max_threshold > value > glowing_min_threshold:
        return 1
    elif value > hot_pixel_threshold:
        return 2
    else:
        return 3

#-----------------------------------------------------------------------------

#Creates masks with shape (n_img, h, w, n_classes) from inputs. Uses get_monochrome() and get_class()
def get_mask(images): #input shape (ix, height, width, 3(rgb))
    Xtrain_monochrome = get_monochrome(images) #shape (ix, height, width, 1(mean value of rgb))
    #mask. Initialized as zeros in shape (ix, height, width, channels)
    mask=np.zeros((len(Xtrain_monochrome),Xtrain_monochrome.shape[1],Xtrain_monochrome.shape[1],IMG_CHANNELS)) 
    for ix in range(len(Xtrain_monochrome)):
        for height in range(Xtrain_monochrome.shape[1]):
                for width in range(Xtrain_monochrome.shape[2]): 
                    if get_class(Xtrain_monochrome[ix,height,width]) == 0: 
                        #depending on which class it is, it will store the value of 1
                        #in the corresponding channel depth, while the rest is 0
                        classes=0
                        mask[ix,height,width,classes] = 1
                    if get_class(Xtrain_monochrome[ix,height,width]) == 1:
                        classes=1
                        mask[ix,height,width,classes] = 1
                    if get_class(Xtrain_monochrome[ix,height,width]) == 2:
                        classes=2    
                        mask[ix,height,width,classes] = 1
                    if get_class(Xtrain_monochrome[ix,height,width]) == 3:
                        classes=3 
                        mask[ix,height,width,classes] = 1
    return mask #output shape mask: (ix, height, width, channels)

# classes array depth: [background, glowing, hot pixel, cluster]
# e.g. hot pixel (class 2) : [0,0,1,0] --> max_in_mask = 2 (class 2, position 2 in classes array)

#-----------------------------------------------------------------------------

#Gets the position of the maximum value, this is, the class
def get_max_in_mask(mask):
    #mask_max. Initialized as zeros in shape (ix, height, width, 1(max positions in mask))
    mask_max=np.zeros((len(mask),mask.shape[1],mask.shape[2]))
    for ix in range(len(mask)): 
        mask_max[ix]=np.argmax(mask[ix], axis=2)
    return mask_max #output shape: (ix, height, width, 1(max positions in mask))

#-----------------------------------------------------------------------------

"""
# BACKGROUND (class 0): brown_multiplier = [40./255, 26./255, 13./255]
# GLOWING (class 1): green_multiplier = [0.35,0.75,0.25]
# HOT PIXELS (class 2): blue_multiplier = [0,0.5,1.]#[0,0.25,0.9]
# CLUSTERS (class 3): red_multiplier = [1, 0.2, 0.2]
# yellow_multiplier = [1,1,0.25] unused
"""

#Creates a label with shape (n_img, h, w, 3(rgb)) that can be represented
def mask_to_label(mask_max): #input shape (ix, height, width, 1(max positions in mask))
    label=np.stack((mask_max,)*3, axis=-1) #label. Initialized as class values stacked 3 times in shape (ix, height, width, rgb(3))
    black_multiplier = [0./255, 0./255, 0./255]
    green_multiplier = [0.35,1.,0.25]
    blue_multiplier = [0,0.5,1.]#[0,0.25,0.9]
    red_multiplier = [1, 0.2, 0.2]
    for ix in range(len(mask_max)):
        for height in range(mask_max.shape[1]):
                for width in range(mask_max.shape[2]): 
                    if mask_max[ix, height, width] == 0: #class BACKGROUND, color BROWN 
                        #depending on which class it is, it will color it with the corresponding multiplier
                        label[ix,height,width,0] = black_multiplier[0]
                        label[ix,height,width,1] = black_multiplier[1]
                        label[ix,height,width,2] = black_multiplier[2] 
                    if mask_max[ix, height, width] == 1: #class GLOWING, color GREEN 
                        label[ix,height,width,0] = green_multiplier[0]
                        label[ix,height,width,1] = green_multiplier[1]
                        label[ix,height,width,2] = green_multiplier[2] 
                    if mask_max[ix, height, width] == 2: #class HOT PIXELS, color BLUE 
                        label[ix,height,width,0] = blue_multiplier[0]
                        label[ix,height,width,1] = blue_multiplier[1]
                        label[ix,height,width,2] = blue_multiplier[2] 
                    if mask_max[ix, height, width] == 3: #class CLUSTERS, color RED 
                        label[ix,height,width,0] = red_multiplier[0]
                        label[ix,height,width,1] = red_multiplier[1]
                        label[ix,height,width,2] = red_multiplier[2] 
    print('Labels correctly created')
    return label #output shape mask: (ix, height, width, 3(rgb))

#-----------------------------------------------------------------------------

#Shows statistics regarding classes
def statistics(mask_max):
    unique_elements, counts_elements = np.unique(ar = mask_max,
                                              return_counts = True)
    print('There are {0} different classes'.format(len(unique_elements)))
    #print('counts_elements = {0}'.format(counts_elements))
    class_frequency = counts_elements / np.sum(counts_elements)
    print('The percetage of class 0 (background) in the dataset is: {0} %'.format(round(class_frequency[0]*100, 2)))
    print('The percetage of class 1 (glowing) in the dataset is: {0} %'.format(round(class_frequency[1]*100, 2)))
    print('The percetage of class 2 (hot pixels) in the dataset is: {0} %'.format(round(class_frequency[2]*100, 2)))
    print('The percetage of class 3 (clusters) in the dataset is: {0} %'.format(round(class_frequency[3]*100, 2)))

#-----------------------------------------------------------------------------

#Returns percentages of each class. Used to calculate the weights for the loss function
def get_percentages(images):
    mask=get_mask(images)
    mask_max=get_max_in_mask(mask)
    unique_elements, counts_elements = np.unique(ar = mask_max,
                                              return_counts = True)
    #print('counts_elements = {0}'.format(counts_elements))
    class_frequency = counts_elements / np.sum(counts_elements)
    percentages=np.zeros(len(unique_elements))
    for i in range(len(unique_elements)):
        percentages[i] = round(class_frequency[i]*100, 2)
    return unique_elements, percentages
    
#-----------------------------------------------------------------------------

#Visualizes the label with shape (n_img, h, w, 3(rgb))
def visualize_label(images, label): 
    
    #for ix in range (len(images)):                   
    ix = random.randint(0, len(images)-1)
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    ax[0].imshow(images[ix])
    ax[0].set_title('Training image example: {0}'.format(ix+1), fontsize=25);
    ax[0].set_xlabel('pixels', fontsize=16)
    ax[0].set_ylabel('pixels', fontsize=16)
    ax[0].tick_params(axis='both', which='major', labelsize=16)
    ax[1].imshow(np.squeeze(label[ix]))
    ax[1].set_title('Training label example: {0}'.format(ix+1), fontsize=25);
    ax[1].set_xlabel('pixels', fontsize=16)
    ax[1].set_ylabel('pixels', fontsize=16)
    ax[1].tick_params(axis='both', which='major', labelsize=16)
    red_patch = mpatches.Patch(color=[1, 0.2, 0.2], label='Cluster')
    blue_patch = mpatches.Patch(color=[0,0.5,1.], label='Hot pixel')
    green_patch = mpatches.Patch(color=[0.35,1.,0.25], label='Glowing')
    black_patch = mpatches.Patch(color=[0./255, 0./255, 0./255], label='Background')
    plt.legend(handles=[red_patch, blue_patch, green_patch, black_patch])
    plt.show()
      
#-----------------------------------------------------------------------------

#This is what the model receives as labels, with shape (ix, height, width, n_classes)
def create_masks(images):
    mask=get_mask(images)
    print('Masks correctly created')
    return mask 

#-----------------------------------------------------------------------------

#From images to labels for representations    (the whole process) 
def create_labels(images):
    mask=get_mask(images)
    mask_max=get_max_in_mask(mask) #this is what the model needs for training
    statistics(mask_max)
    label=mask_to_label(mask_max)
    print('Black: BACKGROUND')
    print('Green: GLOWING')
    print('Blue: HOT PIXEL')
    print('Red: CLUSTER')
    #visualize_label(images, label) # no need. augmentation will show an example
    return label

#-----------------------------------------------------------------------------
    
#The only difference with create_labels() is that it does not print the information
#Done in order to avoid repeated information shown in the console   
def create_labels_noStat_noPrint(images):
    mask=get_mask(images)
    mask_max=get_max_in_mask(mask) 
    label=mask_to_label(mask_max)
    return label

#-----------------------------------------------------------------------------

#The model gives output with shape (n_img, h, w, n_classes); a mask
#This function gets the positions of the maximum values from the mask, giving a shape (n_img, h, w, 1)
#Then a label is created from this
#The result is a label with shape (n_img, h, w, 3(rgb))
def output_to_label(predictions):
    mask_max=get_max_in_mask(predictions)
    predicted_label=mask_to_label(mask_max)
    return predicted_label
