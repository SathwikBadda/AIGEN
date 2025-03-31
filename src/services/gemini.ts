import { GoogleGenerativeAI } from '@google/generative-ai';

const GEMINI_API_KEY = 'AIzaSyB6hZddLirVDuKKZ2Z3ExMtS1XxYiQPQb8';

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

export async function generateWebsite(prompt: string) {
  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
    
    const result = await model.generateContent(`
      You are an expert full-stack developer and AIML Engineer with python or java at backend tasked with generating a production-ready website. Create a complete, professional implementation based on this description: ${prompt}
 
      CRITICAL REQUIREMENTS:
      1. You MUST create actual implementation files, not just empty directories
      2. Every directory MUST contain at least one implementation file
      3. Each file MUST contain complete, working code (no placeholders)
      4. All code MUST follow React and TypeScript best practices

      Required Files (at minimum):
      1. src/components/
         - Layout.tsx (main layout component)
         - Header.tsx (header component)
         - Footer.tsx (footer component)
         - At least 2 feature-specific components
      
      2. src/pages/
         - Home.tsx (homepage implementation)
         - At least 1 additional page
      
      3. src/hooks/
         - useAuth.ts (authentication hook)
         - At least 1 feature-specific hook
      
      4. src/utils/
         - api.ts (API utilities)
         - helpers.ts (helper functions)
      
      5. src/types/
         - index.ts (shared TypeScript interfaces)
      
      6. src/styles/
         - globals.css (global styles)
      
      required backend files:
      1. src/server/
          - server.py (Flask or FastAPI server)
          - routes.py (API routes)
          - models.py (database models)
          - database.py (database connection)
          - requirements.txt (Python dependencies)
      7. src/tests/
          - test_server.py (unit tests for server)
      8. src/assets/
          - images/ (directory for images)
          - styles/ (directory for styles)
      9. src/config/
          - config.ts (configuration file)

      Each file MUST include:
      1. Proper imports
      2. Complete TypeScript types/interfaces
      3. Full component/function implementations
      4. Error handling
      5. Loading states
      6. Proper exports
      7. JSDoc comments

      You MUST return ONLY a valid JSON object in the following format:
      {
        "files": [
          {
            "name": "string",
            "type": "file" | "directory",
            "content": "string (for files)",
            "children": [] (for directories)
          }
        ]
      }

      IMPORTANT:
      - Every file MUST have actual, working code implementation
      - DO NOT create empty files or directories
      - DO NOT use placeholder content
      - All code MUST be production-ready and fully functional
      - Include proper error handling and TypeScript types
      - Use Tailwind CSS for styling
      - Implement proper component composition
      - Add proper accessibility attributes
    `);

    const response = await result.response;
    const text = response.text();
    
    // Log the raw response for debugging
    console.log('Raw Gemini Response:', text);

    // Try to extract JSON if the response contains additional text
    let jsonText = text;
    const jsonStart = text.indexOf('{');
    const jsonEnd = text.lastIndexOf('}');
    
    if (jsonStart !== -1 && jsonEnd !== -1) {
      jsonText = text.substring(jsonStart, jsonEnd + 1);
    }

    try {
      const parsed = JSON.parse(jsonText);
      
      // Validate the response structure
      if (!parsed.files || !Array.isArray(parsed.files)) {
        throw new Error('Invalid response structure: missing files array');
      }

      // Validate each file has required properties and content
      interface File {
        name: string;
        type: 'file' | 'directory';
        content?: string;
        children?: File[];
      }

      const validateFileStructure = (file: File): void => {
        const allowedEmptyDirectories = ['images', 'styles']; // Add directories that can be empty

        if (!file.name || !file.type) {
          throw new Error(`Invalid file structure: missing name or type for ${JSON.stringify(file)}`);
        }

        if (file.type === 'file' && !file.content) {
          throw new Error(`Missing content for file: ${file.name}`);
        }

        if (file.type === 'directory') {
          if (!Array.isArray(file.children)) {
            throw new Error(`Invalid directory structure: ${file.name}`);
          }

          if (file.children.length === 0 && !allowedEmptyDirectories.includes(file.name)) {
            throw new Error(`Empty or invalid directory: ${file.name}`);
          }

          file.children.forEach(validateFileStructure);
        }
      };

      parsed.files.forEach(validateFileStructure);

      return parsed;
    } catch (error) {
      console.error('JSON Parse Error:', error);
      throw new Error('Failed to parse Gemini response as JSON. Please try again with a different prompt.');
    }
  } catch (error) {
    console.error('Error generating website:', error);
    throw error;
  }
}