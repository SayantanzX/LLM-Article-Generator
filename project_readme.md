# 🤖 LLM Article Generator

A powerful web application that generates articles using multiple Large Language Models (LLMs) including GPT-Neo, Bloom, and OPT, with comprehensive analytics and a user-friendly Streamlit interface.

## ✨ Features

- **Multiple LLM Support**: GPT-Neo 1.3B, Bloom-560M, OPT-1.3B
- **Interactive Web Interface**: Clean, modern Streamlit UI
- **Real-time Analytics**: Track usage patterns and model performance
- **Lazy Loading**: Models load only when needed to optimize memory
- **Export Functionality**: Download articles and analytics data
- **Memory Management**: Built-in cache clearing and optimization
- **Error Handling**: Robust error handling and user feedback

## 🏗️ Project Structure

```
llm-article-generator/
├── app.py                 # Main Streamlit application
├── llm_handler.py         # LLM loading and response generation
├── analytics.py           # Analytics tracking and data management
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
├── run.bat               # Windows run script
├── run.sh                # Unix run script
├── README.md             # This file
├── interactions.csv      # User interaction logs (generated)
├── analytics.json        # Analytics data (generated)
└── models/               # Model cache directory (created)
```

## 🚀 Quick Start

### Method 1: Automated Setup (Recommended)

1. **Clone or download the project files**

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Start the application:**
   - **Windows:** Double-click `run.bat`
   - **Linux/Mac:** `./run.sh`
   - **Manual:** `streamlit run app.py`

4. **Open your browser** to `http://localhost:8501`

### Method 2: Manual Setup

1. **Install Python 3.8+**
   - Download from [python.org](https://python.org)
   - Verify: `python --version`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📋 System Requirements

### Minimum Requirements
- **Python:** 3.8 or higher
- **RAM:** 8GB (16GB recommended)
- **Storage:** 10GB free space
- **Internet:** Required for initial model downloads

### Recommended Requirements
- **Python:** 3.10+
- **RAM:** 16GB+ 
- **GPU:** NVIDIA GPU with 8GB+ VRAM (optional, for faster inference)
- **Storage:** 20GB+ SSD

## 🔧 Installation Guide

### Step 1: Environment Setup

**Using Conda (Recommended):**
```bash
# Create new environment
conda create -n llm-generator python=3.10
conda activate llm-generator

# Install PyTorch (choose appropriate version)
# CPU only:
conda install pytorch cpuonly -c pytorch

# GPU (CUDA 11.8):
conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia
```

**Using pip with virtual environment:**
```bash
# Create virtual environment
python -m venv llm-env

# Activate environment
# Windows:
llm-env\Scripts\activate
# Linux/Mac:
source llm-env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

## 🎯 Usage Guide

### 1. Article Generation

1. **Open the application** in your browser
2. **Navigate to "Article Generator"**
3. **Enter your topic** in the text area
4. **Select an LLM** from the dropdown
5. **Adjust max length** if needed
6. **Click "Generate Article"**
7. **Download** the generated article if satisfied

**Example Prompts:**
- "Write an article about renewable energy benefits"
- "The impact of artificial intelligence on healthcare"
- "Sustainable agriculture practices for the future"

### 2. Analytics Dashboard

- **View usage statistics**: Total queries, unique topics, model usage
- **Analyze trends**: Query patterns over time
- **Export data**: Download CSV or JSON files
- **Response analysis**: Length distribution and quality metrics

### 3. Settings & Management

- **Model status**: View loaded/unloaded models
- **Memory management**: Clear model cache when needed
- **Data management**: Clear analytics data
- **System info**: Check GPU availability and versions

## 🛠️ Configuration Options

### Model Configuration

Edit `llm_handler.py` to modify:
- **Generation parameters**: Temperature, repetition penalty
- **Response length**: Default and maximum lengths
- **Memory optimization**: Device mapping, data types

### UI Customization

Edit `app.py` to customize:
- **Styling**: CSS modifications
- **Layout**: Column arrangements, page structure
- **Features**: Add new functionality or models

## 🔍 Troubleshooting

### Common Issues

**1. Out of Memory Errors**
```bash
# Solution: Use CPU mode or smaller models
export CUDA_VISIBLE_DEVICES=""
# Or clear model cache frequently
```

**2. Model Loading Fails**
```bash
# Solution: Check internet connection and disk space
# Manually download models if needed
```

**3. Streamlit Port Issues**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

**4. Permission Errors**
```bash
# Windows: Run as administrator
# Linux/Mac: Check file permissions
chmod +x run.sh
```

### Performance Optimization

**For Limited RAM:**
- Use only one model at a time
- Reduce max_length parameter
- Clear cache after each session

**For Better Performance:**
- Use GPU if available
- Increase batch size for multiple queries
- Use SSD storage for model cache

## 📊 Model Information

| Model | Size | Parameters | Use Case |
|-------|------|------------|----------|
| GPT-Neo 1.3B | ~5GB | 1.3 billion | General text generation |
| Bloom-560M | ~2GB | 560 million | Multilingual, faster |
| OPT-1.3B | ~5GB | 1.3 billion | Optimized for dialogue |

### Model Comparison

- **GPT-Neo**: Best for creative writing and general articles
- **Bloom**: Good for multilingual content and faster responses
- **OPT**: Optimized for conversational and explanatory content

## 🔒 Security & Privacy

- **Local Processing**: All models run locally, no data sent to external servers
- **Data Storage**: Interactions stored locally in CSV/JSON format
- **No Telemetry**: No usage data transmitted externally
- **Open Source**: All code is transparent and modifiable

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature-name`
3. **Make changes** and test thoroughly
4. **Submit pull request** with detailed description

### Adding New Models

1. **Update `model_names` in `llm_handler.py`**
2. **Test model loading and generation**
3. **Update documentation and requirements**

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Added lazy loading for memory optimization
- ✅ Enhanced error handling and user feedback
- ✅ Improved analytics with visualizations
- ✅ Added settings page and system management
- ✅ Better UI/UX with modern styling
- ✅ Export functionality for articles and data

### Version 1.0
- ✅ Basic article generation
- ✅ Multiple LLM support
- ✅ Simple analytics tracking
- ✅ CSV data storage

## 🐛 Known Issues

- **First model load**: Takes 2-5 minutes depending on internet speed
- **Memory usage**: Models require significant RAM (8GB+ recommended)
- **GPU compatibility**: Some older GPUs may not be supported

---

## 🚨 Important Notes

1. **First Run**: Initial model download requires internet connection and may take several minutes
2. **Disk Space**: Ensure at least 10GB free space for model storage
3. **Memory**: Close other applications if experiencing memory issues
4. **Updates**: Check for dependency updates regularly for security and performance
5. **Backup**: Export analytics data before clearing or reinstalling

