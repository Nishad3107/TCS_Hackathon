# 🚀 How to Run - Travel Itinerary AI Agent

## Quick Start (2 Minutes)

### Step 1: Setup Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Verify dependencies (already installed)
pip list | grep streamlit
```

### Step 2: Configure API Key
Make sure your `.env` file exists with a valid API key:
```bash
# Check if .env exists
cat .env

# If not, copy from example
cp .env.example .env
nano .env  # Add your API key
```

### Step 3: Run the App

**🌐 Web Interface (Recommended)**
```bash
streamlit run app.py
```
- Opens automatically at `http://localhost:8501`
- Beautiful UI with animations
- Interactive forms
- One-click download

**💻 Command Line Interface**
```bash
python main.py
```
- Terminal-based interaction
- Rich formatted output
- Quick for power users

---

## 🎯 First Time Usage

### For Web App:
1. Launch: `streamlit run app.py`
2. Browser opens to `http://localhost:8501`
3. Fill the form:
   - Destination: "Paris"
   - Duration: 3 days
   - Budget: Medium
   - Interests: Food, Culture
4. Click "🚀 Generate Itinerary"
5. Wait ~30 seconds for AI magic
6. View your beautiful itinerary!
7. Download as PDF or Markdown

### For CLI:
1. Launch: `python main.py`
2. Type: "Plan a 3-day trip to Paris for food and culture lovers. Medium budget."
3. Confirm with 'y'
4. Wait for generation
5. Choose to save or export

---

## 📋 Pre-flight Checklist

Before running, ensure:
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] `.env` file exists with valid API key
- [ ] Internet connection active
- [ ] Port 8501 available (for web app)
- [ ] Dependencies installed (`pip list`)

---

## 🐛 Common Issues & Solutions

### Issue: "streamlit: command not found"
**Solution:**
```bash
source venv/bin/activate
pip install streamlit
```

### Issue: "API key not found"
**Solution:**
```bash
# Create .env file
cp .env.example .env

# Add your key
echo "GOOGLE_API_KEY=your_key_here" >> .env
echo "MODEL_NAME=gemini-1.5-flash" >> .env
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

### Issue: "Module not found"
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎨 Customization

### Change Port
```bash
streamlit run app.py --server.port 8080
```

### Run in Background
```bash
nohup streamlit run app.py &
```

### Enable Auto-reload
```bash
streamlit run app.py --server.runOnSave true
```

---

## 📊 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Internet**: Required for API calls and search
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

---

## 🌟 What to Expect

### Web App Experience:
1. **Load Time**: 2-3 seconds
2. **Generation Time**: 20-60 seconds (depends on API)
3. **Validation**: 5-10 seconds additional
4. **Export**: Instant for Markdown, 2-3 seconds for PDF

### Features Available:
- ✅ Interactive form inputs
- ✅ Real-time progress bars
- ✅ Animated card displays
- ✅ Activity validation
- ✅ PDF/Markdown export
- ✅ Responsive design

---

## 💡 Pro Tips

1. **Keep terminal open** - Watch for error messages
2. **Check browser console** - F12 for debugging
3. **Use valid destinations** - "Paris, France" works better than just "Paris"
4. **Be specific with interests** - Better results with clear preferences
5. **Validate activities** - Especially for lesser-known destinations
6. **Save your itineraries** - Download before closing browser

---

## 🔄 Stopping the App

### Web App:
- Press `Ctrl+C` in terminal
- Or close the terminal window

### CLI:
- Type `exit` or `quit`
- Or press `Ctrl+C`

---

## 📸 What You'll See

### Homepage:
- Purple gradient hero section
- Interactive form with dropdowns and sliders
- Sidebar with quick guide
- Example destinations

### Results Page:
- Statistics cards (Days, Destination, Budget, Interests)
- Day-by-day cards with morning/afternoon/evening activities
- Action buttons (Validate, Download, Export)
- Beautiful animations on scroll

---

## 🎓 Demo Script for Hackathon

```bash
# 1. Start app
streamlit run app.py

# 2. In browser (while explaining features):
# - Point out beautiful UI
# - Show interactive form
# - Mention AI-powered planning

# 3. Fill form with impressive destination:
Destination: Dubai
Duration: 7 days
Budget: Luxury
Interests: Adventure, Shopping, Culture

# 4. Click Generate (explain while waiting):
# - Real attraction search
# - Weather integration
# - Smart daily planning

# 5. Show results:
# - Beautiful day cards
# - Activity validation
# - PDF export

# 6. Emphasize unique features:
# - Custom CSS animations
# - Activity verification
# - Multiple LLM support
# - Responsive design
```

---

## 📞 Need Help?

1. **Check Logs**: Terminal output shows detailed errors
2. **Browser Console**: F12 for JavaScript errors
3. **API Status**: Verify keys in `.env`
4. **Dependencies**: Run `pip list` to check installations
5. **Network**: Test internet connection

---

**Ready to create amazing travel itineraries? Let's go! 🌍✈️**

```bash
streamlit run app.py
```
