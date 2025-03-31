import React from 'react';
import Editor from '@monaco-editor/react';
import type { FileStructure } from '../types';

interface CodeViewerProps {
  file: FileStructure | null;
  onContentChange?: (content: string) => void;
}

export const CodeViewer: React.FC<CodeViewerProps> = ({ file, onContentChange }) => {
  if (!file || !file.content) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400 bg-gray-900/50">
        Select a file to view its contents
      </div>
    );
  }

  return (
    <Editor
      height="100%"
      defaultLanguage="typescript"
      theme="vs-dark"
      value={file.content}
      onChange={(value) => onContentChange?.(value || '')}
      options={{
        readOnly: false,
        minimap: { enabled: true },
        fontSize: 14,
        wordWrap: 'on',
        scrollBeyondLastLine: false,
        automaticLayout: true,
      }}
    />
  );
};