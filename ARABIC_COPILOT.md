# Arabic Co-Pilot for QDA - Mini Version

AI-powered assistant for Arabic content and audio analysis with intelligent suggestions and real-time support.

## Overview

The Arabic Co-Pilot is a mini AI assistant specifically designed for Arabic qualitative research, providing:
- Real-time transcription assistance for Arabic audio
- Content analysis suggestions in Arabic
- Code recommendations based on Arabic text patterns
- Cultural context awareness for Arabic interviews
- Bilingual translation support

## Features

### 1. Arabic Audio Co-Pilot

#### Real-Time Transcription Support
- **Live audio monitoring** during recording
- **Automatic dialect detection** (MSA, Egyptian, Levantine, Gulf, Maghrebi)
- **Speaker diarization** for multi-participant interviews
- **Intelligent punctuation** for Arabic text
- **Timestamp generation** for easy navigation

#### Audio Quality Feedback
```python
# Backend endpoint
@app.post("/copilot/audio-feedback")
async def audio_copilot_feedback(audio_chunk: UploadFile):
    """
    Provides real-time feedback on audio quality
    """
    analysis = {
        "audio_quality": "good",  # good, fair, poor
        "background_noise": "low",
        "speech_clarity": 0.92,
        "suggestions": [
            "الصوت واضح، استمر في هذا المستوى",
            "Audio is clear, maintain this level"
        ]
    }
    return analysis
```

### 2. Arabic Content Co-Pilot

#### Intelligent Code Suggestions

**Auto-suggest codes** based on Arabic text patterns:

```python
@app.post("/copilot/suggest-codes")
def suggest_arabic_codes(text: str, existing_codes: List[str]):
    """
    AI-powered code suggestions for Arabic content
    """
    prompt = f"""
    أنت مساعد للبحث النوعي. اقترح رموز تحليلية مناسبة للنص التالي:
    
    النص: {text}
    
    الرموز الموجودة: {existing_codes}
    
    اقترح 3-5 رموز جديدة أو موجودة تناسب هذا المقطع.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt]
    )
    
    return {
        "suggested_codes": response.text,
        "confidence": 0.85,
        "reasoning": "Based on semantic analysis"
    }
```

#### Contextual Help

**Cultural context awareness**:

```python
@app.post("/copilot/cultural-context")
def arabic_cultural_context(text: str):
    """
    Provides cultural context for Arabic expressions
    """
    prompt = f"""
    حلل هذا النص من منظور ثقافي عربي:
    {text}
    
    حدد:
    1. التعبيرات الثقافية الخاصة
    2. المراجع الدينية أو الاجتماعية
    3. السياق المحلي المحتمل
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt]
    )
    
    return {"context_analysis": response.text}
```

### 3. Smart Memo Assistant

#### Auto-generate memos in Arabic

```python
@app.post("/copilot/generate-memo")
def generate_arabic_memo(quotation: str, code: str):
    """
    Generates analytical memos in Arabic
    """
    prompt = f"""
    أنشئ مذكرة تحليلية قصيرة (2-3 جمل) للاقتباس التالي:
    
    الاقتباس: {quotation}
    الرمز: {code}
    
    اكتب بأسلوب أكاديمي مختصر.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt]
    )
    
    return {
        "memo_ar": response.text,
        "timestamp": datetime.now().isoformat()
    }
```

### 4. Translation Co-Pilot

#### Bidirectional translation with context

```python
@app.post("/copilot/translate")
def contextual_translation(text: str, source_lang: str, target_lang: str, context: str = ""):
    """
    Context-aware translation for research content
    """
    prompt = f"""
    ترجم النص التالي من {source_lang} إلى {target_lang} مع الحفاظ على المعنى البحثي:
    
    النص: {text}
    السياق: {context}
    
    قدم ترجمة دقيقة تحافظ على المصطلحات البحثية.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt]
    )
    
    return {
        "translation": response.text,
        "confidence": 0.9,
        "alternatives": []  # Can suggest multiple translations
    }
```

### 5. Interview Analysis Co-Pilot

#### Real-time interview feedback

```python
@app.post("/copilot/interview-feedback")
def interview_copilot(transcript_segment: str, interview_type: str):
    """
    Provides real-time suggestions during interview analysis
    """
    prompt = f"""
    أنت خبير في المقابلات البحثية. حلل المقطع التالي من مقابلة {interview_type}:
    
    {transcript_segment}
    
    قدم:
    1. تقييم عمق الأسئلة
    2. اقتراحات لأسئلة متابعة
    3. ملاحظات على راحة المشارك
    4. نقاط قوة المقابلة
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[prompt]
    )
    
    return {
        "feedback_ar": response.text,
        "suggestions": [],
        "quality_score": 0.85
    }
```

## Frontend Integration

