#!/usr/bin/env python3

import socket
import time

def main():
  counter = 1

  try:
    while True:
      s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind(("fd53:7cb8:383:5::e", counter))
      s.listen(1)
      conn, addr = s.accept()

      data = conn.recv(1024, socket.MSG_WAITALL)
      if data:
          counter = counter + 1

      s.shutdown(socket.SHUT_RDWR)
      s.close()

  except KeyboardInterrupt:
    pass
  print("counter = %d" % counter)

if __name__ == '__main__':
  main()
