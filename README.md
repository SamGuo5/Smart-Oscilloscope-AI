# Smart-Oscilloscope-AI
Smart Oscilloscope AI Analysis System - Integrating traditional oscilloscope with large language models for intelligent waveform diagnostic analysis


## Features
- 📊 Real-time waveform acquisition and display
- 🤖 Intelligent waveform analysis based on DeepSeek LLM
- 📝 Auto-generated professional diagnostic reports
- 🔄 Seamless communication between LabVIEW and Python


### Requirements
- LabVIEW 2020 or later
- Python 3.8+

### Installation
```bash
pip install flask openai
```

### Quick Start
1. **Start Python backend**:
   ```bash
   cd Python
   python ai_server.py
   ```

2. **Open LabVIEW interface**:
   - Run `LabVIEW/Smart_Oscilloscope.vi`
   - Ensure oscilloscope hardware is connected

3. **Configure API Key**:
   - Set your DeepSeek API Key in `ai_server.py`

## API Endpoints

### POST /analyze
Analyze waveform data

**Request Body**: Waveform data array (JSON format)

**Response**:
```json
{
    "status": "success",
    "report": "AI 诊断报告内容..."
}
```

## License
MIT License