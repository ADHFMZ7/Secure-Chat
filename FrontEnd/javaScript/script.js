import React from 'react'
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { MessageSquare, Plus, Menu, UserPlus, Settings } from "lucide-react"

export default function Component() {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(true)
  const [isSettingsOpen, setIsSettingsOpen] = React.useState(false)

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen)

  return (
    <Card className="w-full h-screen flex overflow-hidden">
      {/* Sidebar */}
      <div className={`bg-secondary ${isSidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden flex flex-col`}>
        <div className="p-4 flex space-x-2">
          <Button className="flex-1" variant="outline" title="New Chat">
            <Plus className="h-4 w-4" />
          </Button>
          <Button className="flex-1" variant="outline" title="Add Friend">
            <UserPlus className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {/* Chat list */}
          <div className="p-2 font-semibold">Chats</div>
          {[1, 2, 3].map((chat) => (
            <div key={chat} className="p-2 hover:bg-primary/10 cursor-pointer flex items-center">
              <MessageSquare className="mr-2 h-4 w-4" />
              <span>Chat {chat}</span>
            </div>
          ))}
          {/* Friends list */}
          <div className="p-2 font-semibold mt-4">Friends</div>
          {['Alice', 'Bob', 'Charlie'].map((friend) => (
            <div key={friend} className="p-2 hover:bg-primary/10 cursor-pointer flex items-center">
              <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
              <span>{friend}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-secondary p-4 flex items-center justify-between">
          <div className="flex items-center">
            <Button variant="ghost" size="icon" onClick={toggleSidebar} className="mr-2 lg:hidden">
              <Menu />
            </Button>
            <h1 className="text-xl font-bold">Web Chat</h1>
          </div>
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
                  <span>Enable notifications</span>
                  <input type="checkbox" />
                </div>
                <div className="flex items-center justify-between">
                  <span>Sound</span>
                  <input type="checkbox" />
                </div>
                <h3 className="font-semibold mt-4 mb-2">Theme</h3>
                <select className="w-full p-2 rounded border">
                  <option>Light</option>
                  <option>Dark</option>
                  <option>System</option>
                </select>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {/* You can add chat messages here */}
          <div className="text-center text-muted-foreground">
            Select a chat or start a new one
          </div>
        </div>

        {/* Message input */}
        <div className="p-4 border-t">
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Type a message..."
              className="flex-1 p-2 rounded-l-md border border-input bg-background"
            />
            <Button className="rounded-l-none">Send</Button>
          </div>
        </div>
      </div>
    </Card>
  )
}