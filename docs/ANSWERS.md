# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

Le data pipeline suit un modèle ETL (Extract-Transform-Load).

>>> Pour run le pipeline, exécuter le fichier etl.py.

    Le fichier va appeler extract.py, transform.py et load.py pour obtenir les data de l'API, formater les données et les enregistrer dans la base de données locale, respectivement.

classes.py contient les définitions des classes Track, Users et Listen_history qui sont utilisées pour formater le data.

On utilise sqlalchemy pour créer une database SQLite (mydb.db) où seront enregistrées les données en local.

Le fichier load.py possède un paramètre ajustable par l'utilisateur: check_PK_double, qui prend la valeur True/False (ligne 7).

    True: le programme vérifie qu'il n'y a pas de duplicate primary key dans la database avant d'insérer un item. Cela prend plus de temps mais assure l'intégrité des données.

    False: aucune vérification. Si la database mydb.db existe déjà sous TECHNICAL-TEST-DATA-ENGINEER, le programme risque de retourner une erreur de type "UNIQUE constraint violation" en essayant d'insérer des data à partir de l'API avec la même Primary Key que certaines des data déjà dans la base de données.

        IF YOU WANT, you can manually delete the database before running the program, it will be generated again when the program runs.

        IF YOU WANT, you can remove '/mydb.db' on line 14 of file load.py so that the database is saved in RAM instead of in a file.

Les tests unitaires pour les composants du data pipeline sont dans le fichier test_etl.py.

Les requêtes SQL peuvent être affichées sur la console en passant le paramètre output_SQL_to_console à 'True' dans le fichier load.py (ligne 10).

Le pipeline de données est automatisé pour s'exécuter 1 fois par jour à 2h30AM à l'aide d'un GIT ACTION WORKFLOW, programmé dans le fichier /.github/workflows/data_pipeline.yml.

    Il est aussi possible d'activer manuellement le workflow à partir de GIT (workflow_dispatch).

-----
IMPORTANT - Pour que le automated workflow run sur votre repo GIT, il faut changer le user.name (ligne 31) et le user.email (ligne 32) dans le fichier data-pipeline.yml pour votre propre user.name et user.email GITHUB.
-----

Si le workflow devennait plus complexe (e.g. plusieurs scripts à exécuter en parallèle, etc.), il pourrait être avantageux d'utiliser un outil d'orchestration spécialisé (e.g. Airflow) à la place.

NOTA BENE - Mes tests unitaires de contrôle de la qualité des données ont révélé que le genre des tracks n'est pas choisi parmis les genres proposés dans la liste genre_list() fournie (mais plutôt un mot aléatoire).

    Comme je n'étais pas certain s'il s'agissait d'un oubli, j'ai considéré que Track.genres pouvait être n'importe quelle String, et je me contente de partager mon observation qu'elle n'est pas dans genre_list().

## Questions (étapes 4 à 7)

### Étape 4

SCHEMA DE BASE DE DONNEES

On propose un schéma de base de donnée avec 3 tables.

Table1:
    Name: users
    Columns:
        id              : int
        first_name      : str
        last_name       : str
        email           : str
        gender          : str
        favorite_genres : str
        created_at      : datetime
        updated_at      : datetime
    Constraints:
        Primary key (unique):
            id

Table2:
    Name: tracks
    Columns:
        id              : int
        name            : str
        artist          : str
        songwriters     : str
        duration        : str
        genres          : str
        album           : str
        created_at      : datetime
        updated_at      : datetime
    Constraints:
        Primary key (unique):        
            id

Table3:
    Name: listen_History
    Columns:
        user_id         : int
        track_id        : int
        created_at      : datetime
        updated_at      : datetime
    Constraints:
        Primary key (unique, composite):
            user_id
            track_id
        Foreign key:
            user_id (users.id)
        Foreign key:
            track_id (tracks.id)

Explications:

Each listening is recorded as a seperate entry in table3 (listen_history). The 'user_id' refers to the column 'id' from table1 (users) and the 'track_id' refers to the column 'id' from table2 (tracks).

We have a MANY-TO-MANY relationship between the users table and the tracks table (i.e. 1 user may listen to multiple tracks, but 1 track can also be listened by multiple users).

    A composite primary key is appropriate for this situation, using both foreign keys 'user_id' and 'track_id'.

Considerations:

We assume that a user listening multiple times to the same track should not affect the data any differently than listening to that track only once.

    IF the model were to require that we know the number of times a track is played, we could simply add a column to the listen_history table containing this number.

    OR we could add the 'created_at' column to the primary key for the listen_history table. That way multiple listening would appear as different entries in the table.

QUEL SYSTEME DE BASE DE DONNEES ?

Je pense qu'un système de base de donnée basé dans le cloud permet de répondre aux besoins, en assurant une capacité d'évoluer avec les données et l'application/l'entreprise du client.

