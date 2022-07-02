"""
Lost in Space : Retrouve une étoile sur une image
"""
from Dependance import *
from time import time

class TraitementImage:
    """Classe Traitement Image permettant de réaliser un traitement'
    d'une image d'un ciel étoilé. Cette image traité peu ensuite
    être analysée
    Méthodes : NomImage, CoorEtoileLabel, CoorEtoileGaussian, Affichage, Maxietoile, RapportImage"""

    def __init__(self):
        """
        initialisation des variables de la classe TraitementImage

        list liste_etoile  => Une liste contenant les coordonnées et le rayon de chaque étoiles (x,y,r).
        str image =  => l'image analysée.
        """

        self.liste_etoile = []
        self.image = "crabe.png"

    def __CoorEtoile(self):
        """
        lecture de l'image et calcul du seuil de luminosité pour les méthode de reconaissances d'étoiles CoorEtoileLabel et CoorEtoileGaussian
        """
        self.image = cv2.imread(self.image)  # image a transformer
        self.image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # transformation en niveau de gris
    
    def NomImage(self, nom):
        """
        Permet de définir le nom de l'image à analyser. Attention ! ne pas oublier l'extension
        Cette image serra utiliser pour l'ensemble des fonction de la classe TraitementImage

        Parameters
        ----------
        :param nom: str => nom de l'image à analyser, exemple 'crabe.png' .
        """

        self.image = nom

    def CoorEtoileLabel(self):
        """ 
        Permet de connaître la position et la taille de chaque étoiles de l'image analysée
        Pour se faire on utilise la fonction Label https://en.wikipedia.org/wiki/Connected-component_labeling

        Returns
        -------
        :rtype: list
        :returns: Liste des des étoiles sous le format (x,y,r) position x , position y , rayon 
        """

        self.__CoorEtoile()
        self.threshold = threshold_yen(self.image_gray)
        bw = closing(self.image_gray > self.threshold , square(2))
        cleared = clear_border(bw)
        self.image_gray = (255 - self.image_gray)  # négatif de notre image le noir sont nos étoiles
        self.label_image = label(cleared)
        liste_étoile = []
        for region in regionprops(self.label_image):
            # take regions with large enough areas
            if region.area >= 1:
                r = region.equivalent_diameter/2
                x,y = region.centroid
                liste_étoile.append((y,x,r))
        self.liste_etoile = liste_étoile
        print("Cette image contient {} étoiles.".format(len(liste_étoile)))
        return liste_étoile

    def CoorEtoileGaussian(self):
        """ 
        Permet de connaître la position et la taille de chaque étoiles de l'image analysée
        Pour se faire on utilise la fonction Gaussian https://en.wikipedia.org/wiki/Blob_detection#The_Laplacian_of_Gaussian

        Returns
        -------
        :rtype: list
        :returns: Liste des des étoiles sous le format (x,y,sigma) position x , position y , sigma / info : sigma*(2)**0.5 envrion égale à rayon 
        """

        self.__CoorEtoile()
        self.threshold = threshold_otsu(self.image_gray)/256
        self.blobs_log = blob_log(self.image_gray,max_sigma=80,num_sigma=150,threshold=self.threshold ,overlap=0.6,exclude_border=True)
        self.image_gray = (255 - self.image_gray)  # négatif de notre image le noir sont nos étoiles
        liste_étoile = []
        for elem in self.blobs_log:
            (x, y, sigma) = elem[1], elem[0], elem[2]
            if (elem[2] < 10000):  # a changer mettre valeur plus juste avec test mais cela change en fonction d ela lunete
                liste_étoile.append((x, y, sigma))
            else:  # ce n'est pas une étoile (c'est un nuage, un amas par exemple)
                print((x, y, sigma),"(x,y,sigma) a été suppr car il n'a pas été considéré comme une étoile",)
        self.liste_etoile = liste_étoile
        print("Cette image contient {} étoiles.".format(len(liste_étoile)))
        return liste_étoile

    def Affichage(self):
        """
        Un affichage de l'image en niveau de gris avec des cercle entourant les zones détecté si une
        méthode de détection à été utilisé
        """

        image = self.image_gray
        fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=(16, 8), sharex=True, sharey=True)
        ax.set_title("La détection d'étoiles par Lost in Space")
        ax.imshow(image, cmap=plt.cm.gray)
        for elem in self.liste_etoile:
            x, y, g = elem
            c = plt.Circle((x, y), g, color="red", linewidth=2, fill=False)
            ax.add_patch(c)
        ax.set_axis_off()

        plt.tight_layout()
        plt.show()

    def Maxietoile(self, liste_etoile, nb=50):
        """
        Sélectionne les nb plus grandes étoiles (théoriquement les nb plus lumineuse) et 
        les renvoies dans l'ordre décroissant.

        Parameters
        -----------
        :param liste_etoile: list => Liste d'étoiles sous le format (x,y,r/sigma).
        :param nb: int => nombre d'étoile a sélectionner dans la liste.

        Returns
        -------
        :returns: Renvoie une liste des étoiles les plus lumineuses de nb élément dans l'ordre décroissant.
        :rtype: list
        """
        liste_etoile.sort(key=lambda x: x[2], reverse=True)
        if len(liste_etoile) >= nb:
            liste_etoile = liste_etoile[0:nb]
        return liste_etoile

    def RapportImage(self, liste_étoile):
        """
        Permet de créer des rapports grace à 3 points formant un triangles les rapports sont petit coté / grand coté et  moyen coté / grand coté

        Parameters
        ----------
        :param liste_étoile: list => Liste d'étoiles sous le format (x,y,r/sigma).


        Returns
        -------
        :rtype: dict
        :returns: Renvoie un dictionnaire contenant un tuple de rapports et leurs erreurs (r1,dr1,r2,dr2) en clé associé à un tuple contenant des trios d'étoiles chacune caractérisée pas des coordonnées cartésiennes (xi,yi,ri/sigmai).
        Exemple : dico={(r1,dr1,r2,dr2): ((x1,y1,r1),(x2,y2,r2),(x3,y3,r3))...}
        """
        La = []
        La2 = []

        l_etoile = []
        for elem in liste_étoile:
            l_etoile.append((elem[0], elem[1], elem[2]))

        liste_combinaison = []
        for combinaison in combinations(l_etoile, 3):
            liste_combinaison.append(combinaison)

        dico_rap = {}
        for element in liste_combinaison:
            l = []
            a, b, c = element[0], element[1], element[2]
            xa, ya, sigmaA = a[0], a[1], a[2]
            xb, yb, sigmaB = b[0], b[1], b[2]
            xc, yc, sigmaC = c[0], c[1], c[2]

            AB = ((xb - xa) ** 2 + (yb - ya) ** 2) ** 0.5
            AC = ((xc - xa) ** 2 + (yc - ya) ** 2) ** 0.5
            BC = ((xc - xb) ** 2 + (yc - yb) ** 2) ** 0.5
            l.extend((AB, AC, BC))
            L = l.copy()
            L.sort()
            l_deplacement = []
            for i in range(3):
                for j in range(3):
                    if L[i] == l[j]:
                        v = (i, j)
                        l_deplacement.append(v)
            rapport_pg = L[0] / L[2]
            rapport_mg = L[1] / L[2]

            sigmapetit = l_deplacement[0]
            if sigmapetit[1] == 0:
                sig0 = sigmaA + sigmaB
            elif sigmapetit[1] == 1:
                sig0 = sigmaA + sigmaC
            else:
                sig0 = sigmaB + sigmaC
            sigmamoyen = l_deplacement[1]
            if sigmamoyen[1] == 0:
                sig1 = sigmaA + sigmaB
            elif sigmamoyen[1] == 1:
                sig1 = sigmaA + sigmaC
            else:
                sig1 = sigmaB + sigmaC
            sigmagrand = l_deplacement[2]
            if sigmagrand[1] == 0:
                sig2 = sigmaA + sigmaB
            elif sigmagrand[1] == 1:
                sig2 = sigmaA + sigmaC
            else:
                sig2 = sigmaB + sigmaC

            delta_rapport_pg = rapport_pg * ((sig0 / L[0]) + (sig2 / L[2]))
            delta_rapport_mg = rapport_mg * ((sig1 / L[1]) + (sig2 / L[2]))

            dico_rap[(rapport_pg, delta_rapport_pg, rapport_mg, delta_rapport_mg)] = (a,b,c)

        return dico_rap


