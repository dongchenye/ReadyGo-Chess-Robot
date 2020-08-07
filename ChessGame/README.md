<img src="./UI workflow.png" width="700" >

### <a name="install"></a>Installing 

**Install**:
1. Download the "Chess Game" zip file.
2. Unzip the zipfile


### <a name="running"></a> Running 

#### Important Note 1 (before runing): 

1. Go to "ChessEng.py"
2. Find the following line:
```
self.engine = chess.engine.SimpleEngine.popen_uci("/Users/dongchenye/Desktop/Senior Design/Chess Game/stockfish-11-64")
```
3. change the path into your own path:
```
self.engine = chess.engine.SimpleEngine.popen_uci(""your own path"/Chess Game/stockfish-11-64")
```
#### Important Note 2 (before runing): 

By default, in the `OOPGUI_revised.py` file, the test mode is on : `test_flag = True`.
When test mode is on, this will ignore the camera input, and ask the player input on command line.
For example: 
when the "PlayerMovePage" is displayed, click "Done" buttom, then on command line, it will ask you for input.`Please input your next move (ex: 'e2e4'):`. And display the board, after the move is made.

If you want to turn off the test mode, go to `OOPGUI_revised.py` file, change 'test_flag' from 'True' to 'False' 
```
test_flag = False
```

#### Running
* Open a command line terminal, and activate the virtual environment with `source chess_env/bin/activate`
* Go to this `./Chess Game` folder 
* Type in command line with following code:  
```
python3 OOPGUI_revised.py 
``` 
