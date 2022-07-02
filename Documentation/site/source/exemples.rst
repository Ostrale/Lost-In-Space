Exemples
========

Vous trouverez ici des exemples d'utilisation de nos programmes.
Attention, il est possible que certaines images proviennent d'anciennes versions du programme, si cela n'est pas encore fait, nous ferons notre possible pour actualiser ces dernières.



Exemple détection taches
-------------

.. NOTE::

    Nous allons utiliser cette image avec deux méthodes différentes (andro.png)

.. image:: images/andro.png
        :height: 600
        :scale: 50
        :align: center
        :alt: andromède

Avec CoorEtoileLabel
____________________

.. code-block:: python
    :linenos:

    from Lostinspace import *
    TraitementImage = TraitementImage()
    TraitementImage.image = 'andro.png'
    Coordonnees = TraitementImage.CoorEtoileLabel()  # on récupère les coordonnées des étoiles
    TraitementImage.Affichage()  # on affiche notre image en niveau de gris avec les centres en rouge (optionnel)

.. image:: images/androfigure1.png
        :height: 600
        :scale: 50
        :align: center
        :alt: résultat andromède Gaussian

Avec Gaussian
_____________

.. code-block:: python
    :linenos:

    from Lostinspace import *
    TraitementImage = TraitementImage()
    TraitementImage.image = 'andro.png'
    Coordonnees = TraitementImage.CoorEtoileGaussian()  # on récupère les coordonnées des étoiles
    TraitementImage.Affichage()  # on affiche notre image en niveau de gris avec les centres en rouge (optionnel)

.. image:: images/androfigure2.png
        :height: 600
        :scale: 50
        :align: center
        :alt: résultat andromède Label

Exemple complet
-------------

Voici comment détecter simplement un astre sur une image

.. code-block:: python
    :linenos:

    from Lostinspace import *
    nb_etoile_analyse = 15  # On choisit le nombre d'étoiles les plus lumineuses pour effectuer notre analyse khi2

    TraitementImage = TraitementImage()
    BaseDeDonee = BaseDeDonee()
    Compar = Comparaison()

    Coordonnees = TraitementImage.CoorEtoileLabel()  # on récupère les coordonnées des étoiles
    TraitementImage.Affichage()  # on affiche notre image en niveau de gris avec les centres en rouge (optionnel)

    Coordonnees = TraitementImage.Maxietoile(Coordonnees, 50)
    rapport_I = TraitementImage.RapportImage(Coordonnees)  # on fait les rapports pour les comparer à la base de donnée

    LesNPlesLumi_B = BaseDeDonee.ListeN(nb_etoile_analyse)
    rapport_B = BaseDeDonee.rapportBaseDeDonnee(LesNPlesLumi_B)  # on fait les rapports pour les comparer à l'image
    BaseDeDonee.Affichage()  # on affiche une image de synthèse (optionnel)

    DicoNDDSKY = Compar.KHI2(rapport_I, rapport_B[0], rapport_B[1])
    transformation = Compar.transfos(DicoNDDSKY[0],DicoNDDSKY[1])
    bonnetransfo = Compar.vote(transformation)
    Letoileestla = Compar.transfoetoile(bonnetransfo)
    Compar.Affichage()

.. NOTE::

    Par défaut, nous cherchons la Nébuleuse du Crabe sur l'image contenant la Nébuleuse du Crabe, celle-ci se situe en haut à droite de la plus grosse étoile (au centre). Finalement, cette dernière est localisée par le programme avec une croix bleue sur l'affichage final.

.. image:: images/Figure_1.png
        :height: 600
        :scale: 50
        :align: center
        :alt: Figure_1

.. image:: images/Figure_2.png
        :height: 600
        :scale: 50
        :align: center
        :alt: Figure_2

.. image:: images/Figure_3.png
        :height: 600
        :scale: 50
        :align: center
        :alt: Figure_3