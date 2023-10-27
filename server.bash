#!/usr/bin/bash

# Open first terminal and enter directory
gnome-terminal --working-directory=home/rohan/qualitas_bot/UI/qualitasbot --tab --title="UI Server" --command="serve -s build"

# Open second terminal and enter directory
gnome-terminal --working-directory=home/rohan/qualitas_bot/chatbot --tab --title="Chatbot Server" --command="flask run --host=0.0.0.0"