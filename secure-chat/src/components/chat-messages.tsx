import React, { useRef, useEffect } from 'react';

interface ChatMessagesProps {
  messages: { [key: string]: any[] };
  activeChatId: string | null;
  users: { [key: number]: string };
  user: { user_id: number } | null;
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, activeChatId, users, user }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4">
      {activeChatId && messages[activeChatId] && (
        <div>
          <h2 className="font-bold">Chat {activeChatId}</h2>
          {messages[activeChatId].map((message, index) => (
            <div key={index} className={`flex ${message.sender_id === user?.user_id ? 'justify-end' : 'justify-start'}`}>
              <div className={`p-2 my-2 rounded-lg max-w-xs ${message.sender_id === user?.user_id ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
                {message.sender_id !== user?.user_id && <div className="font-semibold">{users[message.sender_id]}</div>}
                <div>{message.content}</div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
};

export default ChatMessages;