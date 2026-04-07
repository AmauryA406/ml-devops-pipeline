# ML DevOps Pipeline

Pipeline CI/CD complet déployant une API de classification ML sur AWS, avec infrastructure as code et déploiement automatisé.

## Architecture

```
git push → GitHub Actions → Tests → Build Docker → Push ECR → Deploy EC2
```

```
Internet
    ↓
AWS VPC (eu-west-3)
    ↓
Subnet public
    ↓
Security Group (ports 22, 8000)
    ↓
EC2 t3.micro
    ↓
Container Docker → API FastAPI + modèle sklearn
```

## Stack technique

| Couche           | Technologie                     |
| ---------------- | ------------------------------- |
| API              | FastAPI + scikit-learn          |
| Containerisation | Docker                          |
| Registry         | AWS ECR                         |
| Serveur          | AWS EC2 t3.micro                |
| Réseau           | AWS VPC, Subnet, Security Group |
| Infrastructure   | Terraform                       |
| CI/CD            | GitHub Actions                  |
| Tests            | pytest                          |

## Structure du projet

```
ml-devops-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline CI/CD complet
├── app/
│   ├── __init__.py
│   ├── main.py             # API FastAPI
│   └── model.py            # Modèle Random Forest (iris)
├── terraform/
│   ├── main.tf             # Provider AWS
│   ├── variables.tf        # Variables
│   ├── outputs.tf          # Outputs (IP, URL ECR)
│   └── ec2.tf              # Infra AWS (VPC, EC2, IAM, ECR)
├── tests/
│   ├── __init__.py
│   └── test_api.py         # Tests unitaires pytest
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## Prérequis

- Docker Desktop
- Terraform
- AWS CLI configuré (`aws configure`)
- Compte AWS avec un utilisateur IAM (droits EC2, ECR, VPC, IAM)

## Installation locale

```bash
git clone https://github.com/AmauryA406/ml-devops-pipeline
cd ml-devops-pipeline

# Lancer l'API en local
docker compose up

# Tester l'API
curl http://localhost:8000
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## Lancer les tests

```bash
python -m pytest tests/ -v
```

## Déploiement infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Pour détruire l'infrastructure :

```bash
terraform destroy
```

## Pipeline CI/CD

Le pipeline se déclenche automatiquement à chaque `git push` sur `main` :

1. **Install dependencies** — installation des dépendances Python
2. **Run tests** — exécution des tests pytest
3. **Configure AWS credentials** — authentification AWS via secrets GitHub
4. **Login to ECR** — authentification Docker sur le registry AWS
5. **Build and push Docker image** — build en `linux/amd64` et push sur ECR
6. **Deploy to EC2** — connexion SSH, pull de la nouvelle image, redémarrage du container

### Secrets GitHub requis

| Secret                  | Description                         |
| ----------------------- | ----------------------------------- |
| `AWS_ACCESS_KEY_ID`     | Clé d'accès AWS                     |
| `AWS_SECRET_ACCESS_KEY` | Clé secrète AWS                     |
| `EC2_HOST`              | IP publique de l'instance EC2       |
| `EC2_SSH_KEY`           | Clé SSH privée pour accéder à l'EC2 |

## API Endpoints

| Méthode | Endpoint   | Description                |
| ------- | ---------- | -------------------------- |
| GET     | `/`        | Status de l'API            |
| GET     | `/health`  | Health check               |
| POST    | `/predict` | Prédiction d'espèce d'iris |

### Exemple de prédiction

```bash
curl -X POST http://<EC2_IP>:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

Réponse :

```json
{
  "species": "setosa",
  "confidence": 1.0
}
```

## Notes importantes

- L'image Docker est buildée en `--platform linux/amd64` pour être compatible avec les serveurs AWS (important sur Apple Silicon ARM64)
- Le `user_data` Terraform installe Docker et AWS CLI au premier démarrage de l'EC2
- Les credentials AWS ne sont jamais stockés dans le code — uniquement dans les secrets GitHub
