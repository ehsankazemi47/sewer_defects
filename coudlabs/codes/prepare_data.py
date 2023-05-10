'''
File name: prepare_data.py
Author: Ehsan Kazemi
Date created: Apr 2023
Date last modified: 28 Apr 2023
-------------------------------------------------------------------------\
 This code reads the data from the data folder and copy them into the    /
 coudlabs training data folder in subfolders for training, validation    \
 and test.                                                               /
-------------------------------------------------------------------------\
'''

# Import dependencies
import os
import glob
import random
import shutil
from PIL import Image

# name of dataset
data_name = "d1"

# Set the paths for the source folder and the three destination folders
data_path = 'C:/Ehsan/sewer_data/labelled images'
destination_dir = "C:/Ehsan/sewer_defects/coudlabs/data/" + data_name

# file extensions
extensions = ["png", "jpg", "tif", "bmp"]

# convert to grey? "y" or "n"
cl2gry = "y"

# Set the percentages for each subset (should add up to 100)
train_percent = 70
valid_percent = 15
test_percent = 15

# Set the local paths for the three folders where the downloaded files will be saved
train_images = destination_dir + "/images/training/"
train_labels = destination_dir + "/labels/training/"
valid_images = destination_dir + "/images/validation/"
valid_labels = destination_dir + "/labels/validation/"
test_images = destination_dir + "/images/test/"
test_labels = destination_dir + "/labels/test/"

# Destination folders (to be overwritten))
for folder in [train_images,valid_images,test_images,train_labels,valid_labels,test_labels]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

# List of image files in source path
image_list = []
for ext in extensions:
    image_list.extend(glob.glob(os.path.join(data_path, f'*.{ext}')))

# Calculate the number of files for each subset based on the percentages
nsub_train = int(len(image_list) * train_percent / 100)
nsub_valid = int(len(image_list) * valid_percent / 100)
nsub_test = int(len(image_list) * test_percent / 100)

# Splid images intwo three subsets (training / validation / test) randomly
random.shuffle(image_list)
files_trainset = image_list[0:nsub_train]
files_validset = image_list[nsub_train:nsub_train+nsub_valid]
files_testset = image_list[nsub_train+nsub_valid:nsub_train+nsub_valid+nsub_test]

# Function to convert images into grey and then 
# copy images and labels to the destination folders
def process_file(image_path,image_destination,label_destination):
    missing_label_files = []
    for file in image_path:
        # folder path, file name and file extension
        folder, file_name_with_extension = os.path.split(file)
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        # convert image to grey?
        if cl2gry == 'y':  # convert
            image = Image.open(file)
            image = image.convert('L')
            image.save(os.path.join(image_destination, file_name + file_extension))
        else:   # just copy the original image
            shutil.copy(file, image_destination)
        # label file
        label_file = os.path.join(folder, file_name + ".txt")
        if os.path.isfile(label_file):
            shutil.copy(label_file, label_destination)
        else:
            missing_label_files.append(label_file)
    if missing_label_files:
        raise Exception("ERROR: the following label files are missing: ", missing_label_files)

# Copy files
print(f'Training data set ... {train_percent}% of data')
process_file(files_trainset,train_images,train_labels)
print(f'Validation data set ... {valid_percent}% of data')
process_file(files_validset,valid_images,valid_labels)
print(f'Test data set ... {test_percent}% of data')
process_file(files_testset,test_images,test_labels)