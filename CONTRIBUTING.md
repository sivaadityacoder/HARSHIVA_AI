# Contributing to HARSHIVA AI

## 🤝 How to Contribute

We welcome contributions to HARSHIVA AI! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

## 🚀 Getting Started

### 1. Fork the Repository
- Click the "Fork" button on the top right of the GitHub page
- Clone your fork locally:
```bash
git clone https://github.com/yourusername/harshiva-ai.git
cd harshiva-ai
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
python src/harshiva_ai.py --verify-ai
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## 🎯 Types of Contributions

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Provide system information (OS, Python version)
- Include error messages and logs

### 💡 Feature Requests
- Check existing issues first
- Clearly describe the feature and its benefits
- Consider implementation complexity

### 🔧 Code Contributions
- **AI Personalities**: New hacker personalities for different assessment styles
- **Assessment Modules**: Additional vulnerability detection capabilities
- **Reporting**: Enhanced output formats and visualizations
- **Performance**: Optimization and efficiency improvements

### 📖 Documentation
- README improvements
- Code comments and docstrings
- Tutorial and example creation
- API documentation

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 for Python code formatting
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include type hints where appropriate

### Testing
- Test your changes thoroughly
- Include test cases for new features
- Verify AI model integration still works
- Test on different target types

### Commit Messages
Use clear, descriptive commit messages:
```
Add new STEALTH AI personality for passive reconnaissance
Fix vulnerability detection accuracy in PHP applications
Update documentation for new Google dork techniques
```

## 🔒 Security Considerations

### Ethical Guidelines
- **Authorized testing only**: Ensure all code promotes ethical usage
- **No malicious payloads**: Avoid including actual exploit code
- **Educational focus**: Maintain the tool's educational purpose
- **Responsible disclosure**: Include guidelines for reporting vulnerabilities

### Code Review Requirements
- All AI personality changes must be reviewed
- New assessment techniques require security validation
- Documentation updates need accuracy verification

## 🚀 Submission Process

### Pull Request Checklist
- [ ] Code follows the project style guidelines
- [ ] Changes are tested and working
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] No large files (models) are included
- [ ] Ethical guidelines are followed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] AI model integration verified
- [ ] No ethical concerns

## Additional Notes
Any additional information or context
```

## 🏆 Recognition

Contributors will be:
- Listed in the README contributors section
- Mentioned in release notes
- Given credit in code comments where appropriate

## 📞 Getting Help

- **Questions**: Open a GitHub discussion
- **Issues**: Use the GitHub issue tracker
- **Real-time chat**: (Add Discord/Slack if available)

## 📋 Project Roadmap

### Current Priorities
1. **Enhanced AI Models**: Integration with newer LLM models
2. **Web Interface**: User-friendly web-based dashboard
3. **API Development**: RESTful API for integration
4. **Mobile Support**: Mobile app for security assessments

### Future Goals
- Multi-language support for international users
- Cloud deployment options
- Integration with popular security tools
- Academic partnerships for research

Thank you for contributing to HARSHIVA AI! 🚀