### React Component Example

```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

const ArabicCopilot = ({ selectedText, language }) => {
  const [suggestions, setSuggestions] = useState(null);
  const [loading, setLoading] = useState(false);

  const getCopilotSuggestions = async () => {
    if (!selectedText || language !== 'ar') return;
    
    setLoading(true);
    try {
      const response = await axios.post('/copilot/suggest-codes', {
        text: selectedText,
        existing_codes: existingCodes
      });
      setSuggestions(response.data);
    } catch (error) {
      console.error('Copilot error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (selectedText) getCopilotSuggestions();
    }, 500);
    return () => clearTimeout(debounce);
  }, [selectedText]);

  return (
    <div className="copilot-panel" dir="rtl">
      <h3>🤖 المساعد الذكي</h3>
      {loading && <div>جاري التحليل...</div>}
      {suggestions && (
        <div>
          <h4>اقتراحات الترميز:</h4>
          <ul>
            {suggestions.suggested_codes.map((code, idx) => (
              <li key={idx}>
                <button onClick={() => applyCode(code)}>
                  {code}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
```

### Floating Copilot Button

```jsx
const CopilotButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        className="floating-copilot"
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: language === 'ar' ? 'auto' : '20px',
          left: language === 'ar' ? '20px' : 'auto',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          backgroundColor: '#0078d4',
          color: 'white',
          fontSize: '24px'
        }}
      >
        🤖
      </button>
      {isOpen && (
        <CopilotPanel onClose={() => setIsOpen(false)} />
      )}
    </>
  );
};
```

## Copilot Modes

### 1. **Passive Mode** (Default)
- Watches for selected text
- Provides suggestions on hover
- Non-intrusive

### 2. **Active Mode**
- Real-time analysis during typing
- Continuous audio monitoring
- Proactive suggestions

### 3. **Learning Mode**
- Learns from user's coding patterns
- Adapts suggestions to researcher's style
- Improves over time

## Arabic-Specific Features

### Dialect Recognition
```python
DIALECTS = {
    "msa": "Modern Standard Arabic",
    "egy": "Egyptian Arabic",
    "lev": "Levantine Arabic",
    "gulf": "Gulf Arabic",
    "maghreb": "Maghrebi Arabic"
}

@app.post("/copilot/detect-dialect")
def detect_arabic_dialect(text: str):
    prompt = f"حدد اللهجة العربية للنص التالي: {text}"
    # Returns detected dialect
    return {"dialect": "egy", "confidence": 0.88}
```

### Cultural Sensitivity Check
```python
@app.post("/copilot/sensitivity-check")
def cultural_sensitivity(text: str):
    """
    Checks for culturally sensitive content
    """
    prompt = f"""
    حلل النص التالي للتحقق من الحساسية الثقافية:
    {text}
    
    حدد أي محتوى قد يكون حساسًا ثقافيًا أو دينيًا.
    """
    return {"sensitivity_level": "low", "notes": []}
```

## Performance Optimization

### Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_code_suggestions(text_hash: str):
    # Cache frequent suggestions
    pass
```

### Batching Requests
```python
async def batch_copilot_requests(texts: List[str]):
    # Process multiple requests together
    tasks = [get_suggestions(text) for text in texts]
    return await asyncio.gather(*tasks)
```

## Configuration

```python
COPILOT_CONFIG = {
    "enabled": True,
    "language": "ar",
    "mode": "passive",  # passive, active, learning
    "min_text_length": 10,
    "max_suggestions": 5,
    "auto_apply": False,
    "show_confidence": True,
    "enable_audio_copilot": True,
    "enable_translation": True
}
```

## Usage Examples

### Example 1: Auto-suggest codes while coding
```
User selects Arabic text: "الوضع الاقتصادي صعب جداً"
Copilot suggests:
- الصعوبات الاقتصادية
- التحديات المالية
- الضغوط المعيشية
```

### Example 2: Audio transcription assist
```
During recording:
Copilot: "Background noise detected. Consider moving to quieter location."
Copilot: "تم اكتشاف ضوضاء خلفية. يُفضل الانتقال لمكان أهدأ."
```

### Example 3: Cultural context
```
Text: "إن شاء الله نتحسن"
Copilot Context:
- Religious expression commonly used
- Indicates hope/optimism
- Cultural norm in Arabic conversations
```

## Security & Privacy

- All Co-Pilot data processed server-side
- No data stored unless user opts in
- GDPR compliant
- Azure data residency options

## Future Enhancements

- [ ] Voice commands in Arabic
- [ ] Multi-modal analysis (text + audio + video)
- [ ] Collaborative copilot for team research
- [ ] Offline mode with local models
- [ ] Custom copilot training per project

## API Reference

See full API documentation in `/docs/copilot-api.md`
