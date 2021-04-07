# Phoxtrot

(previously called Chrome Explorer)

Phoxtrot is an in-development online game that will take place in a Chrome extension. The back-end will be in Python utilizing Flask to package it as a web app, and the front-end will utilize HTML, CSS, Javascript, and potentially Socket.IO if the need arises.

Phoxtrot is a game that exists somewhere between Pokemon, Pokemon-GO, and Skannerz. It is a Pokemon-style game that uses the internet as its game map. As players traverse the web and hop from site to site, they will encounter different monsters (called Phoxes). Players can then use their own Phoxes to battle the ones they encounter in the wild, strenghtening their own Phoxes while also adding to their collection each time they find a new one.

## KNOWN ISSUES THAT NEED TESTING

A lot of this project is really difficult to test while in development. Things that need to be tested once its live:

With the use of sockets, the game is theoretically playable by different people on different computers at the same time. Unfortunately, this is hard/impossible to test without having multiple people with multiple IPs. Similarly, multiple people in the same house/network cannot play at the same time if they have the same IP.

The way that new URLs are currently handled is very wonky. It attempts to take the IP address from whoever contacted the server, but it is currently replying with the IP address of localhost... which isn't right. This may right itself upon deployment, but it may not. For now, a dummy IP address (mine) will be hard-coded into the program to allow for testing and development.

## General Structure

When a user turns on the Chrome Explorer extension, it will start pinging the Phoxtrot server every time a new web address is visited (probably only listening on one tab to avoid confusion/errors). The server will take the URL and identify the domain name, which it will then check against a pre-made list of "Regions" such as Social Media, Video Streaming, News, Search Engine, etc. Much like how different regions of Pokemon have different Pokemon living in them, so too will the different Regions have different Phoxes lurking as potential encounters.

When the server decides that an encounter with a wild Phox will happen, the user will be given the option to engage it or run away. If the user engages, they will find themselves in a Pokemon-style battle (with slight tweaks to mechanics as I see fit). Defeating wild Phoxes will give your active Phox more experience so they can level up, get stronger, and learn new attacks. It will also add any newly encountered Phoxes to the user's collection.

## Anatomy of the Phox

### Stats

Each Phox will have a stat block, not dissimilar to the stat blocks attached to most RPG characters (like Pokemon, for example):

Health: The amount of damage a Phox can withstand before disconnecting

Speed: The frequency with which the Phox will be able to attack 

Cloud Power: The damage that the Phox will do with Cloud attacks (abbreviated to CPOW)

Local Power: The damage that the Phox will do with Local attacks (abbreviated to LPOW)

Cloud Security: The Phox's resistance to Cloud attacks (abbreviated to CSEC)

Local Security: The Phox's resistance to Local attacks (abbreviated to LSEC)

Refresh Rate: The rate at which a Phox regains RAM during battle (abbreviated to RR)

Visibility: Comes into play for specific attacks.

In addition to the more straightforward attack/defense aspects of these stats, some attacks will also incorporate "checks," which are analogous to saves in DnD. Checks will compare one of the attacker's stats against a defender's stat. If the attacker wins the check, some special effect will happen. If the defender wins the check, then the attack fails.

### Familes

Like in Pokemon, the Phoxes here will have different types, here called families. This list is very much a work in progress, but some of the potential familes are:

* Data
* Virus
* AV (anti-virus)
* Blockchain
* Pirate
* Nullset
* Bug
* Meme
* Assembly
* Troll

These familes will have advantages and disadvantages. Attacks with advantage will deal double damage, and attacks with disadvantage will deal half. Phoxes can have up to two types, meaning that attacks can deal anywhere from 4x to 1/4x damage.

### Abilities

Different Phoxes will have different passive abilities that will provide different effects inside or outside of combat. These abilities could be any of the following (though they are certainly not limited to the following):

* Increase the rate at which rare Phoxes are encountered
* Reduces damage from a specific attack type
* Recover a portion of health based on damage dealt

### Attacks

As Phoxes level up and grow, they will gain access to a wider and more powerful array of attacks. Attacks will be made up of four main parts: Damage, Family, Style, and Effect. Damage is self explanatory and will be calculated alongside a Phox's Strength of Intelligence stat to determine the actual damage dealt. Family refers to whether it is the Data family, Virus family, etc. Style differentiates between physical and magical attacks. The attack's effect is whatever happens in addition to raw damage - maybe inflicting a status effect, maybe temporarily raising or lowering a Phox's stat.

