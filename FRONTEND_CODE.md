# Frontend Code Reference

This file contains all the frontend code needed to complete the QDA Bilingual App.

## File Structure

```
frontend/
├── src/
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
└── index.html
```

## 1. package.json

```json
{
  "name": "qda-bilingual-ui",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }
}
```

## 2. vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
})
```

## 3. index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>QDA Bilingual App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## 4. src/main.jsx

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## 5. src/App.jsx (Complete with bilingual support)

See the backend repository or README for the complete App.jsx code with:
- Language detection and switching (Arabic/English/Auto)
- Audio upload and transcription
- Template-based analysis
- Interactive document chat
- RTL support for Arabic text

Refer to the main conversation for the complete App.jsx implementation.

## Setup Instructions

1. Create the frontend directory:
```bash
mkdir -p frontend/src
cd frontend
```

2. Create all files listed above

3. Install dependencies:
```bash
npm install
```

4. Run development server:
```bash
npm run dev
```

5. Access at http://localhost:3000
