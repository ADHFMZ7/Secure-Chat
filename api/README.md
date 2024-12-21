# API Docs


## TODOs

- [ ] Key distribution
  - User generates key-pair and sends public when registering
  - Symmetric session key distributed when new chat is created
- [x] Password hashing
- [x] Websocket Connection Manager
- [ ] Adding friends
- [ ] Infer sender id from websocket


## Auth

### /login
### /register
### /logout

## Chat

Chat features are all handled through a websocket connection

The websocket connection expects json commands

format of json command:

```
{
  type: {type of command}
  body: {body of command}
}
```

### Chat Creation
```
type: 'create_chat'
body: {
  user_ids: [int]
}
```
### Sending Messages
```
type: 'send_message'
body: {
sender_id: int 
  chat_id: int
  content: str
}
```
## Protocol

1. User starts a websockets connection with the server
1. Fetches all past messages
1. Server maintains a dictionary of session -> websocket connection
1. Everytime a user sends a message, the server broadcasts it to all active connections that are in the chat
