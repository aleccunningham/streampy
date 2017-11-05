package main;

import (
  "io"
  "log"
  "net"
  "bufio"
  "os"
  "fmt"
)

// Python "Class"
type Manager struct {
  // Structs can contain structs
  clients     map[*Client]bool // Holds <x> client instances
  broadcast   chan []byte // Slice of bytes
  register    chan *Client // Pointer to Client struct
  unregister  chan *Client // Pointer to Client struct
}

// Client that takes a socket to
// connect to and send some sort of data
type Client struct {
  socket  net.Conn
  // Represents an abstract collection of bytes
  data    chan []byte
}

// The *Manager argument ties the function to
// that struct, creating what Go calls an Interface
func (m *Manager) start() {
  for {
    select {
    // <- is Go's representation of a channel, basically
    // an asynchonus, small thread where data is passed
    case conn := <-manager.register:
      // Pass the connection to the managers client
      manager.clients[conn] = true
      fmt.Println("Added new client connection")
    case conn := <- manager.unregister:
      if _, ok := manager.clients[conn]; ok {
        // Once unregistered, the connection and its
        // clients' data are deleted
        close(conn.data)
        delete(manager.clients, conn)
        fmt.Println("A client's connection has been closed")
      }
    // Message is set to a Managers broadcast
    // attribute, which is a slice of bytes (a message or file)
    case message := <-manager.broadcast:
      for conn := range manager.clients {
        select {
        // Pass messages into a connections data
        case conn.data <- message:
        default:
          close(conn)
          // Deletes the clients registered by the manager
          // along with the connection it was using
          delete(manager.clients, conn)
        }
      }
    }
  }
}

func (m *Manager) send(client *Client)  {
  // Defer runs after the rest of the function has
  // completed, making sure we close the socket
  defer client.socket.Close()
  for {
    select {
    // Send a message through the clients data channel
    case message, ok := <-client.data:
      if !ok {
        return
      }
      // As passed through the channel, write it
      // to the socket the client is connected to
      client.socket.Write(message)
    }
  }

// Adds recieve to the Manager interface
func (m *Manager) recieve(client *Client)  {
  // Goroutine created for each established conn
  for {
    // Allocate a byte slice of size 4096
    message := make([]byte, 4096)
    length, err := client.socket.Read(message)
    if err != nil {
      // Kill and close the client and socket
      manager.unregister <- client
      client.socket.Close()
      log.Fatal(err)
    }
    if length > 0 {
      fmt.Println("RECIEVED: " + string(message))
      // Channel that sends all messages to the
      // manager's broadcast attribute
      m.broadcast <- message
    }
  }
}

// Adds recieve to the Client struct
func (client *Client) receive() {
    for {
        message := make([]byte, 4096)
        length, err := client.socket.Read(message)
        if err != nil {
            client.socket.Close()
            break
        }
        if length > 0 {
            fmt.Println("RECEIVED: " + string(message))
        }
    }
}

func (m *Manager) send(client *Client) {
  // Once the function has completed, defer
  // will run, ensuring the socket is closed
  defer client.socket.Close()
  for {
    select {
    // If there's no error pass the message into
    // the clients data channel
    case message, ok := <-client.data:
      if !ok {
        return
      }
      // Write to socket if no error
      client.socket.Write(message)
    }
  }
}

// Similair to a server in python, but it
// handles a Manager interface which then
// handles Clients and their actions
func consumer() {
  // Listen (NOT DIAL) on TCP socket
  // allowing perisistent monitoring of socket
  ln, err := net.Listen("tcp", ":3033")
  if err != nil {
    log.fatal(err)
  }
  fmt.Println("Listening to socket...")
  // Make sure we close the Listener
  defer ln.Close()
  // Creates a Manager interface
  manager := Manager{
    clients:    make(map[*Client]bool),
    broadcast:  make(chan []byte),
    register:   make(chan *Client),
    unregister: make(chan *Client),
  }
  go manager.start()
  // Same as while true in Python
  for {
    // Connect to net.Listen  on
    // TCP port 3033
    conn, err := ln.Accept()
    if err != nil {
      log.fatal(err)
    }
    // Using & instead of * creates a copy of the
    // defined struct, while * is just a pointer
    // to the definition
    // Using Make() allocates memory for a Clients data
    client := &Client{socket: conn, data: make(chan []byte)}
    // Pass the client into the running Manager
    // instance's register channel
    manager.register <- client
    // Create goroutines to recieve data
    // on a client
    go manager.recieve(client)
    // Another goroutine
    go manager.send(client)
  }
}

// AKA a client
func producer() {
  conn, err := net.Dial("tcp", "localhost:3033")
  if err != nil {
    log.Fatal(err)
  }
  client := &Client{socket: conn}
  // Goroutine that recieves requests on
  // the TCP port 3033 (there can be TONS of these)
  go client.recieve()
  for {
    reader := bufio.NewReader(os.Stdin)
    msg, _ := reader.ReadString('\n')
    conn.Write([]byte(strings.TrimRight(message, "\n")))
  }
}

func main() {
    flagMode := flag.String("mode", "server", "start in client or server mode")
    flag.Parse()
    // EX: go run *.go --mode server
    //     go run &.go --mode client
    if strings.ToLower(*flagMode) == "server" {
        consumer()
    } else {
        producer()
    }
}