### Upgrades

Like in many RPGs, Phoxes will be able to unlock different talents as they ascend in level. Talents may give access to new attacks, new abilities, or simple stat boosts.

## Collection
Like in Pokemon, Phoxes can be collected and trained. The actual collection process, however, will be quite different.

A player will never be able to have more than one of each species of Phox. I never had fun catching multiples of the same Pokemon, so why bother include it as a feature? Breeding was an interesting aspect of Pokemon that I may need to consider, but that is much further down the line.

Instead of weakening a pokemon and using a pokeball and hoping to capture it, players will add a blank slate level 1 Phox to their collection simply by defeating any instance of that Phox's species. This may change to adding a blank slate Phox of the wild Phox's level.

## Combat

Combat is turn-based in the flavor of Pokemon, but with definite tweaks. Note that this is all subject to change during development.

### Turn Order

The two Phoxes in combat do not choose their actions simultaneously, then have the actions executed in order of speed. Instead, each Phox will act on their own turn. Turn order is decided by the following (subject to change):

Every Phox will have a speed stat. When a battle starts, each Phox will gain another attribute called accumulated_speed. Each Phox's accumulated_speed will increment by that respective Phox's speed, up to a maximum of 100. When a Phox hits 100 accumulated_speed, that Phox will take its turn. For example:

Cookiemon has a speed of 20, and Dinomon has a speed of 40. When their battle starts, they both have an accumulated_speed of 0. Behind the scenes, their accumulated_speeds incremend by their speeds. After the first incrementation, Cookiemon has 20 accumulated_speed and Dinomon has 40. Neither has 100, so incrementation happens again. Cookiemon goes to 40 AS, Dinomon goes to 80 AS. Incrementation continues this way until Dinomon finally hits 120 AS (with Cookiemon at 60 AS). Dinomon, having hit 100, will take his turn and attack Cookiemon.

Next, the game will reset Dinomon's AS to 20 (he gets to keep the surplus AS over 100), and it will then increment again. Cookiemon then will have 80 AS, and Dinomon will be up to 60. On the next incrementation, they will both hit 100 AS, meaning they both get to act. In the case of ties like this, the Phox with the higher base speed will act first. So, Dinomon will take a turn, then Cookiemon will finally act.

The effect of speed and accumulated_speed means that Phoxes with a higher speed stat will get to attack more often than Phoxes with a lower speed stat. In this scenario, because Dinomon has a speed stat that is double Cookiemon's speed, Dinomon gets to attack twice as often, with a turn order that will go Dinomon > Dinomon > Cookiemon > repeat.

### Attacks

Each Phox will have a repertoire of attacks and abilities at their disposal, much like in Pokemon. However, unlike in Pokemon, Phoxes will have a resource system akin to mana or energy. Differenet attacks will cost a different amount of resources, which will then regenerate at a certain rate every turn. Like in Pokemon, there will be type advantage/disadvantage of some sort that will double or halve effectiveness of attacks.

### Swapping

Like in Pokemon, a player will be able to spend their action to swap between the active Phox and another Phox in their party. The utility of switching will be very different than in Pokemon, though. Because the players' turns do not happen simultaneously, you will not be able to switch in a predictive manner. When a Phox is on the bench, it will continue to regenerate resources according to its stat block.

## Future Goals

The immediate goal is to get the game up and running so that a player can have a single player experience. This includes:

* Account creation and login ability
* Generate encounters as they go through the internet
* Full combat in those encounters
* Adding defeated Phoxes to player collection
* Leveling up and choosing talents for Phoxes
* Ability to swap out Phoxes in your party/collection
* Display basic info about each Phox

When all of this is accomplished, phase 1 of the game development will be complete. However, I have multiple extended goals for what I want to be in the game:

### PvP
If a player chooses to do so, they can flag themselves for PvP (perhaps will be mandatory in some regions). If they do so, they will be able to encounter other actual players who are in their same region.

### Gyms
The game would be much more fun with some sense of story or progression through it. Eventually, it would be cool for each region to have their own gym like in Pokemon, and for players to be able to progress from region to region.

### Trading and Challenging
Players should be able to interact with their friends! It would be great if they can challenge each other. Trading would be neat too, but I think it may not make sense considering how collection works.
