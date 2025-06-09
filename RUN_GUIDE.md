# Marketing Agency AI - Quick Start Guide

🎯 **Welcome to the Marketing Agency AI Assistant!**

This AI-powered marketing agency can help you with domain suggestions, website creation, marketing strategies, and logo design.

## ✅ Prerequisites Verified

- ✅ Python 3.11+ installed
- ✅ Virtual environment activated (`venv_adk`)
- ✅ Google Cloud credentials configured
- ✅ All dependencies installed
- ✅ Environment variables properly set

## 🚀 How to Run

### Option 1: Interactive Demo (Recommended)

```bash
# Navigate to the project directory
cd /Users/amerlin/Desktop/market_agent_google/marketing-agency

# Activate virtual environment (if not already active)
source ../venv_adk/bin/activate

# Run the interactive marketing agency
python run_marketing_agency.py
```

### Option 2: Interactive Chat Mode

```bash
python run_marketing_agency.py --interactive
```

### Option 3: Run Tests

```bash
# Run the basic test suite
python -m pytest tests/test_agents.py -v

# Run the demo test
python demo_test.py
```

## 🎯 What the Marketing Agency Can Do

### 1. **Domain Name Suggestions** 🌐
- Generates 10 unique, available domain names
- Uses Google Search to verify availability
- Provides creative and relevant suggestions

### 2. **Website Creation** 💻
- Creates complete multi-page websites
- Responsive HTML5 design
- Professional CSS styling
- Contact forms and navigation

### 3. **Marketing Strategy** 📈
- Develops comprehensive marketing plans
- Target audience analysis
- Campaign recommendations
- Brand positioning advice

### 4. **Logo Design** 🎨
- AI-generated logo concepts
- Uses Google's Imagen 3.0 model
- Creates visual brand identity
- Saves logo files as artifacts

## 📝 Example Usage

### Sample Prompts:

1. **Starting a Business:**
   ```
   I want to start a bakery called "Sweet Dreams Bakery". 
   Can you help me create a complete marketing package?
   ```

2. **Domain Suggestions:**
   ```
   I need domain name suggestions for my tech startup "InnovateTech".
   ```

3. **Website Creation:**
   ```
   Create a website for my restaurant "Gourmet Garden" 
   that serves organic farm-to-table cuisine.
   ```

4. **Logo Design:**
   ```
   I need a logo for my fitness app called "FitTracker Pro".
   ```

## 🔧 Configuration Details

### Environment Variables (`.env`):
```bash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=gen-lang-client-0519496639
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/Users/amerlin/Desktop/market_agent_google/marketing-agency/credentials/google_service-account-key.json
VERTEX_AI_ENDPOINT=https://us-central1-aiplatform.googleapis.com
GEMINI_MODEL=gemini-2.5-pro-preview-05-06
IMAGEN_MODEL=imagen-3.0-generate-002
DEBUG=True
```

### Sub-Agents Architecture:
- **Root Agent**: Coordinates all sub-agents
- **Domain Create Agent**: Generates and verifies domain names
- **Website Create Agent**: Creates complete websites
- **Marketing Create Agent**: Develops marketing strategies
- **Logo Create Agent**: Generates logo designs

## 🛠️ Troubleshooting

### Common Issues:

1. **Authentication Error:**
   - Ensure `GOOGLE_APPLICATION_CREDENTIALS` points to the correct service account key
   - Verify Google Cloud project permissions

2. **Import Error:**
   - Make sure virtual environment is activated
   - Check that all dependencies are installed: `pip install -r tests/requirements.txt`

3. **API Quota Issues:**
   - Check Google Cloud console for API usage
   - Ensure Vertex AI API is enabled

### Verification Commands:

```bash
# Test basic functionality
python -c "from marketing_agency.agent import root_agent; print('✅ Agent loaded successfully')"

# Run basic test
python -m pytest tests/test_agents.py::test_happy_path -v

# Check Google Cloud authentication
gcloud auth list
```

## 📊 Expected Output

When you run the marketing agency, you should see:

1. **Domain Suggestions**: List of 10 available domain names
2. **Website Code**: Complete HTML, CSS, and JavaScript files
3. **Marketing Strategy**: Detailed marketing plan and recommendations
4. **Logo Design**: Generated logo image saved as artifact

## 🎉 Success!

Your Marketing Agency AI is now ready to help you build your business! 

Try running one of the sample scenarios or ask for help with your own business idea.

---

**Need Help?** 
- Check the `docs/` directory for detailed documentation
- Review the test files in `tests/` for more examples
- Examine the sub-agent implementations in `marketing_agency/sub_agents/`