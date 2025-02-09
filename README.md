dit is de readme van het game project door maarten bernhard

de game heet "maze game" en is gebasseerd op pac-man

benodigde library: pygame
om pygame te installeren voor je de volgende code in bij cmd:
pip install pygame

install guide:
0 download en install pygame
1 maak een folder genaamd maze_game (naam kan anders zijn maar dit is aanbevolen)
2 download alle files van github
3 maak 2 folders genaamd "levels" en "assets", let erop dat ze maze_game genest zijn en niet in elkaaar.
4 verplaats "level1.txt" t/m "level5.txt" naar het "levels" folder
5 open main.py met thonny
6 run main.py
comment: het assets folder blijft leeg, dit is voor toekomstige textures


het spel heeft 5 levels met 1 of 2 doelen per level, als er 2 doelen zijn kan je zelf kiezen wat je doet.
Het uiteindelijke doel is om zoveel mogelijk coins te verzamelen binnen de tijdlimiet van 60 seconden, de levels worden progressief moeilijker en groter.
Elke coin geeft 10 punten, het eind scherm na level 5 laat zien hoeveel coins en punten je hebt gehaald.

Elk level heeft 1 of meerdere enemies, de enemies bewegen op een vast traject op de X-as,
de enemies pakken je niet als je stil blijft staan maar wel als je tegen ze aan loopt.
Soms is het noodzaklijk om de enemie door jou heen te laten gaan om bij een coin te komen.

de meerderheid van de code is door chatgpt geschreven, alle bugfixes zijn door mij gedaan.
Ik heb ervoor gekozen om alle bugfixes zelf te doen zodat ik blijf begrijpen hoe de code werkt en ik deze zelf ook kan aanpassen,
ziehier de link naar mijn chat: https://chatgpt.com/share/67a8a6e3-13cc-800b-9997-46adcb1e8d15
de link bevat een vrij lang gesprek met chatgpt.

controls:
om je player te bewegen gebruik je de arrow keys, dit zijn de enige controls die je player nodig heeft, 
om naar het volgende level te gaan (kan alleen als je het huidige hebt gehaald) druk je op enter.
Als je alle 5 levels hebt uitgespeeld kan je met escape uit het spel gaan.

-Maarten Bernhard

