#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

cd src
# Create the images in blender
# python convobot/simulator/blender/SimulateImages.py -d convobot -e ../config -c test

# Convert the images to 28x28 grayscale
# python convobot/imageprocessor/PrepareImages.py -d convobot -e ../config -c test-color

# Run the model 1-run, 1-epoch on the grayscale images.
python convobot/model/mnist/model.py -d convobot -e ../config -m mnist-color -c test-color
cd ..
