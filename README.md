# chrome_explorer

Chrome Explorer (the name is WIP) is an in-development online game that will take place in a Chrome extension. The back-end will be in Python utilizing Flask to package it as a web app, and the front-end will utilize HTML, CSS, Javascript, and potentially Socket.IO if the need arises.

Chrome Explorer is a game that exists somewhere between Pokemon, Pokemon-GO, and Skannerz. It is a Pokemon-style game that uses the internet as its game map. As players traverse the web and hop from site to site, they will encounter different monsters (the name of which is to be determined - cybermon, webbies, phoxmon, etc). They can then use their own monsters to battle the ones they encounter in the wild, strenghtening their own monsters while also adding to their collection each time they find a new one.

## General Structure

When a user turns on the Chrome Explorer extension, it will start pinging the Chrome Explorer server every time a new web address is visited (probably only listening on one tab to avoid confusion/errors). The server will take the URL and identify the domain name, which it will then check against a pre-made list of "Regions" such as Social Media, Video Streaming, News, Search Engine, etc. Much like how different regions of Pokemon have different Pokemon living in them, so too will the different Regions have different monsters lurking as potential encounters.

When the server decides that an encounter with a wild monster will happen, the user will be given the option to engage it or run away. If the user engages, they will find themselves in a Pokemon-style battle (with slight tweaks to mechanics as I see fit). Defeating wild monsters will give your active monster more experience so they can level up, get stronger, and learn new attacks. It will also add any newly encountered monsters to the user's collection.