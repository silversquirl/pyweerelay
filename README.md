# PyWeeRelay

A WeeChat relay client library in pure Python.

## Example

```python
from pyweerelay import Relay
with Relay("localhost") as r:
  r.command("core.weechat", "print Hello from PyWeeRelay!")
```

