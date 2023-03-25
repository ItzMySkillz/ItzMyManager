
# À propos de ItzMyManager

ItzMyManager est une gestion libre de parc informatique, elle fournit la
gestion complète d'un parc mais pas que, elle possède aussi un 
système de suivi pour les problèmes qui peuvent apparaitre.


## Caractéristiques

- Inventaire de stock de machine ( Poste de travaille, Serveur, Imprimante, Switch)
- Application web ( Multi-Plateform)
- Système de ticket dédié
- Système d'email lors de changement
- Suivie des machines


## Variables d'environment

Pour exécuter ce projet, vous devez ajouter les variables d'environnement suivantes à votre fichier config.ini
Si le fichier n'existe pas il faudra le créer.


```
[APP_INFORMATION]
secret_password = 
upload_folder = /static/uploads/pp

[SQL_SERVER]
host = 
user = 
password = 
database = 

[SMTP_SERVER]
host = 
port = 
mail = 
password = 
```


Pour lancer l'application 
```
venv\Scripts\Activate
flask run --host=ip_local
```
