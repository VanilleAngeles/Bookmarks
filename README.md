# Bookmarks

## But
Enregistrer des signets dans un fichier (au format json).  
Chaque signet appartient à une catégorie, est défini par son nom, son url et éventuellement l'icône spécifique associée.  
Le programme administre les signets, génère le fichier Html à publier, et peut même le diffuser.  
Pour l'instant seul un mode ligne de commande est développé  

## Éléments
bkmUI.py.     Programme principal en mode graphique
bkm.py        Programme secondaire en mode ligne de commande
config.ini    Fichier de configuration (gérable par les options du programme) qui permet de nommer les fichiers annexes (répertoires des icônes et des icônes spécifiques,répertoire de sauvegarde, nom du fichier htrml généré, taille des icônes téléchargées...) 
CryptMac.py   Programme qui permet de crypter des données (user/MdP...). La clé de cryptage est l'adresse mac de l'ordinateur qui l'éxécute  
link.json     Base json qui contient les données  
index.html     Fichier Html généré  
.ico          Répertoire des icônes téléchargées automatiquement  
.img          Répertoire des images spécifiques  
.sav          Sauvegarde des fichier json avant modification  

### bkmUI.py
Écrit à l'aide de l'utilitaire tkinter, les options sont dans le bandeau d'entête.  
- file: regroupe ce qui peut gérer les enregistrements:  
    ajout/suppression des enregistrement (add/del), vue synthétique de la base (list)  
    génération du fichier html et envoi sur le site de destination (voir ftp)  
- tools: outil pour recharger les icônes par défaut, modifier le fichier de configuration config.ini ou restaurer une base json à partir s=d'une sauvegarde  
Il est préférable de positionner le programme dans le répertoire contenant les autres fichiers et les sous-répertoires (.ico .img .sav)

### bkm.py
Ce programme est l'ancêtre du précédent. Il n'a plus trop d'utiklité mais peut être utilisé en chargemlent de masse.
Le programme concentre toutes les options de lancement
- -l ou --list  liste tous les signets par catégorie
- -a ou --add   permet d'ajouter un signet. Si l'icône n'est pas renseignée, c'est le favicon du site qui est chargé (si absent, icône avec initiales)
- -d ou --del   supprime un signet par son numério d'ordre
- -g ou --generate Génère le fichier Html
- -f ou --ftp   Envoie les nouveaux fichiers (depuis le dernier envoi) sur le site distant
- -h ou --help  Aide en ligne  
Tous ces arguments sont exclusifs les uns des autres.  
**Attention** contrairement au programme graphique, celui-ci n'accède pas au fichier de configuration. Si on veut gérér plusieurs bases, il faut mettre ce programme dans les répertoires contenant les bases et sous-répertoires.  
#### cas particulier des icônes
comme noté dans les sources référencées dans l'entète du programme, on utilise un artifice pour récupérer les favicon de chaque site. L'url https://www.google.com/s2/favicons?sz=64&domain_url=https://www.macif.fr permet par exemple de récupérer le favicon du site macif. Si cette requète ne rapporte rien, on crée une icône fond rouge avec le [début du] texte à l'intérieur

### LastUpdateDate.txt  
Permet de positionner un rappel de derbière date d'envoi de fichier sur le site destinataire  

### tab.css
Feuille de style qui reprend en particulier toutes les dénominations couleurs standardisées html.  
Sont aussi définies les formes de blocs, arrondis, taille et police h1 h2...

### CryptMac.py
Est appelé par le programme principal mais permet aussi de générer un enregistrement crypter.  
***Attention*** ne crypte qu'un enregistrement, pas un fichier entier.
Utilisation en mode cryptage; dans l'exemple on génère un fichier nommé .ftp contenant des instructions json sur une seule ligne:  
> python3 Crypt.py .ftp '{ "Host": "giveYourOwn", "Port": "giveYourOwn", "ftpUsername": "giveYourOwn", "ftpPassword": "giveYourOwn" }'  

### header.html
Fichier de l'entête utilisé pour constituer le fichier html; il pourra être modifié pour la table css, le titre ou les meta données.

## Intialisation
Les répertoires .ico .img .sav sont vides.  
Seul le fichier null.png sert à compléter les tableaux des catégories pour qu'ils aient la même hauteur
Le fichier link.json ne contient que le formatage d'un fichier json  
> [ ]  

Les couleurs de fond de chaque catégorie est dans la variable *Colors* du programme principal. Si le nombre de catégories est supérieur au nombre de couleurs, on boucle en revenant sur la première couleur.  

## À faire
1. ~~mettrre null.png dans répertoire racine~~
2. ~~permettre de choisir son répertoire de travail (actuellement celui où est le programme)~~ (config.ini)
3. ~~paramétrer taille des icônes (actuellement 64px)~~ (config.ini)
4. Générer une version portrait et une version paysage
5. ~~écrire une interface graphique~~
6. mette CryptMac dans un répertoire d'où on pourra toujours l'appeler
7. générer une version .deb
8. Mettre les textes en multilingue


[1] [Lien vers aide éditeur markdown](https://docs.roadiz.io/fr/latest/user/write-in-markdown/)
