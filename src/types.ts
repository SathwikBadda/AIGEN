export interface FileStructure {
  name: string;
  type: 'file' | 'directory';
  content?: string;
  children?: FileStructure[];
}

export interface GeneratedCode {
  files: FileStructure[];
}