# Training Data Guide

## Overview

The AI Digital Clutter Cleaner supports two modes for document classification:

1. **Synthetic Data (Default)**: Uses pre-defined synthetic examples for demonstration
2. **Real Datasets (Recommended)**: Uses data from 20 Newsgroups and AG News for better accuracy

## Generating Training Data from Real Datasets

### Step 1: Install Dependencies

The `datasets` library is already included in `requirements.txt`. If not installed:

```bash
pip install datasets
```

### Step 2: Generate Training Data

Run the included script to download and process real datasets:

```bash
python generate_training_data.py
```

This will:
- Download 20 Newsgroups dataset (via scikit-learn)
- Download AG News dataset (via Hugging Face)
- Map public dataset categories to the app's 8 categories
- Create `training_data.csv` with ~1000+ labeled examples

**Note**: Requires internet connection on first run (~50MB total download).

### Step 3: Use Real Training Data in the App

1. Start the application: `streamlit run app.py`
2. Navigate to "AI Organization" page
3. Check the "Use Real Training Data" checkbox
4. Click "Classify Files"

The classifier will now use the real training data from `training_data.csv` instead of synthetic examples.

## Available Datasets

### 20 Newsgroups
- **Source**: scikit-learn
- **Size**: ~18,000 documents
- **Categories**: 20 topics (computers, science, religion, sports, politics, etc.)
- **Mapped to**: Software and Code, Education and Notes, Personal Documents

### AG News
- **Source**: Hugging Face
- **Size**: 120,000 documents
- **Categories**: World, Sports, Business, Sci/Tech
- **Mapped to**: Miscellaneous, Personal Documents, Work and Projects, Software and Code

## Category Mapping

The DatasetLoader automatically maps public dataset categories to the app's 8 categories:

| Public Category | App Category |
|----------------|--------------|
| comp.* (computers) | Software and Code |
| sci.* (science) | Software and Code / Education and Notes |
| rec.* (recreation) | Personal Documents |
| talk.* (discussions) | Personal Documents |
| Business | Work and Projects |
| Sci/Tech | Software and Code |
| World | Miscellaneous |
| Sports | Personal Documents |

## Custom Training Data

You can create your own `training_data.csv` with the following format:

```csv
text,label,source
"Your document text here","Work and Projects","custom"
"Another document","Finance and Bills","custom"
```

Place this file in the project root and check "Use Real Training Data" in the app.

## Dataset Licenses

When using datasets for production or redistribution, ensure you comply with their licenses:

- **20 Newsgroups**: Public domain
- **AG News**: Licensed for research use
- Check individual dataset cards for specific terms

## Performance Comparison

- **Synthetic Data**: Good for demonstration, may misclassify real documents
- **Real Datasets**: Significantly better accuracy on real-world content
- **Custom Data**: Best when you have domain-specific documents

## Troubleshooting

### "training_data.csv not found"
Run `python generate_training_data.py` to generate the file.

### Slow loading on first use
The datasets are downloaded on first run. Subsequent uses will be faster.

### Internet connection required
Only for generating training data. The app itself works offline once trained.
