import React from 'react';
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Settings } from "lucide-react";

interface ChatHeaderProps {
  isSettingsOpen: boolean;
  setIsSettingsOpen: (isOpen: boolean) => void;
  logOut: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ isSettingsOpen, setIsSettingsOpen, logOut }) => {
  return (
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
  );
};

export default ChatHeader;