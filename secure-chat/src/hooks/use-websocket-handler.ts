import { useEffect, useRef } from 'react';

export function useWebSocketHandler(token: string, setMessages: any, setChats: any, setUsers: any, setActiveUsers: any) {
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!token) {
      console.error("No token found in localStorage");
      return;
    }

    ws.current = new WebSocket(`wss://chat.aldasouqi.com/chat?token=${token}`);

    ws.current.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("Received message:", message);
      if (!message.body) {
        console.error("Message body is undefined:", message);
        return;
      }
      switch (message.type) {
        case "chat_created":
          console.log(`Chat created with ID: ${message.body.chat_id}`);
          setChats((prevChats: any) => [
            ...prevChats,
            { id: message.body.chat_id, name: `Chat ${message.body.chat_id}` }
          ]);
          setMessages((prevMessages: any) => ({
            ...prevMessages,
            [message.body.chat_id]: []
          }));
          break;
        case "message":
          setMessages((prevMessages: any) => {
            const updatedMessages = { ...prevMessages };
            if (!updatedMessages[message.body.chat_id]) {
              updatedMessages[message.body.chat_id] = [];
            }
            updatedMessages[message.body.chat_id].push(message.body);
            return updatedMessages;
          });
          break;
        case "left_chat":
          console.log(`User ${message.body.user_id} left chat ${message.body.chat_id}`);
          break;
        case "went-online":
          if (message.body.user_id && message.body.username) {
            setUsers((prevUsers: any) => ({
              ...prevUsers,
              [message.body.user_id]: message.body.username
            }));
            setActiveUsers((prevUsers: any) => [
              ...prevUsers,
              { id: message.body.user_id, name: message.body.username }
            ]);
            console.log(`User ${message.body.username} went online`);
          } else {
            console.error("Invalid went-online message body:", message.body);
          }
          break;
        case "went-offline":
          if (message.body.user_id) {
            setActiveUsers((prevUsers: any) =>
              prevUsers.filter((user: any) => user.id !== message.body.user_id)
            );
            console.log(`User ${message.body.username} went offline`);
          } else {
            console.error("Invalid went-offline message body:", message.body);
          }
          break;
        default:
          console.error("Unknown message type:", message.type);
      }
    };

    ws.current.onclose = (event) => {
      if (event.wasClean) {
        console.log(`WebSocket connection closed cleanly, code=${event.code}, reason=${event.reason}`);
      } else {
        console.error('WebSocket connection closed unexpectedly');
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [token, setMessages, setChats, setUsers, setActiveUsers]);

  return ws;
}