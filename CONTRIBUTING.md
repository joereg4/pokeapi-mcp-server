# Contributing to PokeAPI MCP Server

Thank you for your interest in contributing to the PokeAPI MCP Server! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- Python 3.11+
- Git
- Basic understanding of MCP (Model Context Protocol)

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/pokeapi-mcp-server.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up development environment:
   ```bash
   cd pokeapi-mcp-server
   pip install -r requirements.txt
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add type hints where appropriate
- Keep functions focused and single-purpose

### MCP Tool Development
When adding new tools:

1. **Use the `@mcp.tool()` decorator**
2. **Single-line docstrings only** (multi-line causes gateway errors)
3. **Default parameters to empty strings** (`param: str = ""` not `None`)
4. **Return formatted strings** with emojis for LLM-friendly output
5. **Include error handling** with user-friendly messages

Example:
```python
@mcp.tool()
async def new_tool(identifier: str = "") -> str:
    """Single-line description of what this tool does."""
    if not identifier.strip():
        return "❌ Error: Identifier is required"
    
    try:
        # Implementation here
        return f"✅ Success: {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

### Testing
Before submitting:
1. Test your changes locally: `python pokeapi_server.py`
2. Test with Docker: `docker build -t test-server .`
3. Verify MCP protocol: `echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python pokeapi_server.py`

## 📝 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] New tools have proper error handling
- [ ] Documentation is updated
- [ ] Tests pass locally
- [ ] Docker image builds successfully

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
- [ ] Tested with Docker
- [ ] Verified MCP protocol

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🐛 Bug Reports

When reporting bugs, please include:
- Operating system and version
- MCP client being used (Cursor, Claude Desktop, etc.)
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## 💡 Feature Requests

For new features:
- Check existing issues first
- Provide clear use case
- Consider backward compatibility
- Think about LLM usability

## 📋 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed

## 🏷️ Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Update documentation

## 📞 Getting Help

- Check existing [Issues](https://github.com/yourusername/pokeapi-mcp-server/issues)
- Join discussions in [Discussions](https://github.com/yourusername/pokeapi-mcp-server/discussions)
- Create a new issue for bugs or feature requests

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to the PokeAPI MCP Server! 🎉