class BaseDeDonee:
    """Classe qui concerne tout ce qui se rapporte à la Base de Données. 
    A savoir, l'importation des coordonnées des étoiles dans la région observée 
    et le calcul des rapports des triangles formées à partir de ses étoiles 
    
    Méthodes: Build, ListeN, rapportBaseDeDonnee, Affichage
    """

    def __init__(self):
        """
        initialisation des variables de la classe BaseDeDonee
        """
        self.nomsetoiles = ["Vega", "Sirius", "Canopus", "Arcturus", "Rigel", "Procyon", "Achernar", "Betelgeuse", "Hadar", "Capella", "Altair", "Aldébaran", "Antares", "Pollux", "Fomalhaut", "Deneb", "Mimosa", "Alpha Centauri B", "Regulus", "Acrux", "Adhara", "Shaula", "Gacrux", "Bellatrix", "Elnath", "Miaplacidus", "Alnilam", "Alnitak", "Alnair", "Alioth", "Dubhe", "Kaus Australis", "Mirfak", "Wezen", "Alkaïd", "Sargas", "Alhena", "Atria", "Althar", "Double Double I", "Nasr Alwaki"]

        self.numerocorrespondant = [91262,32349,30438,69673,24436,37279,7588,27989,68702,24608,97649,21421,80763,37826,11368,102098,62434,71681,49669,60718,33579,85927,61084,25336,25428,45238,26311,26727,109268,62956,54061,90185,15863,34444,67301,86228,31681,82273,90191,91919,91973]

        self.centre = Star(ra_hours=(5, 34, 31.97),dec_degrees=(22, 0, 52.1))

        # https://fr.wikipedia.org/wiki/Liste_des_%C3%A9toiles_les_plus_brillantes

    def BUILD(self, Adroite, Declinaison ):
        """
        Initialise les coordonnées de l'objet que l'on veut observer en équatoriale = (h,m,s),(°,','') = (heure minute seconde) et (Degree Minute d'arc Seconde d'arc)
        Exemple  (5, 34, 31.97),(22, 0, 52.1) Coordonnées nébuleuse du Crabe

        Parameters
        -----------
        :param Adroite: tuple => les coordonnées de l'objet que l'on veut observer heure minute seconde.
        :param Declinaison: tuple => les coordonnées de l'objet que l'on veut observer Degree Minute d'arc Seconde d'arc.
        """
        self.centre = Star(ra_hours=Adroite, dec_degrees=Declinaison)  #old : self.centre = Star.from_dataframe(df.loc[self.centre])

    def ListeN(self, n, angle=2.5):
        """
        Parameters
        -----------
        :param  n: int => nombre d'étoile a sélectionner dans la Base de Données.
        :param  angle: float => valeur du rayon du cercle autour de l'astre à observer pour une image 5°x5° il faut donner 2.5.

        Returns
        -------
        :rtype: list
        :returns: Une liste des étoiles les plus lumineuses dans l'ordre décroissant
        format : (x,y,magnitude) 
        """
        with load.open("hip_main.dat.gz") as f:
            df = hipparcos.load_dataframe(f)
        planets = load("de421.bsp")
        earth = planets["earth"]
        ts = load.timescale()
        t = ts.now()
        astrometric = earth.at(t).observe(self.centre)
        ra, dec, distance = astrometric.radec()

        a = u.rad
        c = u.deg
        racentre = ra.to(c)
        deccentre = dec.to(c)
        self.cat = df
        delimitationdec = Angle(angle, c)
        ref = Angle(90.0, c)
        refbis = Angle(-90.0, c)
        rayon_zone = Angle(angle, c)
        if deccentre + delimitationdec > ref:

            self.cat = self.cat[self.cat["dec_degrees"] < ref]
            self.cat = self.cat[self.cat["dec_degrees"] > deccentre - delimitationdec]

            for i in self.cat.index:

                distcentre = ref - deccentre
                valdec = self.cat.dec_degrees[i]
                valasc = self.cat.ra_degrees[i]
                distastre = ref - Angle(valdec, c)
                valasc = Angle(valasc, c)
                diff = racentre - valasc
                check = (distcentre ** 2+ distastre ** 2- 2 * (distastre * distcentre * np.cos(diff))) ** 0.5
                if check > rayon_zone:
                    self.cat = self.cat.drop(index=i, axis=0)

        elif deccentre - delimitationdec < refbis:
            rayon_zone = Angle(2, c)
            self.cat = self.cat[self.cat["dec_degrees"] > refbis]
            self.cat = self.cat[self.cat["dec_degrees"] < deccentre + delimitationdec]
            for i in self.cat.index:
                distcentre = deccentre - refbis
                valdec = self.cat.dec_degrees[i]
                valasc = self.cat.ra_degrees[i]
                distastre = Angle(valdec, c) - refbis
                valasc = Angle(valasc, c)
                diff = valasc - racentre
                check = ((distcentre) ** 2+ (distastre) ** 2- 2 * (distastre * distcentre * np.cos(diff))) ** 0.5
                if check > rayon_zone:
                    self.cat = self.cat.drop(index=i, axis=0)
        elif deccentre - delimitationdec > 0:
            self.cat = self.cat[self.cat["dec_degrees"] < deccentre + delimitationdec]
            self.cat = self.cat[self.cat["dec_degrees"] > deccentre - delimitationdec]
            for i in self.cat.index:
                distcentre = ref - deccentre
                valdec = self.cat.dec_degrees[i]
                valasc = self.cat.ra_degrees[i]
                distastre = ref - Angle(valdec, c)
                valasc = Angle(valasc, c)
                diff = racentre - valasc
                check = (distcentre ** 2+ distastre ** 2- 2 * (distastre * distcentre * np.cos(diff))) ** 0.5
                if check > rayon_zone:
                    self.cat = self.cat.drop(index=i, axis=0)
        elif deccentre + delimitationdec < 0:
            self.cat = self.cat[self.cat["dec_degrees"] < deccentre + delimitationdec]
            self.cat = self.cat[self.cat["dec_degrees"] > deccentre - delimitationdec]

            for i in self.cat.index:
                distcentre = deccentre - refbis
                valdec = self.cat.dec_degrees[i]
                valasc = self.cat.ra_degrees[i]
                distastre = Angle(valdec, c) - refbis
                valasc = Angle(valasc, c)
                diff = valasc - racentre
                check = ((distcentre) ** 2+ (distastre) ** 2- 2 * (distastre * distcentre * np.cos(diff))) ** 0.5
                if check > rayon_zone:
                    self.cat = self.cat.drop(index=i, axis=0)
        elif deccentre + delimitationdec == 0 or deccentre - delimitationdec == 0:
            self.cat = self.cat[self.cat["dec_degrees"] < deccentre + delimitationdec]
            self.cat = self.cat[self.cat["dec_degrees"] > deccentre - delimitationdec]
            self.cat = self.cat[self.cat["ra_degrees"] < racentre + delimitationdec]
            self.cat = self.cat[self.cat["ra_degrees"] > racentre - delimitationdec]

        baisse = 0.0

        self.ximage = []
        self.yimage = []
        magni = []
        image = []
        while len(self.cat) > n:
            for i in self.cat.index:
                mag = self.cat.magnitude[i]
                if mag >= 10 - baisse:
                    self.cat = self.cat.drop(index=i, axis=0)
                baisse += 0.00001
        region = Star.from_dataframe(self.cat)
        astrometric = earth.at(t).observe(region)
        ra, dec, distance = astrometric.radec()
        ascregion = ra.to(a)
        decregion = dec.to(a)
        self.Mag = list(self.cat.magnitude)

        for i in range(len(self.Mag)):
            x = -np.float(np.cos(decregion[i]) * np.sin(ascregion[i] - racentre)) / (np.sin(decregion[i]) * np.sin(deccentre)+ np.cos(decregion[i])* np.cos(deccentre)* np.cos(ascregion[i] - racentre))
            y = np.float(np.sin(decregion[i]) * np.cos(deccentre)- np.cos(decregion[i])* np.sin(deccentre)* np.cos(ascregion[i] - racentre)) / (np.sin(decregion[i]) * np.sin(deccentre)+ np.cos(decregion[i])* np.cos(deccentre)* np.cos(ascregion[i] - racentre))
            image.append((float(x), float(y), self.Mag[i]))
            self.ximage.append(float(x))
            self.yimage.append(float(y))
        #print("Catalogue", self.cat)
        return image

    def rapportBaseDeDonnee(self, image):
        """
        Permet de créer des rapports grace à 3 points formant un triangles les rapports sont :
        petit coté / grand coté et  moyen coté / grand coté

        Parameters
        ----------
        :param image: list => liste des étoiles au format : (x,y,magnitude).


        Returns
        -------
        :rtype: tuple
        :returns: Deux éléments : 
        Renvoie un dictionnaire contenant un tuple de rapports (r1,r2) en clé associé à un tuple 
        contenant des trios d'étoiles chacune caractérisée pas des coordonnées gnomoniques (xi,yi).
            Exemple : dico={(r1,r2): ((x1,y1),(x2,y2),(x3,y3))...}


        Renvoie aussi une liste composée des coordonnées (xi,yi) et magnitude (Mi) 
        des toutes les étoiles de la région observée
            Exemple : image=[(x1,y1,M1),(x2,y2,M2)]
        """
        liste_combi = []
        imagetrilumi = []
        etoiles_lumineuses = []

        self.Mag.sort()

        for k in range(len(self.Mag)):
            minus = 15.0
            parcours = image.copy()
            for etoiles in parcours:

                if etoiles[2] < minus:
                    minus = etoiles[2]
                    etoilebrillante = etoiles

            imagetrilumi.append(etoilebrillante)
            image.remove(etoilebrillante)
        for l in range(len(imagetrilumi)):
            if l <= 2:
                etoiles_lumineuses.append(imagetrilumi[l])
            else:
                liste_combi.append(imagetrilumi[l])

        dico = {}
        #print("les etoiles ...", imagetrilumi)
        for etoile in imagetrilumi:
            for combi in combinations(imagetrilumi, 3):
                l = []
                a, b, c = combi[0], combi[1], combi[2]
                xa, ya = a[0], a[1]
                xb, yb = b[0], b[1]
                xc, yc = c[0], c[1]

                AB = ((xb - xa) ** 2 + (yb - ya) ** 2) ** 0.5
                AC = ((xc - xa) ** 2 + (yc - ya) ** 2) ** 0.5
                BC = ((xc - xb) ** 2 + (yc - yb) ** 2) ** 0.5
                l.extend((AB, AC, BC))
                l.sort()
                rapport_pg = l[0] / l[2]
                rapport_mg = l[1] / l[2]
                dico[(rapport_pg, rapport_mg)] = (a, b, c)

        return dico, imagetrilumi

    def Affichage(self):
        """
        Un affichage de la base de donnees (une image)
        """

        HIP = list(self.cat.index)
        plt.scatter(self.ximage, self.yimage)
        fenetre = 0.04
        plt.xlim(-fenetre, fenetre)
        plt.ylim(-fenetre, fenetre)
        for i in range(len(HIP)):
            if HIP[i] not in self.numerocorrespondant:
                plt.text(self.ximage[i] - 0.003, self.yimage[i] + 0.003, HIP[i])
            else:
                plt.text(
                    self.ximage[i] - 0.003,
                    self.yimage[i] + 0.003,
                    self.nomsetoiles[self.numerocorrespondant.index(HIP[i])],
                )
        plt.axis("equal")
        plt.show()


