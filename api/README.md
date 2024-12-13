# API Docs


## TODOs

- [ ] Key distribution
  - User generates key-pair and sends public when registering
  - Symmetric session key distributed when new chat is created
- [ ] Password hashing
- [ ] Websocket Connection Manager











## Auth

### /login
### /register
### /logout


## Chat

### Protocol

1. User starts a websockets connection with the server
1. Fetches all past messages
1. Server maintains a dictionary of session -> websocket connection
1. Everytime a user sends a message, the server broadcasts it to all active connections that are in the chat
