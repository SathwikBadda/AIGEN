import React from 'react';
import { ChevronDown, ChevronRight, File, Folder } from 'lucide-react';
import type { FileStructure } from '../types';

interface FileExplorerProps {
  files: FileStructure[];
  onFileSelect: (file: FileStructure) => void;
}

interface FileNodeProps {
  file: FileStructure;
  level: number;
  onFileSelect: (file: FileStructure) => void;
}

const FileNode: React.FC<FileNodeProps> = ({ file, level, onFileSelect }) => {
  const [isOpen, setIsOpen] = React.useState(true);
  const indent = level * 16;

  if (file.type === 'file') {
    return (
      <div
        className="flex items-center py-1 px-2 hover:bg-gray-700 cursor-pointer text-gray-300"
        style={{ paddingLeft: `${indent}px` }}
        onClick={() => onFileSelect(file)}
      >
        <File className="w-4 h-4 mr-2 text-gray-400" />
        <span className="text-sm">{file.name}</span>
      </div>
    );
  }

  return (
    <div>
      <div
        className="flex items-center py-1 px-2 hover:bg-gray-700 cursor-pointer text-gray-300"
        style={{ paddingLeft: `${indent}px` }}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? (
          <ChevronDown className="w-4 h-4 mr-2 text-gray-400" />
        ) : (
          <ChevronRight className="w-4 h-4 mr-2 text-gray-400" />
        )}
        <Folder className="w-4 h-4 mr-2 text-gray-400" />
        <span className="text-sm font-medium">{file.name}</span>
      </div>
      {isOpen && file.children?.map((child, index) => (
        <FileNode
          key={index}
          file={child}
          level={level + 1}
          onFileSelect={onFileSelect}
        />
      ))}
    </div>
  );
};

export const FileExplorer: React.FC<FileExplorerProps> = ({ files, onFileSelect }) => {
  return (
    <div className="w-64 bg-gray-800 border-r border-gray-700 overflow-y-auto h-full">
      {files.map((file, index) => (
        <FileNode
          key={index}
          file={file}
          level={0}
          onFileSelect={onFileSelect}
        />
      ))}
    </div>
  );
};