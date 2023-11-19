# Country Game

A board game to learn about countries while having fun that can be played by one or more players.

## The game

Country Game is a board and cards game that requires the following items :  
- 72 country cards
- one standard 6 faces dice
- one board with a world map (optional)
- a token per player to indicate its position on the world map

### Country cards

Each card contains facts and images about a country.


On the back of the card are 4 pictures of landmarks and the name of the country.


On the front of the card are 2 pictures on the background; the one on top shows the location of the country on earth,
the one below shows a map of the country with the name of neighbour countries, the capital and some other important
cities that allow to locate the landmarks.  
Over those 2 images are displayed informations about the country
- the number of the country (1 to 72)
- Capitals, the administrative capital is underlined 
- Languages, official languages are underlined and when a country has many other languages we add an astrisk `*`
- Population, we diplay 1 to 3 digits and a unit (B: billions, M:millions, K:thousands) for instance `35,588,987` is written `36M`, `1,412,175,000` is written `1.4B` and `56,661` is written `57K`
- Currency, we display only the main currency name and its 3 characters code ([norm ISO 3166-1 alpha-3](https://www.iso.org/obp/ui/#search))
- Landmarks, the layout of the 4 pictures of the back of the card is represented transparently with black borders. In each picture frame we display the name of the landmark and of the closet city you can find on the background map.
- Food and drinks,  3 typical food or drink are dislayed under the landmarks, the name of the dish or drink is displayed in bold font followed by a description.

### Board

The board represents the world map.  
Optionally on the border are displayed the flags of the 72 countries with a number (from 1 to 72)

## Setup

Shuffle the cards and put back face up (the back face is the one showing 4 picture and the country name in the middle).  
If you play with the board place the card stack one the designated place of the board.  
Give a token to each player.

## Rules

Each player plays one after another.  

There are by default 6 categories of questions:
1: Capital
2: Population
3: Languages
4: Currency
5: Landmarks
6: Food and drinks

### Standard Multiplayers version with board

The player looks at the country name on the top of the first card and position his token on the country.

If the country is too small to contain the token, he places the token next to the country.

He then rolls the dice to determine the category of the question he need to answer to earn the card.

If the category was landmarks, the player rolls again the dice until he obtain a number 1 to 4 and 
use this number to determine which of the 4 landmark he has to identify.

If the category was food and drinks, the player rolls again the dice until he obtain a number 1 to 3 and 
use this number to determine which of the 3 food and drinks he has to identify.

The player after him take the card on the stack and check if the answer to the question is correct.

In case the category was food and drinks, he reads aloud to the player the description of the food or drink and
ask the player to provide the name of the dish or drink described.

If the player answered correctly he earns the card and put it in front of him.  
He then checks if the next country on the stack of card can be reached from the country he took by land (that is without having to cross a body of water); if it is the case then he plays again.

If the answer is incorrect then the card is put in the lost country stack (it wont be played again).

The games end when thare are no more card on the stack.

The winner is the one with most cards.

### Ajusting difficulty

If a category is too difficult or not in your liking it can be replaced by the flag category.  
When the player falls on the flag category he need to point to the flag of his country among all the flags displayed in the 
border of the board.  
The other player can then check the answer is correct by verifying the numbers on the flag and on the card match.

You can also decide not to play with some category, let the player choose the landmark he want to identify rather that rolling a dice, etc,...

### Playing without board

The same game can be played without the board, players just have to know if they can go to their current country to
the one on the next card without crossing a body of water. 

### Playing alone

When played alone the goal of the game is to beat one's own record.  
The food and drinks category is replaced by the flag category as described in the section `Adjusting the difficulty` above.

The player verify the answer by himself and proceed to the next card.

### Credits and making off

As any Manaty game "Country Game" is free to use, replicate and modify. You will find in the `src` directory the complete instructions and source code to build your own version.
To help us building new games and new version of our games, please consider donating or buying the commercial versions of the game.