# Lost-In-Space
Matches a celestial object (example: stars) of a region with an image of this same region

.. WARNING::

      This Readme is in french

Exemples
========

Vous trouverez ici des exemples d'utilisation de nos programmes.
Attention, il est possible que certaines images proviennent d'anciennes versions du programme, si cela n'est pas encore fait, nous ferons notre possible pour actualiser ces dernières.



Exemple détection taches
-------------

.. NOTE::

    Nous allons utiliser cette image avec deux méthodes différentes (andro.png)

![alt text](https://github.com/Ostrale/Lost-In-Space/blob/master/Documentation/site/build/html/images/andro.png?raw=true)

Avec CoorEtoileLabel
____________________

.. code-block:: python
    :linenos:

    from Lostinspace import *
    TraitementImage = TraitementImage()
    TraitementImage.image = 'andro.png'
    Coordonnees = TraitementImage.CoorEtoileLabel()  # on récupère les coordonnées des étoiles
    TraitementImage.Affichage()  # on affiche notre image en niveau de gris avec les centres en rouge (optionnel)

![alt text](https://github.com/Ostrale/Lost-In-Space/blob/master/Documentation/site/build/html/images/androfigure1.png?raw=true)
       

Avec Gaussian
_____________

.. code-block:: python
    :linenos:

    from Lostinspace import *
    TraitementImage = TraitementImage()
    TraitementImage.image = 'andro.png'
    Coordonnees = TraitementImage.CoorEtoileGaussian()  # on récupère les coordonnées des étoiles
    TraitementImage.Affichage()  # on affiche notre image en niveau de gris avec les centres en rouge (optionnel)

![alt text](https://github.com/Ostrale/Lost-In-Space/blob/master/Documentation/site/build/html/images/androfigure2.png?raw=true)

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

![alt text](https://github.com/Ostrale/Lost-In-Space/blob/master/Documentation/site/build/html/images/Figure_1.png?raw=true)

![alt text](https://github.com/Ostrale/Lost-In-Space/blob/master/Documentation/site/build/html/images/Figure_2.png?raw=true)

![alt text](https://github.com/Ostrale/Lost-In-Space/blob/master/Documentation/site/build/html/images/Figure_3.png?raw=true)


Exigences
=========

.. IMPORTANT::

    Merci de lire attentivement les exigences pour ne rencontrer aucun problème lors de l'utilisation.

Bibliothèque
------------

Tableau regroupant les exigences d'installation du programme Lost in Space.

    +--------------+---------------------------+
    | bibliothèque | installation              |
    +==============+===========================+
    | numpy        | pip install numpy         |
    +--------------+---------------------------+
    | cv2          | pip install opencv-python |
    +--------------+---------------------------+
    | mathplotlib  | pip install mathplotlib   |
    +--------------+---------------------------+
    | itertools    | X inclu                   |
    +--------------+---------------------------+
    | skyfield     | pip install skyfield      |
    +--------------+---------------------------+
    | os           | X inclu                   |
    +--------------+---------------------------+
    | astropy      | pip install astropy       |
    +--------------+---------------------------+
    | pandas       | pip install pandas        |
    +--------------+---------------------------+
    | skimage      | pip install scikit-image  |
    +--------------+---------------------------+

.. NOTE::

    X inclu indique de bibliothèque déja incluse dans Python, il n'est donc pas nécessaire d'installation.

.. WARNING::

    Attention, nous déconseillons fortement l'utilisation d'Anaconda et de Spider.
    Si malgré tout, vous souhaitez installer ces bibliothèques dans Anaconda, depuis l'invité de commande de Anaconda, veillez à remplacer 'pip' par 'conda'.

Erreurs Fréquentes (débutant)
------------------

Résoudre 'pip' n'est pas reconnu en tant que commande interne sur Windows 10.
Pour résoudre cette erreur :
https://www.youtube.com/watch?v=pjCWtppLN3k&ab_channel=foxxpy

<div itemprop="articleBody">
            
  <div class="section" id="documentation">
<h1>Documentation<a class="headerlink" href="#documentation" title="Lien permanent vers ce titre">¶</a></h1>
<p>Lost in Space : Retrouve une étoile sur une image</p>
<div class="section" id="traitement-image">
<h2>Traitement Image<a class="headerlink" href="#traitement-image" title="Lien permanent vers ce titre">¶</a></h2>
<dl class="py class">
<dt id="Lostinspace.TraitementImage">
<em class="property"><span class="pre">class</span> </em><code class="sig-prename descclassname"><span class="pre">Lostinspace.</span></code><code class="sig-name descname"><span class="pre">TraitementImage</span></code><a class="headerlink" href="#Lostinspace.TraitementImage" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Classe Traitement Image permettant de réaliser un traitement”
d’une image d’un ciel étoilé. Cette image traité peu ensuite
être analysée
Méthodes : NomImage, CoorEtoileLabel, CoorEtoileGaussian, Affichage, Maxietoile, RapportImage</p>
<dl class="py method">
<dt id="Lostinspace.TraitementImage.Affichage">
<code class="sig-name descname"><span class="pre">Affichage</span></code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.TraitementImage.Affichage" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Un affichage de l’image en niveau de gris avec des cercle entourant les zones détecté si une
méthode de détection à été utilisé</p>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.TraitementImage.CoorEtoileGaussian">
<code class="sig-name descname"><span class="pre">CoorEtoileGaussian</span></code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.TraitementImage.CoorEtoileGaussian" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Permet de connaître la position et la taille de chaque étoiles de l’image analysée
Pour se faire on utilise la fonction Gaussian <a class="reference external" href="https://en.wikipedia.org/wiki/Blob_detection#The_Laplacian_of_Gaussian">https://en.wikipedia.org/wiki/Blob_detection#The_Laplacian_of_Gaussian</a></p>
<dl class="field-list simple">
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>list</p>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Liste des des étoiles sous le format (x,y,sigma) position x , position y , sigma / info : sigma*(2)**0.5 envrion égale à rayon</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.TraitementImage.CoorEtoileLabel">
<code class="sig-name descname"><span class="pre">CoorEtoileLabel</span></code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.TraitementImage.CoorEtoileLabel" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Permet de connaître la position et la taille de chaque étoiles de l’image analysée
Pour se faire on utilise la fonction Label <a class="reference external" href="https://en.wikipedia.org/wiki/Connected-component_labeling">https://en.wikipedia.org/wiki/Connected-component_labeling</a></p>
<dl class="field-list simple">
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>list</p>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Liste des des étoiles sous le format (x,y,r) position x , position y , rayon</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.TraitementImage.Maxietoile">
<code class="sig-name descname"><span class="pre">Maxietoile</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">liste_etoile</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">nb</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">50</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.TraitementImage.Maxietoile" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Sélectionne les nb plus grandes étoiles (théoriquement les nb plus lumineuse) et 
les renvoies dans l’ordre décroissant.</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>liste_etoile</strong> – list =&gt; Liste d’étoiles sous le format (x,y,r/sigma).</p></li>
<li><p><strong>nb</strong> – int =&gt; nombre d’étoile a sélectionner dans la liste.</p></li>
</ul>
</dd>
</dl>
<dl class="field-list simple">
<dt class="field-odd">Renvoie</dt>
<dd class="field-odd"><p>Renvoie une liste des étoiles les plus lumineuses de nb élément dans l’ordre décroissant.</p>
</dd>
<dt class="field-even">Type renvoyé</dt>
<dd class="field-even"><p>list</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.TraitementImage.NomImage">
<code class="sig-name descname"><span class="pre">NomImage</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nom</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.TraitementImage.NomImage" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Permet de définir le nom de l’image à analyser. Attention ! ne pas oublier l’extension
Cette image serra utiliser pour l’ensemble des fonction de la classe TraitementImage</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><p><strong>nom</strong> – str =&gt; nom de l’image à analyser, exemple “crabe.png” .</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.TraitementImage.RapportImage">
<code class="sig-name descname"><span class="pre">RapportImage</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">liste_étoile</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.TraitementImage.RapportImage" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Permet de créer des rapports grace à 3 points formant un triangles les rapports sont petit coté / grand coté et  moyen coté / grand coté</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><p><strong>liste_étoile</strong> – list =&gt; Liste d’étoiles sous le format (x,y,r/sigma).</p>
</dd>
</dl>
<dl class="field-list simple">
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>dict</p>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Renvoie un dictionnaire contenant un tuple de rapports et leurs erreurs (r1,dr1,r2,dr2) en clé associé à un tuple contenant des trios d’étoiles chacune caractérisée pas des coordonnées cartésiennes (xi,yi,ri/sigmai).</p>
</dd>
</dl>
<p>Exemple : dico={(r1,dr1,r2,dr2): ((x1,y1,r1),(x2,y2,r2),(x3,y3,r3))…}</p>
</dd></dl>

</dd></dl>

</div>
<div class="section" id="base-de-donee">
<h2>Base De Donee<a class="headerlink" href="#base-de-donee" title="Lien permanent vers ce titre">¶</a></h2>
<dl class="py class">
<dt id="Lostinspace.BaseDeDonee">
<em class="property"><span class="pre">class</span> </em><code class="sig-prename descclassname"><span class="pre">Lostinspace.</span></code><code class="sig-name descname"><span class="pre">BaseDeDonee</span></code><a class="headerlink" href="#Lostinspace.BaseDeDonee" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Classe qui concerne tout ce qui se rapporte à la Base de Données. 
A savoir, l’importation des coordonnées des étoiles dans la région observée 
et le calcul des rapports des triangles formées à partir de ses étoiles</p>
<p>Méthodes: Build, ListeN, rapportBaseDeDonnee, Affichage</p>
<dl class="py method">
<dt id="Lostinspace.BaseDeDonee.Affichage">
<code class="sig-name descname"><span class="pre">Affichage</span></code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.BaseDeDonee.Affichage" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Un affichage de la base de donnees (une image)</p>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.BaseDeDonee.BUILD">
<code class="sig-name descname"><span class="pre">BUILD</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">Adroite</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">Declinaison</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.BaseDeDonee.BUILD" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Initialise les coordonnées de l’objet que l’on veut observer en équatoriale = (h,m,s),(°,”,””) = (heure minute seconde) et (Degree Minute d’arc Seconde d’arc)
Exemple  (5, 34, 31.97),(22, 0, 52.1) Coordonnées nébuleuse du Crabe</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>Adroite</strong> – tuple =&gt; les coordonnées de l’objet que l’on veut observer heure minute seconde.</p></li>
<li><p><strong>Declinaison</strong> – tuple =&gt; les coordonnées de l’objet que l’on veut observer Degree Minute d’arc Seconde d’arc.</p></li>
</ul>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.BaseDeDonee.ListeN">
<code class="sig-name descname"><span class="pre">ListeN</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">n</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">angle</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">2.5</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.BaseDeDonee.ListeN" title="Lien permanent vers cette définition">¶</a></dt>
<dd><dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>n</strong> – int =&gt; nombre d’étoile a sélectionner dans la Base de Données.</p></li>
<li><p><strong>angle</strong> – float =&gt; valeur du rayon du cercle autour de l’astre à observer pour une image 5°x5° il faut donner 2.5.</p></li>
</ul>
</dd>
</dl>
<dl class="field-list simple">
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>list</p>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Une liste des étoiles les plus lumineuses dans l’ordre décroissant</p>
</dd>
</dl>
<p>format : (x,y,magnitude)</p>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.BaseDeDonee.rapportBaseDeDonnee">
<code class="sig-name descname"><span class="pre">rapportBaseDeDonnee</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">image</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.BaseDeDonee.rapportBaseDeDonnee" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Permet de créer des rapports grace à 3 points formant un triangles les rapports sont :
petit coté / grand coté et  moyen coté / grand coté</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><p><strong>image</strong> – list =&gt; liste des étoiles au format : (x,y,magnitude).</p>
</dd>
</dl>
<dl class="field-list simple">
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>tuple</p>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Deux éléments :</p>
</dd>
</dl>
<p>Renvoie un dictionnaire contenant un tuple de rapports (r1,r2) en clé associé à un tuple 
contenant des trios d’étoiles chacune caractérisée pas des coordonnées gnomoniques (xi,yi).</p>
<blockquote>
<div><p>Exemple : dico={(r1,r2): ((x1,y1),(x2,y2),(x3,y3))…}</p>
</div></blockquote>
<p>Renvoie aussi une liste composée des coordonnées (xi,yi) et magnitude (Mi) 
des toutes les étoiles de la région observée</p>
<blockquote>
<div><p>Exemple : image=[(x1,y1,M1),(x2,y2,M2)]</p>
</div></blockquote>
</dd></dl>

</dd></dl>

</div>
<div class="section" id="comparaison">
<h2>Comparaison<a class="headerlink" href="#comparaison" title="Lien permanent vers ce titre">¶</a></h2>
<dl class="py class">
<dt id="Lostinspace.Comparaison">
<em class="property"><span class="pre">class</span> </em><code class="sig-prename descclassname"><span class="pre">Lostinspace.</span></code><code class="sig-name descname"><span class="pre">Comparaison</span></code><a class="headerlink" href="#Lostinspace.Comparaison" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Classe qui s’occupe de comparée l’image à la base de donnée</p>
<dl class="py method">
<dt id="Lostinspace.Comparaison.Affichage">
<code class="sig-name descname"><span class="pre">Affichage</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">image</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'crabe.png'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.Affichage" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Un affichage de deux triangles, si les triangles sont similaires c’est que la transformation est réussite, s’ils ne le sont pas cela n’a pas forcément échoué
Affiche 2 triangles qui s’ils sont similaires montrent que la transformation est un succès</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><p><strong>image</strong> – str =&gt; image de fond, mettre la même que l’image analysé pour un bon visuel.</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.Comparaison.AstreCherche">
<code class="sig-name descname"><span class="pre">AstreCherche</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">tuplecoo</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.AstreCherche" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Permet de décaller le centre de la base de données
En 0,0 nous somme centrée</p>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.Comparaison.KHI2">
<code class="sig-name descname"><span class="pre">KHI2</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">enzo</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dico</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">imagetrilumi</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.KHI2" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Applique la formule du Khi2 afin de comparer les rapports de l’image et ceux de la base de données</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>enzo</strong> – dict =&gt; Returns de la méthode rapport image dans la class TraitementImage</p></li>
<li><p><strong>dico</strong> – dict =&gt; Returns de la méthhode rapportBaseDeDonnee dans la class BaseDeDonnee</p></li>
</ul>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>2 listes Lbdd et Lima qui contiennent les étoiles de la base de données et de l’image qui correspondent entre elles</p>
</dd>
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>tuple</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.Comparaison.transfo">
<code class="sig-name descname"><span class="pre">transfo</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ebdd</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">eima</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.transfo" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Applique des formules d’homothétie à savoir une translation une rotation et une mise à l’échelle afin de déterminer une transformation géométrique
qui permettrait de passer de la base de données à l’image.</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>ebdd</strong> – list =&gt; Correspond à la liste des triangles formés à partir de la base de données dans la méthode transfos.</p></li>
<li><p><strong>eima</strong> – list =&gt; Correspond à la liste des triangles formés à partir de l’image dans la méthode transfos.</p></li>
</ul>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Eqaution: Dictionnaire contenant les variables de la fonction de transfert, e: les coordonnées de l’astre cherché (en cartésien pixel) , aff: ensemble de données utiles à l’affichage.</p>
</dd>
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>tuple</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.Comparaison.transfoetoile">
<code class="sig-name descname"><span class="pre">transfoetoile</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">transfo</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.transfoetoile" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Applique les tranformation à d’autres points</p>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.Comparaison.transfos">
<code class="sig-name descname"><span class="pre">transfos</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">lbdd</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">lima</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.transfos" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>regroupe les étoiles déterminées par le khi2 par trois afin d’en faire des triangles Aussi bien pour Lbdd que pour Lima.</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>Lbdd</strong> – list =&gt; Liste regroupant les étoiles de la base de données retenues.</p></li>
<li><p><strong>Lima</strong> – list =&gt; Liste regroupant les étoiles de l’Image retenue.</p></li>
</ul>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Une liste qui contient la liste des transformations créées à l’aide de la méthode transfo.</p>
</dd>
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>list</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt id="Lostinspace.Comparaison.vote">
<code class="sig-name descname"><span class="pre">vote</span></code><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">EE</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#Lostinspace.Comparaison.vote" title="Lien permanent vers cette définition">¶</a></dt>
<dd><p>Algorithme de vote classique qui détermine la transformation géométrique la plus réaliste.</p>
<dl class="field-list simple">
<dt class="field-odd">Paramètres</dt>
<dd class="field-odd"><p><strong>EE</strong> – list =&gt; liste des transformations déterminées à l’aide des méthodes transfos et transfo.</p>
</dd>
<dt class="field-even">Renvoie</dt>
<dd class="field-even"><p>Dictionnaire contenant les variables de la transformation retenue.</p>
</dd>
<dt class="field-odd">Type renvoyé</dt>
<dd class="field-odd"><p>dict</p>
</dd>
</dl>
</dd></dl>

</dd></dl>

</div>
</div>

</div>