class Comparaison:
    """Classe qui s'occupe de comparée l'image à la base de donnée"""

    def __init__(self):
        """
        initialisation des variables de la classe Comparaison
        """
        self.XE = 0
        self.YE = 0
        self.AFF = []

    def AstreCherche(self, tuplecoo):
        """
        Permet de décaller le centre de la base de données
        En 0,0 nous somme centrée
        """
        self.XE, self.YE = tuplecoo

    def KHI2(self, enzo, dico, imagetrilumi):
        """
        Applique la formule du Khi2 afin de comparer les rapports de l'image et ceux de la base de données 

        :param enzo: dict => Returns de la méthode rapport image dans la class TraitementImage
        :param dico: dict => Returns de la méthhode rapportBaseDeDonnee dans la class BaseDeDonnee

        :returns: 2 listes Lbdd et Lima qui contiennent les étoiles de la base de données et de l'image qui correspondent entre elles
        :rtype: tuple
        """
        resultat = {}
        dicotest = {}
        for trianglesBD in dico:
            khi2 = 100000000000000000
            rapports1BD = trianglesBD[0]
            rapports2BD = trianglesBD[1]
            bonnecoordBD = dico[trianglesBD]
            for trianglesIM in enzo:

                khi = float()
                khir1 = float()
                khir2 = float()
                rapports1IM = trianglesIM[0]
                rapports2IM = trianglesIM[2]
                sigma1 = trianglesIM[1]
                sigma2 = trianglesIM[3]
                khir1 = (rapports1BD - rapports1IM) ** 2
                khir2 = (rapports2BD - rapports2IM) ** 2
                khi += khir1 + khir2

                if khi < khi2:
                    khi2 = khi
                    bonrapIM = (rapports1IM, sigma1, rapports2IM, sigma2)
                    bonnecoordIM = enzo[bonrapIM]
            dicotest[bonnecoordBD] = bonnecoordIM
            resultat[trianglesBD] = bonrapIM

        dicofinal = {}
        for rapps in resultat:
            dicofinal[dico[rapps]] = enzo[resultat[rapps]]
        numetoile = 0
        DicoetoileBddIm = {}

        Lbdd = []
        Lima = []
        for parcours in imagetrilumi:
            numetoile += 1
            chassetoile = []
            vote = 0

            for valeurs in dicofinal:
                corresp = dicofinal[valeurs]

                if valeurs[0] == parcours:

                    etoile1 = corresp[0]
                    etoile2 = corresp[1]
                    etoile3 = corresp[2]
                    chassetoile.append(etoile1)
                    chassetoile.append(etoile2)
                    chassetoile.append(etoile3)
                if valeurs[1] == parcours:

                    etoile1 = corresp[0]
                    etoile2 = corresp[1]
                    etoile3 = corresp[2]
                    chassetoile.append(etoile1)
                    chassetoile.append(etoile2)
                    chassetoile.append(etoile3)

                if valeurs[2] == parcours:

                    etoile1 = corresp[0]
                    etoile2 = corresp[1]
                    etoile3 = corresp[2]
                    chassetoile.append(etoile1)
                    chassetoile.append(etoile2)
                    chassetoile.append(etoile3)
            for variable in chassetoile:
                nboccu = chassetoile.count(variable)
                if nboccu > vote:
                    vote = nboccu
                    star = variable
            DicoetoileBddIm[valeurs] = star
            Lbdd.append(parcours)
            Lima.append(star)
        return (Lbdd, Lima)

    def transfos(self, lbdd , lima):
        """regroupe les étoiles déterminées par le khi2 par trois afin d'en faire des triangles Aussi bien pour Lbdd que pour Lima.

        :param Lbdd: list => Liste regroupant les étoiles de la base de données retenues.
        :param Lima: list => Liste regroupant les étoiles de l'Image retenue.
        :returns: Une liste qui contient la liste des transformations créées à l'aide de la méthode transfo.
        :rtype: list
        """
        liste_trianglelbdd= []
        liste_trianglelima= []
        
        for combinaison in combinations(lbdd, 3):
                liste_trianglelbdd.append(combinaison)
        for combinaison in combinations(lima, 3):
                liste_trianglelima.append(combinaison)

        resultat = []
        for i in range(len(liste_trianglelbdd)):
            resultat.append(self.transfo(liste_trianglelbdd[i],liste_trianglelima[i]))
        return resultat
     

    def transfo(self, ebdd , eima):
        """Applique des formules d'homothétie à savoir une translation une rotation et une mise à l'échelle afin de déterminer une transformation géométrique
        qui permettrait de passer de la base de données à l'image.

        :param ebdd: list => Correspond à la liste des triangles formés à partir de la base de données dans la méthode transfos.
        :param eima: list => Correspond à la liste des triangles formés à partir de l'image dans la méthode transfos.
        
        :returns: Eqaution: Dictionnaire contenant les variables de la fonction de transfert, e: les coordonnées de l'astre cherché (en cartésien pixel) , aff: ensemble de données utiles à l'affichage. 
        :rtype: tuple
        """
        Equations = {}

        XA, YA, j = ebdd[0]          #petite lettre = image observée
        XB, YB, j = ebdd[1]          #grande lettre = BDD
        XC, YC, j = ebdd[2] 
        xa, ya, j = eima[0]
        xb, yb, j = eima[1]
        xc, yc, j = eima[2]
        
        YA, XA = -XA, -YA   
        YB, XB = -XB, -YB        
        YC, XC = -XC, -YC 
        XE, YE = self.XE,self.YE
        XE, YE = -YE, - XE
        bc = ((xb-xc)**2+(yb-yc)**2)**0.5
        ca = ((xc-xa)**2+(yc-ya)**2)**0.5
        BC = ((XB-XC)**2+(YB-YC)**2)**0.5
        CA = ((XC-XA)**2+(YC-YA)**2)**0.5
         
        XCh = XC
        YCh= YC
        
        YBh = ((YB-YC)*bc/BC)+YC   
        XBh = ((XB-XC)*bc/BC)+XC 
        YAh = ((YA-YC)*ca/CA)+YC  
        XAh = ((XA-XC)*ca/CA)+XC

        #Pour n'importe quel autre point
        #Rapport d'homothétie : RH = ca/CA
        YEh = ((YE-YC)*ca/CA)+YC  
        XEh = ((XE-XC)*ca/CA)+XC
        
        #translation
        #translation verticale
        dy = YCh-yc
        YCt = yc

        YAt = YAh - dy
        YBt = YBh - dy
        YEt = YEh - dy
            
        #translation horizontale
        dx = XCh - xc
        XCt = xc

        XAt = XAh - dx
        XBt = XBh - dx
        XEt = XEh - dx
        
        Aa = ((XAt-xa)**2+(YAt-ya)**2)**0.5
        alpha = np.arccos((Aa**2-2*(ca**2))/(-2*ca**2))    #angles déterminés avec les formules d'Al-Kashi
        
        XCf = XCt
        YCf = YCt
        XAf = XCf + (XAt-XCf)*np.cos(alpha) - np.sin(alpha)*(YAt-YCf)
        YAf = YCf + np.sin(alpha)*(XAt-XCf) + np.cos(alpha)*(YAt-YCf)
        XBf = XCf + (XBt-XCf)*np.cos(alpha) - np.sin(alpha)*(YBt-YCf)
        YBf = YCf + np.sin(alpha)*(XBt-XCf) + np.cos(alpha)*(YBt-YCf)
        XEf = XCf + (XEt-XCf)*np.cos(alpha) - np.sin(alpha)*(YEt-YCf)
        YEf = YCf + np.sin(alpha)*(XEt-XCf) + np.cos(alpha)*(YEt-YCf)
        xe = XEf
        ye = YEf
        
        #centrage de l'étoile visée 
        #choix de l'étoile à centrer :
        X = xa
        Y = ya
        xa = xa-X
        xb = xb-X
        xc = xc-X
        xe = xe
        ya = ya-Y
        yb = yb-Y
        yc = yc-Y
        ye = ye
        aff = [[XAf, XBf, XCf, XAf],[YAf, YBf, YCf, YAf],[xa, xb, xc, xa],[ya, yb, yc, ya],xe,ye]
        Equations["XC"] = XC
        Equations["YC"] = YC
        Equations["rapCA"] = ca/CA
        Equations["dx"] = dx
        Equations["dy"] = dy 
        Equations["XCf"] = XCf
        Equations["YCf"] = YCf
        Equations["alpha"] = alpha
        Equations["X"] = X
        Equations["Y"] = Y
        e = (xe,ye)
        return (Equations,e,aff)

    def transfoetoile(self, transfo):
        """Applique les tranformation à d'autres points 
        """
        Equations = transfo
        XE, YE = self.XE, self.YE

        XE, YE = -YE, - XE

        XC, YC, rapCA = Equations["XC"],Equations["YC"],Equations["rapCA"] # rapCA = ca/CA
        dx,dy = Equations["dx"],Equations["dy"]
        XCf, YCf, alpha = Equations["XCf"],Equations["YCf"],Equations["alpha"]
        X,Y =Equations["X"],Equations["Y"]

        XEh = ((XE-XC)*rapCA)+XC
        YEh = ((YE-YC)*rapCA)+YC 

        XEt = XEh - dx
        YEt = YEh - dy

        XEf = XCf + (XEt-XCf)*np.cos(alpha) - np.sin(alpha)*(YEt-YCf)
        YEf = YCf + np.sin(alpha)*(XEt-XCf) + np.cos(alpha)*(YEt-YCf)

        xe = XEf
        ye = YEf
        return(xe,ye)

    def vote(self, EE):
        """Algorithme de vote classique qui détermine la transformation géométrique la plus réaliste.

        :param EE: list => liste des transformations déterminées à l'aide des méthodes transfos et transfo.
        :returns: Dictionnaire contenant les variables de la transformation retenue.
        :rtype: dict
        """
        l = []
        PM = 5
        I = 0
        for chose in EE:
            el,il = chose[1]
            c = True
            for i in range(len(l)):
                if el <= l[i][0]+PM and el >= l[i][0]-PM :
                    if il <= l[i][1]+PM and il >= l[i][1]-PM :
                        l[i][2] +=1  
                        l[i][3].append((el,il))
                        sommeX = 0
                        sommeY = 0
                        for truc in l[i][3]:
                            sommeX += truc[0]
                            sommeY += truc[1]
                        l[i][0] = sommeX/len(l[i][3])
                        l[i][1] = sommeY/len(l[i][3])
                        l[i][4].append(EE[I][0])
                        l[i][5].append(EE[I][2])
                        c =False
            if c == True:
                l.append([el,il,1,[(el,il)],[EE[I][0]],[EE[I][2]]])
            I+=1

        maxi = -1
        for el in l:
            if el[2] > maxi:
                maxi = el[2]
                selec = el

        Xm, Ym = selec[0], selec[1]
        i = 0
        Position = -1
        Damin = 10E10
        for element in selec[3]:
            Xa, Ya = element[0], element[1]
            Dam = ((Xm-Xa)**2 + (Ym-Ya)**2)**0.5
            if Dam < Damin:
                Damin = Dam
                Position = i
            i+=1
        self.AFF = selec[5][Position]
        return selec[4][Position]
            
    def Affichage(self, image='crabe.png'):
        """
        Un affichage de deux triangles, si les triangles sont similaires c'est que la transformation est réussite, s'ils ne le sont pas cela n'a pas forcément échoué
        Affiche 2 triangles qui s'ils sont similaires montrent que la transformation est un succès

        :param image: str => image de fond, mettre la même que l'image analysé pour un bon visuel.
        """
        plt.figure(6)
        img = cv2.imread(image)
        img = 255 - img
        plt.imshow(img,zorder=0)

        ax = plt.gca()
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        plt.plot(self.AFF[0],self.AFF[1], 'k-')
        plt.plot(self.AFF[2],self.AFF[3], 'r:')
        plt.plot(self.AFF[4],self.AFF[5],'b+')
        plt.grid(True)
        #plt.axis('equal')
        plt.show()
