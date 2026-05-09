import json
from flask import Flask, request, Response
from openai import OpenAI  # Install with: pip install openai

app = Flask(__name__)

# ================= Core Configuration =================
# 1. Fill in your DeepSeek API Key
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY_HERE" 

# 2. Initialize DeepSeek client (compatible with OpenAI format)
client = OpenAI(
    api_key=DEEPSEEK_API_KEY, 
    base_url="https://api.deepseek.com"
)
# =============================================

@app.route('/analyze', methods=['POST'])
def analyze_waveform():
    try:
        # 1. Parse waveform array from LabVIEW
        data = request.get_json(force=True)
        print("\n[+] Received real-time waveform data from LabVIEW!")
        
        # 2. Data preprocessing: Take first 50 samples to avoid exceeding AI context limit
        waveform_points = data if isinstance(data, list) else []
        analysis_sample = waveform_points[:50]
        print(f"Data preview: {analysis_sample}...")

        # 3. Construct AI prompt
        prompt = f"""
        You are a senior industrial signal analysis expert.
        My oscilloscope just captured a set of waveform data. Here are the first 50 samples:
        {analysis_sample}
        
        Please analyze this data:
        1. Briefly analyze the waveform trend (e.g., smooth sine wave, noisy signal, DC level, etc.)
        2. Provide a 100-word AI diagnostic report evaluating the system's operational status.
        Please provide the report directly in professional and concise language.
        """

        # 4. Call DeepSeek LLM
        print("[*] Requesting DeepSeek AI analysis, please wait...")
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a professional virtual instrument signal analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 # Sampling temperature, 0.7 balances professionalism with flexibility
        )

        # Get AI-generated report
        ai_report = completion.choices[0].message.content
        print("[√] AI analysis report generated!")

        # 5. Return response with GBK encoding for LabVIEW compatibility
        response_json = json.dumps({
            "status": "success",
            "report": ai_report
        }, ensure_ascii=False)
        
        return Response(
            response_json.encode('gbk'), 
            content_type="application/json; charset=gbk"
        )

    except Exception as e:
        print(f"[X] Error occurred: {str(e)}")
        # Return error info to LabVIEW for debugging
        error_info = json.dumps({
            "status": "error", 
            "report": f"AI analysis failed: {str(e)}"
        }, ensure_ascii=False)
        return Response(
            error_info.encode('gbk'), 
            content_type="application/json; charset=gbk"
        )

if __name__ == '__main__':
    print("🚀 [DeepSeek Smart Oscilloscope] Backend started!")
    print("📍 Listening on http://127.0.0.1:5000/analyze")
    app.run(host='127.0.0.1', port=5000)