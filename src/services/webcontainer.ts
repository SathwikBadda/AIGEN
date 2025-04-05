import { WebContainer } from '@webcontainer/api';

class WebContainerManager {
  private static instance: WebContainer | null = null;
  private static bootPromise: Promise<WebContainer> | null = null;
  private static operationQueue: Promise<void> = Promise.resolve();

  static async getInstance(reset = false): Promise<WebContainer> {
    const operation = this.operationQueue.then(async () => {
      if (reset && this.instance) {
        await this.instance.teardown();
        this.reset();
      }

      if (this.instance) {
        return this.instance;
      }

      if (this.bootPromise) {
        return this.bootPromise;
      }

      this.bootPromise = WebContainer.boot().then(container => {
        this.instance = container;
        return container;
      });

      return this.bootPromise;
    });

    this.operationQueue = operation.then(() => {}).catch(() => {});
    return operation;
  }

  static reset() {
    this.instance = null;
    this.bootPromise = null;
  }
}

export async function runProject(files: Record<string, { file: { contents: string } }>, reset = false) {
  try {
    const webcontainer = await WebContainerManager.getInstance(reset);

    // Updated package.json
    const packageJSON = {
      name: 'web-project',
      type: 'module',
      scripts: {
        dev: 'vite --host'
      },
      dependencies: {
        'react': '^18.2.0',
        'react-dom': '^18.2.0',
        '@types/react': '^18.2.0',
        '@types/react-dom': '^18.2.0',
        'tailwindcss': '^3.3.0',
        'postcss': '^8.4.31',
        'autoprefixer': '^10.4.16'
      },
      devDependencies: {
        '@vitejs/plugin-react': '^4.0.0',
        'vite': '^4.3.9',
        'typescript': '^5.0.2'
      }
    };

    // Updated config files with ESM format
    const configFiles = {
      'package.json': {
        file: {
          contents: JSON.stringify(packageJSON, null, 2)
        }
      },
      'vite.config.js': {
        file: {
          contents: `
            import { defineConfig } from 'vite';
            import react from '@vitejs/plugin-react';

            export default defineConfig({
              plugins: [react()],
              server: {
                host: true,
                port: 5173,
                strictPort: true,
                hmr: { clientPort: 443 }
              }
            });
          `
        }
      },
      'postcss.config.js': {
        file: {
          contents: `
            export default {
              plugins: {
                tailwindcss: {},
                autoprefixer: {},
              }
            };
          `
        }
      },
      'tailwind.config.js': {
        file: {
          contents: `
            /** @type {import('tailwindcss').Config} */
            export default {
              content: [
                "./index.html",
                "./src/**/*.{js,ts,jsx,tsx}",
              ],
              theme: {
                extend: {},
              },
              plugins: [],
            };
          `
        }
      },
      'index.html': {
        file: {
          contents: `
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Generated Website</title>
              </head>
              <body>
                <div id="root"></div>
                <script type="module" src="/src/main.tsx"></script>
              </body>
            </html>
          `
        }
      },
      'src/main.tsx': {
        file: {
          contents: `
            import React from 'react';
            import ReactDOM from 'react-dom/client';
            import App from './App';
            import './index.css';

            ReactDOM.createRoot(document.getElementById('root')!).render(
              <React.StrictMode>
                <App />
              </React.StrictMode>
            );
          `
        }
      },
      'src/index.css': {
        file: {
          contents: `
            @tailwind base;
            @tailwind components;
            @tailwind utilities;
          `
        }
      },
      'src/App.tsx': {
        file: {
          contents: `
            import React from 'react';

            export default function App() {
              return (
                <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
                  <div className="max-w-7xl mx-auto">
                    <h1 className="text-4xl font-bold text-gray-900">
                      Welcome to your new website!
                    </h1>
                  </div>
                </div>
              );
            }
          `
        }
      }
    };

    // Kill any existing processes
    try {
      await webcontainer.spawn('pkill', ['-f', 'node']);
    } catch {
      // Ignore pkill errors
    }

    // Mount all files
    await webcontainer.mount({
      ...configFiles,
      ...Object.fromEntries(
        Object.entries(files).map(([path, content]) => [
          path.replace(/\//g, '_'),
          content
        ])
      )
    });

    // Install dependencies
    console.log('Installing dependencies...');
    const installProcess = await webcontainer.spawn('npm', ['install']);
    const installExitCode = await new Promise<number>((resolve) => {
      const timeout = setTimeout(() => resolve(-1), 60000);
      installProcess.output.pipeTo(new WritableStream({
        write(data) {
          console.log('Install output:', data);
        }
      }));
      installProcess.exit.then((code) => {
        clearTimeout(timeout);
        resolve(code);
      });
    });

    if (installExitCode !== 0) {
      throw new Error('Failed to install dependencies');
    }

    // Start dev server
    console.log('Starting dev server...');
    const serverProcess = await webcontainer.spawn('npm', ['run', 'dev']);

    return await new Promise<string>((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Server start timeout'));
      }, 60000);

      serverProcess.output.pipeTo(new WritableStream({
        write(data) {
          console.log('Server output:', data);

          if (data.includes('Network:')) {
            webcontainer.on('server-ready', (port, url) => {
              clearTimeout(timeout);
              resolve(url);
            });
          }
        }
      }));
    });

  } catch (error) {
    console.error('WebContainer error:', error);
    WebContainerManager.reset();
    throw error;
  }
}