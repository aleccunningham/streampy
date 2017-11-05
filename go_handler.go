package main;

import (
  "io"
  "log"
  "net"
  "bufio"
  "os"
  "fmt"
)

type Client struct {
  socket  net.Conn
  data    chan []byte
}

func dialSocket()  {
  conn, err := net.Dial("tcp", "127.0.0.1:3033")
  if err != nil {
    log.fatal(err)
  }
  return conn
}

func sendMessage()  {
  conn = dialSocket()
  reader, _ := bufio.NewReader(os.Stdin)
  fmt.Print("Text to send: ")
  text, _ := reader.ReadString('\n')
  // Send to socket
  fmt.Fprintf(conn, text + "\n")
}

func listenMessage()  {
  // listen for reply
  message, _ := bufio.NewReader(conn).ReadString('\n')
  fmt.Print("Mesage from server: "+message)
}

func listenSocket() {
  ln, err := net.Listen("tcp", ":3033")
  if err != nil {
    log.fatal(err)
  }
  defer ln.Close()
  for {
    conn, err := ln.Accept()
    if err != nil {
      log.fatal(err)
    }
    go func(c net.Conn) {
      // Print any messages
      listenMessage()
      // Shut down the connection
      c.Close()
    }(conn)
  }
}

func handleConnection(conn) {
  // Do stuff here
}
