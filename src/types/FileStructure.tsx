
export interface FileStructure {
  path: string;
  type: 'file' | 'folder';
  name: string; // Add the 'path' property
  children?: FileStructure[];
  content?: string;
}

export interface FileExplorerProps {
  files: FileStructure[];
  onFileSelect: (file: FileStructure) => void;
}