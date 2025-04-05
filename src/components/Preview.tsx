import React, { useEffect, useState, useRef } from 'react';
import { runProject } from '../services/webcontainer';
import type { FileStructure } from '../types';

interface PreviewProps {
  files: FileStructure[];
}

export const Preview: React.FC<PreviewProps> = ({ files }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const debounceTimeoutRef = useRef<NodeJS.Timeout | null>(null); // For debouncing

  useEffect(() => {
    let isMounted = true;
    abortControllerRef.current = new AbortController();

    // Cleanup previous timeout
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }

    async function startPreview() {
      if (!files.length) return;

      setIsLoading(true);
      setError(null);

      try {
        const webcontainerFiles = convertFilesToWebContainerFormat(files);
        const url = await runProject(webcontainerFiles, true); // Reset instance
        if (isMounted && !abortControllerRef.current?.signal.aborted) {
          setPreviewUrl(url);
        }
      } catch (err) {
        console.error('Preview error:', err);
        if (isMounted && !abortControllerRef.current?.signal.aborted) {
          setError(err instanceof Error ? err.message : 'Failed to start preview');
        }
      } finally {
        if (isMounted && !abortControllerRef.current?.signal.aborted) {
          setIsLoading(false);
        }
      }
    }

    // Debounce the preview start to avoid rapid successive calls
    debounceTimeoutRef.current = setTimeout(() => {
      startPreview();
    }, 500); // 500ms debounce

    return () => {
      isMounted = false;
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
      abortControllerRef.current?.abort();
    };
  }, [files]);

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <p className="text-gray-400">Starting preview environment...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-red-400 text-center">
          <p>Failed to start preview:</p>
          <p className="text-sm mt-2">{error}</p>
        </div>
      </div>
    );
  }

  if (!previewUrl) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400">
        No files to preview
      </div>
    );
  }

  return (
    <iframe
      src={previewUrl}
      className="w-full h-full border-0"
      title="Preview"
      sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
    />
  );
};

function convertFilesToWebContainerFormat(files: FileStructure[]): Record<string, { file: { contents: string } }> {
  const result: Record<string, { file: { contents: string } }> = {};

  // List of file extensions and paths to include
  const allowedExtensions = ['.tsx', '.ts', '.jsx', '.js', '.css', '.html', '.json'];
  const excludedPaths = ['server', 'api', 'database'];
  const configFiles = ['postcss.config.js', 'tailwind.config.js', 'vite.config.js'];

  function processFile(file: FileStructure, path: string = '') {
    const currentPath = path ? `${path}_${file.name}` : file.name;

    // Check if path contains any excluded terms
    if (excludedPaths.some(excluded => currentPath.includes(excluded))) {
      return;
    }

    if (file.type === 'file') {
      // Check if file extension is allowed
      const fileExt = `.${file.name.split('.').pop()}`;
      if (!allowedExtensions.includes(fileExt)) {
        return;
      }

      // Keep config files in root, prefix others with 'src_'
      const filePath = configFiles.includes(file.name) 
        ? file.name 
        : `src_${currentPath}`;

      result[filePath] = {
        file: {
          contents: file.content || ''
        }
      };
    } else if (file.children) {
      file.children.forEach(child => processFile(child, currentPath));
    }
  }

  files.forEach(file => processFile(file));
  return result;
}