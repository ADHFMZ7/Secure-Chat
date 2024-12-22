import React, { useEffect, useState } from 'react'
import { Card } from "@/components/ui/card"
import Sidebar from "@/components/sidebar"
import ChatHeader from "@/components/chat-header"
import ChatMessages from "@/components/chat-messages"
import MessageInput from "@/components/message-input"
import { useAuth } from "@/context/AuthContext"
import { useNavigate } from "react-router-dom"
import { useWebSocketHandler } from "@/hooks/use-websocket-handler"

export function ChatInterface() {
  const [messages, setMessages] = useState<{ [key: string]: any[] }>({});
  const [isSettingsOpen, setIsSettingsOpen] = React.useState(false);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const [activeUsers, setActiveUsers] = useState<{ id: number; name: string }[]>([]);
  const [chats, setChats] = useState<{ id: number; name: string }[]>([]);
  const [users, setUsers] = useState<{ [key: number]: string }>({});
  const { user, logOut } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMessages = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found in localStorage");
        navigate("/login");
        return;
      }

      try {
        const response = await fetch("https://chat.aldasouqi.com/chats", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (!response.ok) {
          if (response.status === 403) {
            logOut();
            navigate("/login");
          }
          throw new Error("Failed to fetch messages");
        }

        const data = await response.json();
        setMessages(data);
        const chatList = Object.keys(data).map(chatId => ({ id: Number(chatId), name: `Chat ${chatId}` }));
        setChats(chatList);
        if (chatList.length > 0) {
          setActiveChatId(chatList[0].id.toString()); // Set the first chat as active by default
        }
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    };

    const fetchActiveUsers = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found in localStorage");
        navigate("/login");
        return;
      }

      try {
        const response = await fetch("https://chat.aldasouqi.com/users", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error("Failed to fetch active users");
        }

        const data = await response.json();
        const users = Object.keys(data).reduce((acc, userId) => {
          acc[Number(userId)] = data[userId];
          return acc;
        }, {} as { [key: number]: string });
        setUsers(users);
        const activeUsersList = Object.keys(data).map(userId => ({ id: Number(userId), name: data[userId] }));
        setActiveUsers(activeUsersList);
      } catch (error) {
        console.error("Error fetching active users:", error);
      }
    };

    fetchMessages();
    fetchActiveUsers();
  }, [logOut, navigate]);

  const token = localStorage.getItem("token");
  if (!token) {
    console.error("No token found in localStorage");
    navigate("/login");
    return null;
  }

  const ws = useWebSocketHandler(token, setMessages, setChats, setUsers, setActiveUsers);

  const handleSendMessage = () => {
    if (activeChatId && newMessage.trim() && ws.current && user) {
      const message = {
        type: 'send_message',
        body: {
          sender_id: user.user_id,
          chat_id: activeChatId,
          content: newMessage,
          timestamp: new Date().toISOString(),
        }
      };
      ws.current.send(JSON.stringify(message));
      setNewMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleCreateChat = () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN && user) {
      ws.current.send(JSON.stringify({ type: 'create_chat', body: { user_ids: [user.user_id] } }));
    } else {
      console.error("WebSocket is not open or user is not defined");
    }
  };

  return (
    <Card className="w-full h-screen flex overflow-hidden">
      <Sidebar 
        chats={chats}
        activeUsers={activeUsers}
        setActiveChatId={setActiveChatId}
        onCreateChat={handleCreateChat}
      />
      <div className="flex-1 flex flex-col">
        <ChatHeader 
          isSettingsOpen={isSettingsOpen}
          setIsSettingsOpen={setIsSettingsOpen}
          logOut={logOut}
        />
        <ChatMessages 
          messages={messages}
          activeChatId={activeChatId}
          users={users}
          user={user}
        />
        <MessageInput 
          newMessage={newMessage}
          setNewMessage={setNewMessage}
          handleSendMessage={handleSendMessage}
          handleKeyPress={handleKeyPress}
        />
      </div>
    </Card>
  );
}

export default ChatInterface;