# chrome_explorer

Chrome Explorer (the name is WIP) is an in-development online game that will take place in a Chrome extension. The back-end will be in Python utilizing Flask to package it as a web app, and the front-end will utilize HTML, CSS, Javascript, and potentially Socket.IO if the need arises.

Chrome Explorer is a game that exists somewhere between Pokemon, Pokemon-GO, and Skannerz. It is a Pokemon-style game that uses the internet as its game map. As players traverse the web and hop from site to site, they will encounter different monsters (the name of which is to be determined - cybermon, webbies, phoxmon, etc). They can then use their own monsters to battle the ones they encounter in the wild, strenghtening their own monsters while also adding to their collection each time they find a new one.

## General Structure

When a user turns on the Chrome Explorer extension, it will start pinging the Chrome Explorer server every time a new web address is visited (probably only listening on one tab to avoid confusion/errors). The server will take the URL and identify the domain name, which it will then check against a pre-made list of "Regions" such as Social Media, Video Streaming, News, Search Engine, etc. Much like how different regions of Pokemon have different Pokemon living in them, so too will the different Regions have different monsters lurking as potential encounters.

When the server decides that an encounter with a wild monster will happen, the user will be given the option to engage it or run away. If the user engages, they will find themselves in a Pokemon-style battle (with slight tweaks to mechanics as I see fit). Defeating wild monsters will give your active monster more experience so they can level up, get stronger, and learn new attacks. It will also add any newly encountered monsters to the user's collection.

## Anatomy of the Monster

### Stats

Each monster will have a stat block similar to most RPG characters. The stats will include Strength, Agility, Intelligence, Spirit, Constitution, and Charisma. These stats are used for the following:

Strength will be used to determine the damage of physical attacks.

Agility will determine frequency of attacks and turn order.

Intelligence will determine the potency of magical attacks.

Spirit will determine how much health and mana are regenerated per turn.

Constitution will determine a monster's health and resistances.

Charisma will come into play in some other calculations.

### Types

Like in Pokemon, the monsters here will have different types. This list is very much a work in progress, but some of the potential types are:

* Data
* Virus
* AV (anti-virus)
* Blockchain
* Pirate
* Dark Web
* Meme
* Browser
* Server

These types will have advantages and disadvantages. For example, Virus will be super effective against Data, Meme, Browser, and Server, but it will be only half effective vs Blockchain and AV.

### Abilities

Different monsters will have different passive abilities that will provide different effects inside or outside of combat. These abilities could be any of the following (though they are certainly not limited to the following):

* Increase the rate at which rare monsters are encountered
* Reduces damage from a specific attack type
* Recover a portion of health based on damage dealt

### Attacks

As monsters level up and grow, they will gain access to a wider and more powerful array of attacks. Attacks will be made up of four main parts: Damage, Type, Style, and Effect. Damage is self explanatory and will be calculated alongside a monster's Strength of Intelligence stat to determine the actual damage dealt. Type refers to whether it is the Data type, Virus type, etc. Style differentiates between physical and magical attacks. The attack's effect is whatever happens in addition to raw damage - maybe inflicting a status effect, maybe temporarily raising or lowering a monster's stat.

### Talents

Like in many RPGs, monsters will be able to unlock different talents as they ascend in level. Talents may give access to new attacks, new abilities, or simple stat boosts.

## Combat

Combat is turn-based in the flavor of Pokemon, but with definite tweaks. Note that this is all subject to change during development.

### Turn Order

The two monsters in combat do not choose their actions simultaneously, then have the actions executed in order of speed. Instead, each monster will act on their own turn. Turn order is decided by the following (subject to change):

Every monster will have a speed stat (maybe agility, dexterity). When a battle starts, each monster will gain another attribute called accumulated_speed. Each monster's accumulated_speed will increment by that respective monster's speed, up to a maximum of 100. When a monster hits 100 accumulated_speed, that monster will take its turn. For example:

Cookiemon has a speed of 20, and Dinomon has a speed of 40. When their battle starts, they both have an accumulated_speed of 0. Behind the scenes, their accumulated_speeds incremend by their speeds. After the first incrementation, Cookiemon has 20 accumulated_speed and Dinomon has 40. Neither has 100, so incrementation happens again. Cookiemon goes to 40 AS, Dinomon goes to 80 AS. Incrementation continues this way until Dinomon finally hits 120 AS (with Cookiemon at 60 AS). Dinomon, having hit 100, will take his turn and attack Cookiemon.

Next, the game will reset Dinomon's AS to 20 (he gets to keep the surplus AS over 100), and it will then increment again. Cookiemon then will have 80 AS, and Dinomon will be up to 60. On the next incrementation, they will both hit 100 AS, meaning they both get to act. In the case of ties like this, the monster with the higher base speed will act first. So, Dinomon will take a turn, then Cookiemon will finally act.

The effect of speed and accumulated_speed means that monsters with a higher speed stat will get to attack more often than monsters with a lower speed stat. In this scenario, because Dinomon has a speed stat that is double Cookiemon's speed, Dinomon gets to attack twice as often, with a turn order that will go Dinomon > Dinomon > Cookiemon > repeat.

### Attacks

Each monster will have a repertoire of attacks and abilities at their disposal, much like in Pokemon. However, unlike in Pokemon, monsters will have a resource system akin to mana or energy. Differenet attacks will cost a different amount of resources, which will then regenerate at a certain rate every turn. Like in Pokemon, there will be type advantage/disadvantage of some sort that will double or halve effectiveness of attacks.

### Swapping

Like in Pokemon, a player will be able to spend their action to swap between the active monster and another monster in their party. The utility of switching will be very different than in Pokemon, though. Because the players' turns do not happen simultaneously, you will not be able to switch in a predictive manner. When a monster is on the bench, it will continue to regenerate resources according to its stat block.

## IDEA

Encounter other users who are on the same site as you
maybe flag yourself for pvp