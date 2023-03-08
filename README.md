# Chess In Python

### Experience the beauty of chess with incredibly human-like AI! This game promises an unforgettable experience. Try it out for yourself now!
#### There are 4 game options:

- Ranked match
- Game vs AI (as black or white)
- Play against a friend
- You can upload your own board

#### This game has a user-friendly GUI that includes the main menu and settings. Also, the interface has 4 languages that can be easily switched in one click.
#### You can customize the AI difficulty level, piece set and board theme!
![menu_preview](https://user-images.githubusercontent.com/103107451/221137231-99fecfce-21f6-473c-93e8-107b2353c46a.jpg)


## Requirements for launch
You need Python 3.8+ and the following modules: ctypes, subprocess, multiprocessing, random (built-in Python modules); and [pygame](https://pypi.org/project/pygame/).

If you don't have the pygame package, use pip (in a terminal or command line) to install it:
```bash
pip install pygame
```


## Launching
Go to the game folder through the terminal and run the main.py file:

On Windows:
```bash
python .\main.py
```
On Linux/MacOS:
```bash
python3 .\main.py
```


## Customization
You can add your own piece set and board theme. To do this, you need to upload your files in ***images/piece_custom/*** and ***images/board_custom/*** folders. 

After completing the previous step, make sure your files are named correctly so that the game engine can use them. You can find out the file names by looking at the ***images/default/*** and ***images/board_classic/*** folders.

After that, go to the ***game_engine/game_objects.py*** file and change lines 31 and 32 of the code by adding the folder names to the lists.
