# Jean Paul Start

L'enfer, c'est les .bats

_Jean-Paul Start is verbose about plugin loading, batch loading and parsing, task execution, ..._

_Be sure to set your logging level to `INFO` if needed_ 

### Usage as a CLI

```bash
python -m jeanpaulstart -f path/to/a/batch.yml
```

### Usage from the API

#### Basic batch run

```python
import jeanpaulstart

jeanpaulstart.run_from_filepath('path/to/a/batch.yml')
```

#### Batch run inside a GUI

Tasks can be run step by step, so progress can be forwarded to the user 

Here, `ui` stands for any class that represents a window or dialog

```python
import jeanpaulstart

executor = jeanpaulstart.executor_from_filepath('path/to/a/batch.yml')

while not executor.has_stopped():
    ui.set_status_message(executor.next_task().name)
    status, messages = executor.step()

    if status != jeanpaulstart.OK:
        ui.set_status_message(' '.join([messages[-1], status]))
    
    ui.set_progress(executor.progress())
``` 
