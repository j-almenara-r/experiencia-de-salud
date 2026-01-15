# Setup Guide

This guide will help you get the Medical Patient Chatbot up and running.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key (get one at https://platform.openai.com/)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/j-almenara-r/experiencia-de-salud.git
cd experiencia-de-salud
```

### 2. Create a Virtual Environment (Recommended)

**On Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- OpenAI Python SDK
- Pydantic for data validation
- Flask for web interface (future)
- And other necessary packages

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Important:** Never commit your `.env` file to version control!

### 5. Verify Installation

Run the tests to make sure everything is set up correctly:
```bash
pytest tests/
```

You should see all tests passing.

### 6. Run the Application

**Option A: Interactive CLI**
```bash
python app.py
```

**Option B: Demo Script**
```bash
python demo.py
```

The demo will walk you through all features with example data.

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"

Make sure you installed all requirements:
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"

Check that:
1. You created the `.env` file (copy from `.env.example`)
2. You added your actual API key
3. The file is in the root directory of the project

### "Permission denied" when running scripts

Make the scripts executable:
```bash
chmod +x app.py demo.py
```

### Tests failing

Make sure you're in the virtual environment and have installed all dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest tests/
```

## Directory Structure After Setup

```
experiencia-de-salud/
├── .env                    # Your environment variables (DON'T COMMIT!)
├── .env.example            # Example environment file
├── venv/                   # Virtual environment (DON'T COMMIT!)
├── data/                   # Patient data storage (created automatically)
│   └── digital_twins/      # JSON files for each patient
├── src/                    # Source code
├── tests/                  # Test files
├── app.py                  # Main application
└── demo.py                 # Demo script
```

## Next Steps

1. **Read the documentation**: Check out `README.md` for feature overview
2. **Run the demo**: `python demo.py` to see the system in action
3. **Try the CLI**: `python app.py` for interactive use
4. **Read examples**: See `EXAMPLES.md` for sample medical transcripts
5. **Understand architecture**: Review `ARCHITECTURE.md` for technical details

## Configuration Options

You can customize the application by editing `.env`:

```bash
# Model Configuration
LLM_MODEL=gpt-4                        # or gpt-3.5-turbo for lower cost
EMBEDDING_MODEL=text-embedding-3-small

# Application Settings
APP_PORT=5000
DEBUG=False

# Data Storage
DATA_DIR=./data                        # Where to store patient data
```

## Cost Considerations

The application uses OpenAI's API which has associated costs:
- GPT-4: ~$0.03-0.06 per 1K tokens
- GPT-3.5-turbo: ~$0.001-0.002 per 1K tokens

To reduce costs:
1. Use `gpt-3.5-turbo` instead of `gpt-4`
2. Process shorter transcripts
3. Limit conversation history
4. Monitor your usage at https://platform.openai.com/usage

## Security Best Practices

1. **Never share your API key**: Keep `.env` file private
2. **Don't commit sensitive data**: Use `.gitignore` properly
3. **Use test data only**: Never use real patient information during development
4. **Secure your deployment**: Use HTTPS in production
5. **Regular updates**: Keep dependencies updated

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review `EXAMPLES.md` for usage examples
3. Look at `ARCHITECTURE.md` for technical details
4. Search existing GitHub issues
5. Create a new issue with detailed information

## Development Setup

If you want to contribute or develop new features:

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=src tests/

# Check code style
# (Add linting tools as needed)
```

See `CONTRIBUTING.md` for detailed contribution guidelines.

## Platform-Specific Notes

### macOS
- Use Homebrew to install Python if needed: `brew install python`
- May need to use `python3` instead of `python`

### Windows
- Install Python from python.org
- Use PowerShell or Command Prompt
- Paths use backslashes (`\`) instead of forward slashes (`/`)

### Linux
- Python usually pre-installed
- May need to install pip: `sudo apt-get install python3-pip`
- May need to use `python3` instead of `python`

## What's Next?

Once you're set up:
- Explore the CLI application (`app.py`)
- Try the demo (`demo.py`)
- Read through the example transcripts (`EXAMPLES.md`)
- Experiment with your own data
- Consider contributing improvements (see `CONTRIBUTING.md`)

Enjoy using the Medical Patient Chatbot!