Solution Cloud

    Par exemple, Microsoft Azure, dont la structure hybride, multicloud ou sur site donne une flexibilité pour répondre aux besoins, et assure une capacité d'évolution, ainsi qu'une bonne capacité d'intégration des autres logiciels, comme les outils de monitoring (Azure offre des outils de Cloud Service Monitoring, Big Data Analytics, and Logs).

    Une solution cloud a aussi l'avantage de nécessiter peu de maintenance (la maintenance étant effectuée par le provider), contrairement aux bases locales qui requièrent des backups réguliers et mises à jour pour assurer la cohérence des données.

    De plus, une solution cloud assure la synchronisation du data entre les différents périphériques (synchronisation automatique).

Solution locale

    D'un autre côté, si la capacité d'évolution est moins importante (limited scalability and little to no storage requirement increase), une base de donnée locale offre plusieurs avantages:
    
    - Fonctionnelle offline: les data pourraient être accédées et utilisées pour des modèles de machine learning ou statistiques même sans connexion Internet.
    
    - Sécurité: des data sensibles, comme les informations des utilisateurs de la plateforme, ne sont pas transmises via le réseau.
    
    - Coûts: une solution cloud peut être plus coûteuse (coûts de stockage des data et autres coûts associés).
    
    - Rapidité de réponse: les data locales sont récupérées plus rapidement.

Conclusion

En définitive, le choix du système de base de donnée dépend des objectifs d'évolution et priorités du client, mais avec les informations actuelles je penche plus pour une solution cloud comme Microsoft Azure (scalable, flexible, low-maintenance, synchronized), en particulier si le client possède déjà des infrastructures cloud sur d'autres de ses applications/services.

### Étape 5

Un outil de monitoring pourrait être utilisé, tel que Graphana (portail open source) ou Data Sentinel, afin d'observer l'activité des données, les pics d'activité, le temps d'exécution de chaque composante du pipeline, le volume de data échangé, ainsi que d'autres métriques selon leur utilité pour le client, comme le monitoring des verrous sur les tables lors des opérations/requêtes SQL, ou la taille des tables/de la database.

### Étape 6

On pourrait utiliser une combinaison de 2 types de systèmes de recommandation:

- Content-based filtering

    1) Creer un dataframe avec comme lignes les differentes tracks, et comme colonnes les differents variables des tracks (genre, artist, songwriters, etc.).
    1 colonne pour chaque genre, 1 colonne pour chaque artiste, etc.
    Chaque cellule du dataframe contient initialement la valeur 0.

    2) Remplir les cellules, selon le metadata de chaque track (e.g. pour une track de rock, la cellule prend la valeur 1 dans la colonne 'rock').
    On obtient un vecteur en k dimensions (k = nombre de colonnes) pour chaque track.

    3) A l'aide du listen_history pour chaque user, creer un vecteur en k dimensions pour le user en additionnant les vecteurs pour toutes les tracks écoutées par ce user. Puis, normaliser le vecteur du user.

    Important: Le vecteur du user est enregistré sous sa forme NON-normalisée, afin de faciliter le réentrainement du modèle avec l'intégration de nouvelles données.

    4) Recommandation: Utiliser un calcul de cosine similarity entre le user vector et chacun des track vector (pour les tracks qui n'ont pas déjà été écoutée par le user). Le calcul de cosine similarity qui retourne le plus petit angle indique la track recommandée au user.

- Collaborative filtering

    1) Même processus que les étapes 1 à 3 du content-based filtering ci-dessus.

    2) On compare (à l'aide de cosine similarity) le vecteur du user cible à chacun des vecteurs des autres users. Le plus petit angle indique le user qui est le plus 'similaire' à notre user cible.

    3) En ce basant sur le principe que les 2 users sont similaires et donc ont une plus grande probabilité d'aimer le même genre de tracks, on peut recommander au user 1 une track qui a été écoutée par le user 2 mais jamais par le user 1.

En combinant les 2 méthodes ci-dessus, on peut commencer par un collaborative filtering pour identifier un user 'similaire' à notre user cible, puis utiliser un content-based filtering pour identifier laquelle des tracks que ce user a écoutée a le plus de chance de plaire à notre user cible.

### Étape 7

Le dataframe contenant les vecteurs pour les tracks pourrait être sauvegardé dans la base de donnée.

Lors de l'acquisition quotidienne de nouvelles données via le data pipeline, on ferait alors les ajustements suivants:

1) Calculer le vecteur pour toute nouvelle track qui n'est pas déjà inclue dans le dataframe.

2) Pour chaque user, mettre à jour le vecteur du user en y additionnant le vecteur de chaque nouvelle track écoutée.

Important: Il est possible de pondéré d'un facteur le vecteur correspondant aux nouvelles tracks écoutées par le user, afin d'accorder une plus grande importance aux écoutes les plus récentes.

3) Une fois le vecteur de chaque user mis à jour, on procède à nouveau au collaborative filtering pour trouver un user similaire, puis au content-based filtering pour identifier la meilleure track à recommander.
