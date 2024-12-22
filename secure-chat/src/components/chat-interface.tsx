import React, { useEffect, useState, useCallback } from 'react'
import { Card } from "@/components/ui/card"
import Sidebar from "@/components/sidebar"
import ChatHeader from "@/components/chat-header"
import ChatMessages from "@/components/chat-messages"
import MessageInput from "@/components/message-input"
import { useAuth } from "@/context/AuthContext"
import { useNavigate } from "react-router-dom"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import useWebSocket, { ReadyState } from 'react-use-websocket';

export function ChatInterface() {
  const [messages, setMessages] = useState<{ [key: string]: any[] }>(() => {
    const savedMessages = localStorage.getItem('messages');
    return savedMessages ? JSON.parse(savedMessages) : {};
  });
  const [isSettingsOpen, setIsSettingsOpen] = React.useState(false);
  const [isDialogOpen, setIsDialogOpen] = React.useState(false);
  const [selectedUsers, setSelectedUsers] = useState<number[]>([]);
  const [activeChatId, setActiveChatId] = useState<string | null>(() => {
    return localStorage.getItem('activeChatId');
  });
  const [newMessage, setNewMessage] = useState('');
  const [activeUsers, setActiveUsers] = useState<{ id: number; name: string }[]>([]);
  const [chats, setChats] = useState<{ id: number; name: string }[]>(() => {
    const savedChats = localStorage.getItem('chats');
    return savedChats ? JSON.parse(savedChats) : [];
  });
  const [users, setUsers] = useState<{ [key: number]: string }>({});
  const { user, logOut } = useAuth();
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  if (!token) {
    console.error("No token found in localStorage");
    navigate("/login");
    return null;
  }

  const { sendMessage, lastMessage, readyState } = useWebSocket(`wss://chat.aldasouqi.com/chat?token=${token}`, {
    onOpen: () => console.log('WebSocket connection established'),
    onClose: () => console.log('WebSocket connection closed'),
    onError: (error) => console.error('WebSocket error:', error),
    shouldReconnect: (closeEvent) => true, // Will attempt to reconnect on all close events
  });

  useEffect(() => {
    if (lastMessage !== null) {
      const message = JSON.parse(lastMessage.data);
      console.log('Received message:', message);
      // Handle incoming messages here
    }
  }, [lastMessage]);

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
        localStorage.setItem('messages', JSON.stringify(data));
        const chatList = Object.keys(data).map(chatId => ({ id: Number(chatId), name: `Chat ${chatId}` }));
        setChats(chatList);
        localStorage.setItem('chats', JSON.stringify(chatList));
        if (chatList.length > 0) {
          setActiveChatId(chatList[0].id.toString()); // Set the first chat as active by default
          localStorage.setItem('activeChatId', chatList[0].id.toString());
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

  const handleSendMessage = () => {
    if (activeChatId && newMessage.trim() && readyState === ReadyState.OPEN && user) {
      const message = {
        type: 'send_message',
        body: {
          sender_id: user.user_id,
          chat_id: activeChatId,
          content: newMessage,
          timestamp: new Date().toISOString(),
        }
      };
      sendMessage(JSON.stringify(message));
      setNewMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleCreateChat = () => {
    if (readyState === ReadyState.OPEN && user) {
      const userIds = selectedUsers.includes(user.user_id) ? selectedUsers : [user.user_id, ...selectedUsers];
      sendMessage(JSON.stringify({ type: 'create_chat', body: { user_ids: userIds } }));
      setIsDialogOpen(false);
      setSelectedUsers([]);
    } else {
      console.error("WebSocket is not open or user is not defined");
    }
  };

  const handleUserSelection = (userId: number) => {
    setSelectedUsers((prevSelectedUsers) =>
      prevSelectedUsers.includes(userId)
        ? prevSelectedUsers.filter((id) => id !== userId)
        : [...prevSelectedUsers, userId]
    );
  };

  return (
    <Card className="w-full h-screen flex overflow-hidden">
      <Sidebar 
        chats={chats}
        activeUsers={activeUsers}
        setActiveChatId={setActiveChatId}
        onCreateChat={() => setIsDialogOpen(true)}
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
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Select Users</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            {Object.entries(users)
              .filter(([userId]) => Number(userId) !== user?.user_id)
              .map(([userId, username]) => (
                <div key={userId} className="flex items-center mb-2">
                  <Checkbox
                    checked={selectedUsers.includes(Number(userId))}
                    onCheckedChange={() => handleUserSelection(Number(userId))}
                  />
                  <span className="ml-2">{username}</span>
                </div>
              ))}
            <Button variant="outline" onClick={handleCreateChat}>Create Chat</Button>
          </div>
        </DialogContent>
      </Dialog>
    </Card>
  );
}

export default ChatInterface;