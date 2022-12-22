# Bookmarks

## But
Enregistrer des signets dans un fichier (au format json).  
Chaque signet appartient à une catégorie, est défini par son nom, son url et éventuellement l'icoône associée.  
Le programmle administre les signets, génère le fichier Html à publier, et peut même le diffuser.  
Pour l'instant seul un mode ligne de commande est développé  

## Éléments
bookmarks.py. Programme principal qui peut être lancé en principal (main) ou appelé par un programme interface (à développer)   
CryptMac.py   Programme qui permet de crypter des données (user/MdP...). La clé de cryptage est l'adresse mac du programme qui l'éxécute  
link.json     Base json qui contient les données  
link.html     Fichier Html généré  
.ico          Répertoire des icônes téléchargées automatiquement  
.img          Répertoire des images spécifiques  
.sav          Sauvegarde des fichier json avant modification  

### bookmarks.py
Le programme concentre toutes les options de lancement
1. -l --list  liste tous les signets par catégorie
2. -a --add   permet d'ajouter un signet. Si l'icône n'est pas renseignée, c'est le favicon du site qui est chargé (si absent, icône avec initiales)
3. -d --del   supprime un signet par son numério d'ordre
4. -g --generate Génère le fichier Html
5. -f --ftp   Envoie les nouveaux fichiers (depuis le dernier envoi) sur le site distant

### tab.css
Feuille de style squi reprend en particulier toutes les dénominations couleurs standardisées.  
Sont aussi définies est formes de blocs, arrondis...

### CryptMac.py
Est appelé par le programme principal mais permet aussi de générer un enregistrement crypter.  
**Attention** ne crypte qu'un enregistrement, pas un fichier entier.
Utilisation en mode cryptage; on génère un fichier nommé .ftp contenant des instructions json sur une seule ligne:  
python3 Crypt.py .ftp '{ "Host": "giveYourOwn", "Port": "giveYourOwn", "ftpUsername": "giveYourOwn", "ftpPassword": "giveYourOwn" }'



