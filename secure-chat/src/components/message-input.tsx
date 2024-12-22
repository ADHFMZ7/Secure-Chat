import React from 'react';
import { Button } from "@/components/ui/button";

interface MessageInputProps {
  newMessage: string;
  setNewMessage: (message: string) => void;
  handleSendMessage: () => void;
  handleKeyPress: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ newMessage, setNewMessage, handleSendMessage, handleKeyPress }) => {
  return (
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
  );
};

export default MessageInput;