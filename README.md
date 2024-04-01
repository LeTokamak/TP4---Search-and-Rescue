# Présentation en Français
Projet étudiant dans le cadre d'un cours sur les systèmes multi-agents, appliqué en particulier à la robotique.

## Objectif
L'objetif de ce projet est de sauver une personne perdu dans un labyrinthe, pour cela, il faut lui apporter deux objets (des RescueItem) le plus vite possible.
Les positions des objets et de la personne sont inconnus, mais la structure du labyrinthe est connue.
Nous disposons de 15 d'argent pour acheter autant de robot que l'on souhaite, afin de former notre flotte de sauveteur.
Une fois que nous auront choisit notre flotte, nous devront programmer tous les robots qu'elle contient.
Voici la liste des robots achetables :
- **Rover** (5 argents) : Robot se déplaçant lentement et pouvant transporter un objet.
- **Speeder** (8 argents) : Robot se déplaçant rapidement et pouvant transporter un objet.
- **Climber** (3 argents) : Robot pouvant escalader les murs mais ne pouvant pas déplacer d'objets.
- **Ballon** (3 argents) : Robot volant, très lent, ne pouvant pas déplacer d'objets mais ayant une très bonne vision.

## Notre travail
Nous formions un groupe de trois, et nous avons chacun opter pour une stratégie :
- **SCC** (Speeder, Climber, Climber)
- **SCB** (Speeder, Climber, Ballon)
- **RCBB** (Rover, Climber, Ballon, Ballon)


