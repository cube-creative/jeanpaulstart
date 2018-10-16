# Jean Paul Start

L'enfer, c'est les .bats

_Jean-Paul Start is verbose about plugin loading, batch loading and parsing, task execution, ..._

_Be sure to set your logging level to `INFO` if needed_ 

## Installation

````bash
pip install git+https://github.com/cube-creative/jeanpaulstart.git
````

## Usage as a CLI

```bash
python -m jeanpaulstart -f path/to/a/batch.yml
```

## Usage from the API

### Basic batch run

```python
import jeanpaulstart

jeanpaulstart.run_from_filepath('path/to/a/batch.yml')
```

### Batch run inside a GUI

Tasks can be run step by step, so progress can be forwarded to the user 

Here, `ui` stands for any class that represents a window or dialog

```python
import jeanpaulstart

executor = jeanpaulstart.executor_from_filepath('path/to/a/batch.yml')

while not executor.has_stopped:
    ui.set_status_message(executor.next_task.name)

    status, messages = executor.step()
    if status != jeanpaulstart.OK:
        ui.set_status_message(' '.join([messages[-1], status]))
    
    ui.set_progress(executor.progress)

if executor.success:
    ui.set_status_message('Execution OK !')
    ui.set_progress(0.0)
``` 

## Batch Redaction

Batch are redacted in YAML or JSON, in a way similar to Ansible playbooks 

A batch describes 

- a name
- an icon path
- tags
- an environment (through variables, can be omitted)
- tasks to perform

```yaml
---
name: Jean Bauchefort
icon_path: $ENVIRONMENT/_config/jeanpaulstart/icons/jean-bauchefort.png
tags:
  - production
environment:
  PYTHONPATH:
    - C:\cube\python\Lib\site-packages
    - R:\deploy\cube
tasks:
  - name: Running application
    raw:
      command: python -m jeanbauchefortui
...
```

For a complete example please read [example-batch.yml](example-batch.yml)

## User Tags

A YAML file represents how usernames (based on `os.getpass.getuser()`) are associated with batch tags

Example

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

Batches with 'production' tag will show for `jp.sartre`

- Special character `$` allows to reference a group withing another group

````yaml
everyone:
  - $production
  - $graphist_base
  - $rigging
  - m.polnareff
...
````

## Tasks

Each task is identified by a command name

Tasks are written as plugins, in the package `jeanpaulstart.tasks`, they must conform to what the plugin loader expects

### Copy

Copies a file

If destination exists and `force: no`, nothing will happen

````yaml
- name: Name of task
  copy:
    src: /path/to/source.ext
    dest: /path/to/destination.ext
    force: [yes|no]
```` 

### File

Creates a file

Use `state: directory` if you want to create a directory

Use `state: absent` if you want to remove a file, or a directory and its subdirectories

````yaml
- name: Name of task
  file:
    path: /path/to/file
    state: [directory|absent]
````

### Include Tasks

Runs another batch file

Current environment is passed to executed batch, modifications made by that batch to the environment are not kept

````yaml
- name: Name
  include_tasks:
    file: path/to/batch/file.yml
```` 

### Ini File

Modifies a config file (.ini)

````yaml
- name: Task Name
  ini_file:
    src: /path/to/ini/file.ini
    state: [present|absent]
    section: sectionName
    option: optionName
    value: valueValue
````

### Pip / Pip3

Runs `pip install` / `pip3 install`

Please make sure that `pip` / `pip3` is in your `$PATH`

Parameter `state` is not mandatory, defaults to `present`

````yaml
- name: Task Name
  pip:
      name: PySide
      state: [present|forcereinstall]
````

````yaml
- name: Task Name
  pip3:
      name: PySide
      state: [present|forcereinstall]
````

````yaml
- name: Task Name
  pip:
      name: git+http://some/url.git
````

### Raw

Run a command in the terminal

Parameter `async` spawns a new process (`Popen()`)
Parameter `open_terminal` opens a new terminal window

`async` defaults to `True`
`open_terminal` defaults to `False`

If the exit code of the command is 0, `jeanpaulstart.OK` is return, else the exit code is returned

If `async: yes`, `jeanpaulstart.OK` is immediately returned

````yaml
- name: Launch djv_view
  raw: 
    command: "\"C:\\Program Files\\djv-1.1.0-Windows-64\\bin\\djv_view.exe\""
    async: [yes|no]
    open_terminal: [yes|no]
````

### Template

Copy a file and applies [Jinja2](http://jinja.pocoo.org/docs/2.10/) templating, based on environment variables

Parameter `force: yes` will overwrite destination if it already exists

````yaml
- name: Task Name
  template:
    src: /path/to/source.ext.j2
    dest: /path/to/dest.ext
    force: [yes|no]
````

### Url

Opens the given url in the default browser

````yaml
- name: Task Name
  url: http://some.url/
````

## Tasks flags

All tasks have 4 flags that can be set besides the command and its arguements.

- `register_status` defaults to `False` or `no`
- `catch_exception` defaults to `False` or `no`
- `exit_if_not_ok` defaults to `True` or `yes`
- `when` defaults to `"True"`

##### 'Register status'

`register_status` memorises the status returned by the task, and stores this 
status in the environment variable `$JPS_REGISTERED_STATUS`, immediately available for the next task

The executor returns the last registered status

##### 'Catch exception' and 'exit if not ok'

All tasks must return `OK`, maybe something else if something went wrong.

Most tasks should not raise any exception (exception should be dealt with when writing the task plugin), 
but it can happen (e.g when a socket is busy, a file missing, ...)

Those two flags are used to control batch execution, when task execution doesn't return `OK`, 
or when an Exception is raised.

If `catch_exception` is set to `True` or `yes`, `exit_if_not_ok` is forced to `False` or `no`

Here is a table of what happens on different cases

| Task return | `catch_exception=True`<br>`exit_if_not_ok=False` | `catch_exception=False`<br>`exit_if_not_ok=True` |
| --- | --- | --- |
| `OK` | execution continues | execution continues |
| not `OK` but no Exception is raised | execution continues | batch is exited<br>status is returned |
| Exception raised | exception is catched<br>TASK_ERROR_IGNORED is returned<br>execution continues | exception is raised | 

##### When

The `when` clause allows to specify a python expression that will be evaluated

If that expression doesn't evaluates to `True`, task is skipped

Environment variables can be used. For example

```yaml
tasks:
  - name: Render Image Sequence
    raw:
      command: $BLENDER_BIN --enable-autoexec ...
      async: False
      open_terminal: True
    register_status: True
    

  - name: Make mov
    raw:
      command: python -m preview ....
    when: $JPS_REGISTERED_STATUS == 'OK'
    register_status: True
```

The "Make mov" task will be run only if the task "Render Image Sequence" returns OK

_If the `when` clause evaluates to `False` and `register_status` is on, no status will be
registered_
