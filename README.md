
# AEWL - Arma Extensible Widget Language
This project aims to simplify the process of creating GUI's for Arma 3. It provides a much simpler language, with the possibility of extending the language through Python classes.

## Installation
This package has not yet been released to PyPI, as it is still currently under development.
It is, however, functional, and can be installed directly from the git repository:
```pip install -e git+https://github.com/SigJig/aewl.git#egg=aewl```

## Usage
The package exposes 5 main functions:
* `get_base()` - Return an [armaconfig.py](https://github.com/SigJig/armaconfig.py) object consisting of all base GUI classes (exported by Arma 3 GUI creator)
* `file_to_file(src, dst, *args, **kwargs)` - Converts a .aewl file into an arma 3 config file
* `file_to_str(src, *args, **kwargs)` - Converts a .aewl file into an arma 3 config string
* `str_to_file(src, dst, *args, **kwargs)` - Converts an aewl string into an arma 3 config file
* `str_to_str(src, *args, **kwargs)` - Converts an aewl string into an arma 3 config string

## Example

```python

from aewl import (
    file_to_file,
    file_to_str,
    str_to_file,
    str_to_file
)

# file_to_file
with open('input.aewl') as inp, open('output.hpp', 'w') as outp:
    file_to_file(inp, outp)

# file_to_str
with open('input.aewl') as inp:
    print(file_to_str(inp))

# str_to_file
with open('output.hpp', 'w') as outp:
    str_to_file('widget my_text(text) { text="Hello World" };', outp)

# str_to_str
print(str_to_str('widget my_text(text) { text="Hello World" };'))

```