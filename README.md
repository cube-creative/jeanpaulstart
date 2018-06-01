[![pipeline status](http://192.0.9.185/cube/jean-paul-start/badges/master/pipeline.svg)](http://192.0.9.185/cube/jean-paul-start/commits/master) [![coverage report](http://192.0.9.185/cube/jean-paul-start/badges/master/coverage.svg)](http://192.0.9.185/cube/jean-paul-start/commits/master) 

# Jean Paul Start

L'enfer, c'est les .bats

## Utilisation en GUI

Ouvir l'interface Jean Paul Start, en fournissant un dossier pour les batches à afficher, et un chemin pour le fichier
de tags

```bash
python -m jeanpaulstartui --batches R:/deploy/cube/_config/jean-paul-start-config/batches --tags R:/deploy/cube/_config/jean-paul-start-config/use
r_tags.yml
```

### Ouverture d'un batch en CLI

L'ouverture directe d'un batch `.yml` avec Jean Paul Start en CLI se fait en précisant le ficier avec l'argument `-f`

```bash
python -m jeanpaulstart -f R:/deploy/cube/_config/jean-paul-start-config/batches/batch_a_lancer.yml
```

## Utilisation en CLI

Il est possible d'utiliser Jean Paul Start en CLI, avec l'argument `--json` ou `-j`

### Directement

```bash
python -m jeanpaulstart --json "{\"name\": \"Some Name\", \"icon_path\": \"some/path\", \"tags\": [], \"tasks\": [{\"name\": \"A Task\", \"raw\": \"some command\"}]}"
```

### Avec les fonctions de dump fournies

Il existe des fonctions pour préparer un fichier ou des données batch pour la ligne de commande

- Directement depuis un chemin vers un batch (au format JSON ou YAML)

```python
import jeanpaulstart

dumped = jeanpaulstart.dump_file_for_command_line("some/filepath")
command = 'python -m jeanpaulstart --json {json_dump}'.format(json_dump=dumped)
```

- Depuis des données brutes (en sortie de parser)

```python
import jeanpaulstart
from jeanpaulstart import parser

data = parser.from_yaml(YAML_CONTENT)
dumped = jeanpaulstart.dump_data_for_command_line(data)
command = 'python -m jeanpaulstart --json {json_dump}'.format(json_dump=dumped)
```

_Note : les fonctions de dump se chargent de valider et normaliser les données, il faut veiller à 
**utiliser le contenu de batch coté utilisateur** (i.e avec le champ `environment`)_
