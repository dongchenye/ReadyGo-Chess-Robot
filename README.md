# ReadyGo Chess Robot 
## Project Demo Video
[![Watch the video](https://img.youtube.com/vi/sLf-PWcZ84k/hqdefault.jpg)](https://youtu.be/sLf-PWcZ84k)

## Table of Contents

[Overview](#Overview)    
[Vision](#Vision)    
[Mission](#Mission)    
[Project Presentation Poster](#Poster)    
[*Ready Go* System Design](#SystemDesign)    
[Edge Detection - Board recognition ](#EdgeDetection)     


## <a name="Overview"></a>Overview
<img src="/images/Overview.png" width="700" >

"READY GO!" is a system that will allow for a person to play chess against a robot. The person will be able to select from various difficulties using a switch that has 3 modes for easy, medium, and hard. The robot will take input from the person using a camera and machine vision to discern the different pieces and their positions. The camera will be mounted on a pole and will only record position once a button is pressed by the user to signify that the person is done moving. Then the GUI provided will tell the user where the "READY GO" system wants to move the next chess piece and the game will continue.

## <a name="Vision"></a>Vision
The vision of ReadyGo Chess Robot is to inspire the next generation of engineers and software developers through machine vision and play. READY GO consists of three major system components:  the machine learning model used to detect the pieces and board, the chess engine using the open-source engine called Stockfish, and the User Interface using python's Tkinter library.

## <a name="Mission"></a>Mission
Our mission is simple: to design, develop, and create a chess playing system via machine vision. Utilizinga YOLO (You Only Look Once) object detection machine learning model, we will train the system todetect pieces of any type on any board. Using a pre-built Stockfish chess engine, our model will be ableto analyze the state of the game and choose the best move.  After the board state has been processedand a move has been chosen, our system will output a move to the appropriate square.

## <a name="Poster"></a>Project Presentation Poster
<img src="/images/Project_Presentation_Poster.png" width="700" >

## <a name="SystenDesign"></a>*Ready Go* System Design
<img src="/images/System_Design.png" width="900" >

## <a name="EdgeDetection"></a>Edge Detection - Board recognition 
#### Original input Board image:
<img src="/images/Edge_Detection/Board_image.jpg" width="400" >

#### Detected edges and corners:
<img src="/images/Edge_Detection/Corners_image.png" width="400" >

#### Identify squares:
<img src="/images/Edge_Detection/Square_image.png" width="400" >

#### `DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING THE UNIVERSITY OF TEXAS AT ARLINGTON`
