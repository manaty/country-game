This directory contain the source code for the html version of the game


## Splash and menu screen

While loading a splash screen display the cover image.  
The menu screen contains a menu to start a game, read the rules, access settings, and access credits

## Start game screen

A screen list the player names and color.  
By default there is one player, the player names are "Player 1", "Player 2",... and the color is randomly selected. 
A button allow to add players.  
On the right of the row displaying player's name and color a "trashcan" icon allow to delete a player (the last player cannot be deleted).  
A "Back" button allow to return to the menu  
A "Start" button allow to start the game

## Game screen

The game screen is divided in two part, a header and the board.
The header contains the current turn player name, its score a menu button to display game menu. 
When a it is a players turn to play a new country name is displayed in the header.
The user can then move his Pin (that has his color) to the location of the country in the board.
If he select the correct country he gets a point, if not a sound and text notify that he missed.
If then through a dice and his presented with the question of the country card that match the number on his dice.
A timer is started for 30 seconds.
After the timer elapse, the card answers are shown and the user select if his answer was correct or no.
IF the question is answered correctly the player earns another point.
If the next country can be accessed by land from his present location and his previous answer was correct then player can play again, if not it is the next player turn.
The game end when all the countries are played.

### Game menu
The game menu show the scores of each players, the country they earns.
A "End game" button allow to return to the menu screen. 

## Rules screen
This screen display the rules of the game.
A "Back" button allow to return to the menu screen.

## Credits screen
This screen display the credits of the game.
A "Back" button allow to return to the menu screen.