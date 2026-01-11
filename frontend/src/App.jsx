import { useState } from 'react'
import './App.css'

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [documentContent, setDocumentContent] = useState('')
  const [audioFile, setAudioFile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const handleLanguageSwitch = () => {
    setSelectedLanguage(prev => prev === 'en' ? 'ar' : 'en')
  }

  const handleDocumentUpload = async () => {
    if (!documentContent) return
    
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/documents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: 'New Document',
          language: selectedLanguage,
          content: documentContent
        })
      })
      const data = await response.json()
      alert('Document uploaded successfully!')
    } catch (error) {
      console.error('Error uploading document:', error)
      alert('Failed to upload document')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAudioAnalysis = async () => {
    if (!audioFile) return

    setIsLoading(true)
    const formData = new FormData()
    formData.append('audio_file', audioFile)
    formData.append('language', selectedLanguage)

    try {
      const response = await fetch(`${API_BASE_URL}/api/audio/analyze`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setAnalysisResult(data)
    } catch (error) {
      console.error('Error analyzing audio:', error)
      alert('Failed to analyze audio')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app" dir={selectedLanguage === 'ar' ? 'rtl' : 'ltr'}>
      <header className="app-header">
        <h1>{selectedLanguage === 'en' ? 'QDA Bilingual App' : 'تطبيق التحليل النوعي ثنائي اللغة'}</h1>
        <button onClick={handleLanguageSwitch} className="language-toggle">
          {selectedLanguage === 'en' ? 'العربية' : 'English'}
        </button>
      </header>

      <main className="app-main">
        <section className="document-section">
          <h2>{selectedLanguage === 'en' ? 'Document Workspace' : 'مساحة العمل'}</h2>
          <textarea
            value={documentContent}
            onChange={(e) => setDocumentContent(e.target.value)}
            placeholder={selectedLanguage === 'en' ? 'Enter your document content...' : 'أدخل محتوى المستند...'}
            rows={10}
            className="document-textarea"
          />
          <button onClick={handleDocumentUpload} disabled={isLoading}>
            {selectedLanguage === 'en' ? 'Upload Document' : 'رفع المستند'}
          </button>
        </section>

        <section className="audio-section">
          <h2>{selectedLanguage === 'en' ? 'Audio Analysis' : 'تحليل الصوت'}</h2>
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => setAudioFile(e.target.files[0])}
            className="audio-input"
          />
          <button onClick={handleAudioAnalysis} disabled={isLoading || !audioFile}>
            {selectedLanguage === 'en' ? 'Analyze Audio' : 'تحليل الصوت'}
          </button>

          {analysisResult && (
            <div className="analysis-result">
              <h3>{selectedLanguage === 'en' ? 'Analysis Result' : 'نتيجة التحليل'}</h3>
              <p><strong>{selectedLanguage === 'en' ? 'Transcript:' : 'النص:'}</strong> {analysisResult.transcript}</p>
              <p><strong>{selectedLanguage === 'en' ? 'Feedback:' : 'التعليقات:'}</strong> {analysisResult.feedback}</p>
              {analysisResult.sentiment && (
                <p><strong>{selectedLanguage === 'en' ? 'Sentiment:' : 'المشاعر:'}</strong> {analysisResult.sentiment}</p>
              )}
            </div>
          )}
        </section>
      </main>

      {isLoading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
        </div>
      )}
    </div>
  )
}

export default App
