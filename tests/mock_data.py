BATCH_YAML_CONTENT = r"""---
name: Yaml Name
icon_path: some/icon/path
tags:
  - tag1
  - tag2
environment:
  ENV_VAR1: value1
  ENV_VAR2: 
    - valuea
    - valueb

tasks:
  - name: Some Task
    raw: 
      command: some command
      async: false
..."""
