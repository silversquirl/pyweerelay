"""
A Pythonic interface to weechat relay servers
"""
import socket

class Relay(socket.socket):
    """An interface to a weechat relay server."""

    def __init__(self, host, port=9000, password=None):
        "Initialize the Relay."
        super(Relay, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.init(password)

    # Helper
    def _sendutf(self, data):
        self.sendall(data.encode("utf-8"))

    def _sendmsg(self, data):
        self.sendall(data.encode("utf-8") + b"\n")

    # Direct correlation to relay commands
    def init(self, password=None):
        "Initialize connection with relay."
        self.sendall(b"init ")
        if password:
            password = password.replace(",", r"\,") # Escape commas
            self._sendutf("password={},".format(password))
        self.sendall(b"compression=off")
        self.sendall(b"\n")

    def hdata(self, path, keys=[]):
        "Request a hdata."
        self._sendmsg("hdata {} {}".format(path, ",".join(keys)))

    def info(self, name):
        "Request an info."
        self._sendmsg("info " + name)

    def nicklist(self, buf=None):
        "Request a nicklist, for one or all buffers."
        self.sendall(b"nicklist")
        if buf:
            self._sendmsg(" " + buf)
        else:
            self.sendall(b"\n")

    def input(self, buf, data):
        "Send data to a buffer."
        self._sendmsg("input {} {}".format(buf, data))

    def sync(self, buffers):
        """Synchronize one or more buffers, to get updates.
        buffers should be a dict with buffer:option pairs."""
        self._sendmsg("sync {} {}".format(
            ','.join(buffers.keys()),
            ','.join(buffers.values())))

    def desync(self, buffers):
        """Desynchronize one or more buffers, to stop updates.
        buffers should be a dict with buffer:option pairs."""
        self._sendmsg("sync {} {}".format(
            ','.join(buffers.keys()),
            ','.join(buffers.values())))

    def ping(self, data=""):
        "Send a ping to WeeChat."
        self._sendmsg("ping " + data)

    def quit(self):
        "Disconnect from relay."
        self.sendall(b"quit\n")

    # Abstractions
    def command(self, buf, cmd):
        """Send a command to a buffer.
        This is equivalent to relay.input(buf, "/" + cmd)"""
        self.input(buf, "/" + cmd)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit()

__all__ = ["Relay"]

