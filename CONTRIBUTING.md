# Contributing to Medical Patient Chatbot

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

This project adheres to professional standards of conduct. We expect all contributors to:
- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or screenshots

### Suggesting Enhancements

We welcome enhancement suggestions! Please:
- Use a clear, descriptive title
- Provide a detailed description of the enhancement
- Explain why this enhancement would be useful
- Include examples if applicable

### Pull Requests

1. **Fork the repository** and create a branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you're adding functionality
4. **Update documentation** as needed
5. **Ensure tests pass** by running `pytest`
6. **Submit a pull request** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/experiencia-de-salud.git
cd experiencia-de-salud

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run tests
pytest tests/
```

## Coding Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all public functions/classes
- Keep functions focused and small
- Maximum line length: 100 characters

### Docstring Format
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Testing
- Write unit tests for new functionality
- Aim for high test coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

Example:
```
Add patient data export functionality

- Implement JSON export for digital twins
- Add CSV export for consultation history
- Update documentation

Closes #123
```

## Project Structure

```
experiencia-de-salud/
├── src/                    # Source code
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── app.py                 # Main CLI application
├── demo.py                # Demo script
└── README.md              # Documentation
```

## Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Web interface (Flask/FastAPI + React)
- [ ] Real-time audio transcription
- [ ] Multi-language support
- [ ] Enhanced security and encryption
- [ ] Integration with medical databases

### Medium Priority
- [ ] More comprehensive test coverage
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] Logging improvements
- [ ] Configuration management

### Documentation
- [ ] API documentation
- [ ] Usage tutorials
- [ ] Video demonstrations
- [ ] Translation to other languages

## Medical and Privacy Considerations

### Important Guidelines

When contributing to this project, remember:

1. **This is NOT a medical device**: Always include appropriate disclaimers
2. **Privacy first**: Be extremely careful with any patient data
3. **Security matters**: Follow security best practices
4. **Accuracy is critical**: Medical information must be handled carefully
5. **Regulatory awareness**: Be aware of healthcare regulations (HIPAA, GDPR, etc.)

### Testing with Medical Data

- **Never use real patient data** for testing or development
- Use synthetic/fictitious data only
- Don't commit any patient information to the repository
- Be careful with API calls that might log sensitive information

## Review Process

1. All submissions require review before merging
2. Maintainers will review for:
   - Code quality and style
   - Test coverage
   - Documentation completeness
   - Security implications
   - Medical accuracy (if applicable)
3. Be responsive to feedback and questions
4. Updates may be requested before merging

## Recognition

Contributors will be:
- Listed in the project's contributors
- Mentioned in release notes for significant contributions
- Credited in documentation when appropriate

## Questions?

If you have questions:
- Check existing issues and discussions
- Create a new issue with your question
- Tag it appropriately

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make healthcare information more accessible and understandable for patients. Thank you for your support!
