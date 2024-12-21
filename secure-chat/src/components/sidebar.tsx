import React from 'react'
import { Button } from "@/components/ui/button"
import { MessageSquare, Plus, UserPlus } from "lucide-react"

interface SidebarProps {
  chats: { id: number; name: string }[];
  activeUsers: { id: number; name: string }[];
  setActiveChatId: (id: string) => void;
  onCreateChat: () => void; // Add this line
}

const Sidebar: React.FC<SidebarProps> = ({ chats, activeUsers, setActiveChatId, onCreateChat }) => { // Modify this line
  return (
    <div className="bg-secondary w-64 transition-all duration-300 overflow-hidden flex flex-col">
      <div className="p-4 flex space-x-2">
        <Button className="flex-1" variant="outline" title="New Chat" onClick={onCreateChat}> {/* Modify this line */}
          <Plus className="h-4 w-4" />
        </Button>
        <Button className="flex-1" variant="outline" title="Add Friend">
          <UserPlus className="h-4 w-4" />
        </Button>
      </div>
      <div className="flex-1 overflow-y-auto">
        {/* Chat list */}
        <div className="p-2 font-semibold">Chats</div>
        {chats.map((chat) => (
          <div key={chat.id} className="p-2 hover:bg-primary/10 cursor-pointer flex items-center" onClick={() => setActiveChatId(chat.id.toString())}>
            <MessageSquare className="mr-2 h-4 w-4" />
            <span>{chat.name}</span>
          </div>
        ))}
        {/* Active users list */}
        <div className="p-2 font-semibold mt-4">Active Users</div>
        {activeUsers.map((user) => (
          <div key={user.id} className="p-2 hover:bg-primary/10 cursor-pointer flex items-center">
            <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
            <span>{user.name}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Sidebar;