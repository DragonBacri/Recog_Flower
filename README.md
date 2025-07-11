# API de Reconnaissance de Fleurs

Ce projet est une API web construite avec Flask et PyTorch qui permet d'identifier des espèces de fleurs à partir d'une image. Elle utilise un modèle ResNet50 pré-entraîné et affiné (fine-tuned) sur le jeu de données Oxford 102 Flowers.

L'application est conteneurisée avec Docker et conçue pour être déployée sur Google Cloud Run avec un pipeline de déploiement continu (CI/CD) via Cloud Build.

## Architecture Technique

- **Framework Web** : Flask
- **Modèle de ML** : PyTorch (ResNet50)
- **Serveur de Production** : Gunicorn
- **Conteneurisation** : Docker
- **Déploiement** : Google Cloud Run
- **CI/CD** : Google Cloud Build

## Endpoints de l'API

### `POST /predict`

Cet endpoint analyse une image et retourne les 3 prédictions les plus probables pour l'espèce de la fleur.

- **Méthode** : `POST`
- **Corps de la requête** : `multipart/form-data` avec un champ `image` contenant le fichier image.
- **Réponse en cas de succès** (`200 OK`):
  ```json
  {
    "flower": [
      "pincushion flower",
      "great masterwort",
      "globe thistle"
    ]
  }
  ```

### `GET /health`

Un endpoint simple pour vérifier que le service est en ligne et fonctionnel.

- **Méthode** : `GET`
- **Réponse** (`200 OK`):
  ```json
  {
    "status": "healthy"
  }
  ```

## Comment Tester l'API

### Prérequis

Assurez-vous d'avoir Python 3.9+ et `pip` installés.

1.  Clonez le dépôt.
2.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

### Test en Local avec le Notebook

1.  **Lancez le serveur Flask localement :**
    ```bash
    python app/app.py
    ```
    Le serveur démarrera sur `http://0.0.0.0:5000`.

2.  **Exécutez le notebook `test_api.ipynb` :**
    Ouvrez et exécutez les cellules du notebook. Il est configuré pour envoyer une image de test au serveur local et afficher la prédiction.

## Déploiement Continu (CI/CD)

Ce projet est configuré pour un déploiement automatique. Chaque `git push` sur la branche `main` déclenche un pipeline sur Google Cloud Build qui :
1.  Construit l'image Docker.
2.  Pousse l'image vers Artifact Registry.
3.  Déploie la nouvelle version sur Cloud Run.

Le processus est défini dans le fichier `cloudbuild.yaml`.

