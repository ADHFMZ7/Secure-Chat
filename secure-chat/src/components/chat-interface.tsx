import React, { useEffect, useState, useRef } from 'react'
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { MessageSquare, Plus, Menu, UserPlus, Settings } from "lucide-react"
import Sidebar from "@/components/sidebar"
import { useAuth } from "@/context/AuthContext"
import { useNavigate } from "react-router-dom"

export function ChatInterface() {
  const [messages, setMessages] = useState<{ [key: string]: any[] }>({});
  const [isSettingsOpen, setIsSettingsOpen] = React.useState(false);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const { user, logOut } = useAuth();
  const navigate = useNavigate();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const fetchMessages = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No token found in localStorage");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/chats", {
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
        if (Object.keys(data).length > 0) {
          setActiveChatId(Object.keys(data)[0]); // Set the first chat as active by default
        }
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    };

    fetchMessages();
  }, [logOut, navigate]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found in localStorage");
      return;
    }

    ws.current = new WebSocket(`ws://localhost:8000/chat?token=${token}`);

    ws.current.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      switch (message.type) {
        case "chat_created":
          console.log(`Chat created with ID: ${message.body.chat_id}`);
          break;
        case "message":
          setMessages((prevMessages) => {
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
  }, []);

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

  return (
    <Card className="w-full h-screen flex overflow-hidden">
      <Sidebar 
        chats={Object.keys(messages).map(chatId => ({ id: chatId, name: `Chat ${chatId}` }))}
        activeUsers={[{ id: 1, name: "User 1" }, { id: 2, name: "User 2" }]}
        setActiveChatId={setActiveChatId}
      />
      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-secondary p-4 flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-xl font-bold">Web Chat</h1>
          </div>
          <div className="flex items-center space-x-2">
            <Dialog open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
              <DialogTrigger asChild>
                <Button variant="ghost" size="icon">
                  <Settings />
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Settings</DialogTitle>
                </DialogHeader>
                <div className="py-4">
                  <h3 className="font-semibold mb-2">Notification Settings</h3>
                  <div className="flex items-center justify-between mb-2">
                    {/* Add your settings content here */}
                  </div>
                </div>
              </DialogContent>
            </Dialog>
            <Button variant="outline" onClick={logOut}>Sign Out</Button>
          </div>
        </div>
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeChatId && (
            <div>
              <h2 className="font-bold">Chat {activeChatId}</h2>
              {messages[activeChatId].map((message, index) => (
                <div key={index} className={`flex ${message.sender_id === user?.user_id ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-2 my-2 rounded-lg max-w-xs ${message.sender_id === user?.user_id ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
                    {message.sender_id !== user?.user_id && <div className="font-semibold">User {message.sender_id}</div>}
                    <div>{message.content}</div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        {/* Message input */}
        <div className="p-4 bg-secondary flex items-center">
          <input
            type="text"
            className="flex-1 p-2 border border-gray-300 rounded"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <Button variant="outline" onClick={handleSendMessage} className="ml-2">Send</Button>
        </div>
      </div>
    </Card>
  );
}

export default ChatInterface;