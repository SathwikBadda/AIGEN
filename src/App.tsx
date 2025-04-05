import React, { useState } from 'react';

// Define the FileStructure type

import { FileExplorer } from './components/FileExplorer';
import { CodeViewer } from './components/CodeViewer';
import { Bot, Send } from 'lucide-react';
import { generateWebsite } from './services/gemini';
import { FileStructure } from './types';
import { AIAssistant } from './components/AIAssistant';
import { Preview } from './components/Preview';

function App() {
  const [prompt, setPrompt] = useState('');
  const [files, setFiles] = useState<FileStructure[]>([]);
  const [selectedFile, setSelectedFile] = useState<FileStructure | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<'editor' | 'preview'>('editor'); // Default to "editor" view


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await generateWebsite(prompt);
      setFiles(response.files);
      if (response.files.length > 0) {
        const firstFile = findFirstFile(response.files);
        if (firstFile) {
          setSelectedFile(firstFile);
        }
      }
      setView('editor'); // Automatically switch to "editor" view after generating files
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while generating the website');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const findFirstFile = (files: FileStructure[]): FileStructure | null => {
    for (const file of files) {
      if (file.type === 'file') {
        return file;
      }
      if (file.children) {
        const found = findFirstFile(file.children);
        if (found) {
          return found;
        }
      }
    }
    return null;
  };

  const updateFileContent = (files: FileStructure[], path: string, newContent: string): FileStructure[] => {
    return files.map((file) => {
      if (file.name === path) {
        return { ...file, content: newContent };
      }
      if (file.children) {
        return { ...file, children: updateFileContent(file.children, path, newContent) };
      }
      return file;
    });
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-950 via-blue-950/20 to-gray-900 text-gray-200 relative">
      {/* Add a subtle animated gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-tr from-purple-900/10 via-blue-900/10 to-gray-900/10 animate-gradient-shift pointer-events-none" />
      
      {/* Wrap the entire content in a relative container to stay above the gradient */}
      <div className="relative flex flex-col flex-1">
        {/* Navbar Header */}
        <header className="bg-gray-800/80 backdrop-blur-md text-white shadow-md sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bot className="w-8 h-8 text-white" />
              <h1 className="text-xl font-semibold">AIGEN</h1>
            </div>
            <nav className="flex items-center gap-6">
              <a href="#features" className="text-gray-300 hover:text-white">
                Features
              </a>
              <a href="#about" className="text-gray-300 hover:text-white">
                About
              </a>
              <a href="#contact" className="text-gray-300 hover:text-white">
                Contact
              </a>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 max-w-7xl mx-auto py-6 px-4 flex flex-col">
          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-600/80 backdrop-blur border border-red-700 rounded-lg text-white">
              {error}
            </div>
          )}

          {/* View Toggle Buttons */}
          <div className="mb-4 flex gap-4">
            <button
              onClick={() => setView('editor')}
              className={`px-4 py-2 rounded-lg ${
                view === 'editor' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
              } hover:bg-blue-700`}
            >
              File Editor & Code Viewer
            </button>
            <button
              onClick={() => setView('preview')}
              className={`px-4 py-2 rounded-lg ${
                view === 'preview' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
              } hover:bg-blue-700`}
            >
              Preview
            </button>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 min-h-0 mb-6 ">
            {/* File Explorer and Code Viewer */}
            {view === 'editor' && files.length > 0 && (
              <div className="flex w-[80vw] h-[100vh] p-4 bg-gray-800/80 backdrop-blur rounded-lg shadow-lg border border-gray-700 overflow-hidden ">
                <div className="w-64 border-r border-gray-700">
                  <FileExplorer files={files} onFileSelect={setSelectedFile} />
                </div>
                <div className="flex-1">
                  <CodeViewer file={selectedFile} onContentChange={(newContent) => {
                    if (selectedFile) {
                      const updatedFiles = updateFileContent(files, selectedFile.name, newContent);
                      setFiles(updatedFiles);
                    }
                  }} />
                </div>
              </div>
            )}

            {/* Preview Section */}
            {view === 'preview' && (
              <div className="h-[calc(100vh-320px)] bg-gray-800/80 backdrop-blur rounded-lg shadow-lg border border-gray-700 overflow-hidden w-[80vw]">
                <Preview files={files} />
              </div>
            )}
          </div>

          {/* AI Assistant */}
          <AIAssistant 
            code={selectedFile?.content || ''} 
            fileName={selectedFile?.name}
          />

          {/* Fixed Input Form */}
          <div className="sticky bottom-4 bg-gray-800/95 backdrop-blur border border-gray-700 rounded-lg p-4 shadow-lg">
            <form onSubmit={handleSubmit} className="flex gap-4">
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the website you want to create..."
                className="flex-1 rounded-lg bg-gray-700/50 border border-gray-600 px-4 py-3 text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg flex items-center gap-2 hover:bg-blue-700 disabled:opacity-50 transition-colors"
                disabled={isLoading || !prompt.trim()}
              >
                <Send className="w-4 h-4" />
                Generate
              </button>
            </form>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-gray-800/80 backdrop-blur-md border-t border-gray-700/50 p-4">
          <p className="text-center text-gray-400 text-sm">
            &copy; 2025 Gemini Website Generator. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;