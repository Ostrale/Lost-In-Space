from Lostinspace import *
from time import time

debut = time()
nb_etoile_analyse = 15  # On choisi le nobre d'étoile plus lumineuse pour faire notre analyse khi2


TraitementImage = TraitementImage()
BaseDeDonee = BaseDeDonee()
Compar = Comparaison()

TraitementImage.NomImage("andro.png")
BaseDeDonee.BUILD((0,42,44.33),(41, 16, 7.50))
#TraitementImage.NomImage("pleiadesbruit2.png")
#BaseDeDonee.BUILD((3,45,48),(24, 22, 0))
#TraitementImage.NomImage("siriusbruit.png")
#BaseDeDonee.BUILD((6, 45, 8.9173),(-16, 42, 58.017))

Coordonnees = TraitementImage.CoorEtoileLabel()  # on récupère les coordonnées des étoiles
pause1 = time()
TraitementImage.Affichage()  # on affiche notre image en niveau de gris avec les centre en rouge (optionel)
pause1 = time()-pause1

Coordonnees = TraitementImage.Maxietoile(Coordonnees, 50)
rapport_I = TraitementImage.RapportImage(Coordonnees)  # on fait les rapport pour les comparés à la base de donnée

LesNPlesLumi_B = BaseDeDonee.ListeN(nb_etoile_analyse, angle=2.5)
rapport_B = BaseDeDonee.rapportBaseDeDonnee(LesNPlesLumi_B)  # on fait les rapport pour les comparés à l'image'
pause2 = time()
BaseDeDonee.Affichage()  # on affiche une image de synthèse (optionel)
pause2 = time()-pause2

DicoNDDSKY = Compar.KHI2(rapport_I, rapport_B[0], rapport_B[1])
transformation = Compar.transfos(DicoNDDSKY[0],DicoNDDSKY[1])
bonnetransfo = Compar.vote(transformation)
Letoileestla = Compar.transfoetoile(bonnetransfo)
print(Letoileestla)
pause3 = time()
Compar.Affichage('andro.png')
pause3 = time()-pause3

fin = time()
duree = fin - debut - pause1 - pause2 - pause3
print("Temps d'execution sans les affichages ", duree)
