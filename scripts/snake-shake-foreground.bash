#!/usr/bin/env bash

# Copy the Env class to a directory where Blender can find it.
#cp src/snakeshake/env/Env.py /Applications/blender.app/Contents/Resources/2.78/python/lib/python3.5/site-packages/snakeshake/Env.py
cp src/convobot/simulator/blender/RadialEnv.py /Applications/blender.app/Contents/Resources/2.78/python/lib/python3.5/site-packages/snakeshake/Env.py

# Start blender with the UI and load the SnakeShake foreground server.s
/Applications/blender.app/Contents/MacOS/blender -P src/snakeshake/SnakeShakeFGServer.py
