# Jean Paul Start

_L'enfer, c'est les .bats_

- Execution de batches avec une syntaxe proche de celle d'Ansible

- Fenêtre affichant les icônes correspondant aux batches

- Utilisé sous Windows, normalement compatible Linux

## Installation

````bash
pip install git+https://github.com/cube-creative/jeanpaulstart.git
````

## Batches

Un batch décrit au format YAML un environnement (à travers des variables), puis des actions à executer

Exemple pour lancer 3Ds Max :

````yaml
---
name: 3Ds Max 2016
icon_path: $ENVIRONMENT\_config\jean-paul-start\icons\max-2016.png
tags: 
  - DCC
  - 3D
  - Max
environment:
  CUBE_ENVIRONMENT: production
  CUBE_MAX_SCRIPTS: $ENVIRONMENT\max-2016
  MAX_VERSION: 2016
  MAX_NAME: Max-$MAX_VERSION
  MAX_DIRECTORY: C:\Program Files\Autodesk\3ds Max $MAX_VERSION
  PYTHONPATH:
    - $MAX_DIRECTORY\python\Lib
    - $ENVIRONMENT\max-2016
    - $ENVIRONMENT\max-2016\python
  INI_TEMPLATE: $ENVIRONMENT\max-2016\config\3dsmax-ini-default-$MAX_VERSION.ini.j2
  INI_SOURCE: $LOCALAPPDATA\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\3dsmax.ini
  INI_TARGET: $LOCALAPPDATA\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\${MAX_NAME}_3dsmax.ini
  PLUGIN_INI_SOURCE: $CUBE_MAX_SCRIPTS\config\Plugin.UserSettings.ini.j2
  PLUGIN_INI_TARGET: $LOCALAPPDATA\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\${MAX_NAME}_Plugin_UserSettings.ini

tasks:
  - name: Copy 3dsmax.ini template if missing
    template:
      src: $INI_TEMPLATE
      dest: $INI_SOURCE
      force: no
      
  - name: Create custom 3dsmax.ini if missing
    copy:
      src: $INI_SOURCE
      dest: $INI_TARGET
      force: no
      
  - name: Additional Icons
    ini_file:
      src: $INI_TARGET
      state: present
      section: Directories
      option: Additional Icons
      value: $ENVIRONMENT\max-2016\resources\icons

  - name: Startup Scripts
    ini_file:
      src: $INI_TARGET
      state: present
      section: Directories
      option: Startup Scripts
      value: $CUBE_MAX_SCRIPTS\maxscript\startupscripts

  - name: AutoBackup Enable
    ini_file:
      src: $INI_TARGET
      state: present
      section: AutoBackup
      value: 1

  - name: Launch 3DS Max 2016
    raw: 
      command: "\"$MAX_DIRECTORY\\3dsmax.exe\" -p ${MAX_NAME}_Plugin_UserSettings.ini %* -i ${MAX_NAME}_3dsmax.ini"
...
````

## Ligne de commande

- Il est possible d'appeler un batch en ligne de commande 

````bash
python -m jeanpaulstart --filepath /path/to/a/batch.yml
````

- Il est possible d'executer un batch au format JSON sérialisé (peu commun)

_L'utilisation du flag `--not-normalized` est conseillée_

````bash
python -m jeanpaulstart --not-normalized --json {"name": "3DS Max", ... }
````

## Interface Graphique

Il existe une version PySide de Jean-Paul Start

Elle se base sur les dossiers contenant des batches, et un fichier de configuration associant les noms d'utilisateurs (obtenus avec `getpass.getuser()`) aux tags présents dans les batches

### Lancement

Il suffit d'appeler le module `jeanpaulstartui`

````bash
python -m jeanpaulstartui --batches /path/to/a/batch/folder;/path/to/another/folder --tags /path/to/user-tags.yml
````

### User Tags

Le fichier user tags représente au format YAML l'association de nom d'utilisateurs à des tags

Exemple

````yaml
---
production:
  - jp.sartre
  - p.deproges

graphist_base:
  - y.montand
  - j.hallyday

rigging:
  - s.weaver
  - j.rochefort
...
````

Ainsi, les batches portant les tags 'production' apparaitront pour l'utilisateur `jp.sartre`

- Il est possible de référencer un groupe dans un autre groupe en utilisant le caractère spécial `$`

````yaml
everyone:
  - $production
  - $graphist_base
  - $rigging
  - m.polnareff
...
````
