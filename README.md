python api client [TorrServer](https://github.com/YouROK/TorrServer)

Getting Started
---------------
```python
from api import Client

# instantiate a Client
client = Client("http://192.168.1.5:8090")

# /torrents
client.list_torrents()
```
