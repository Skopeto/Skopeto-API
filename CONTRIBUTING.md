# Contributing to Server Monitoring Tool

Thank you for your interest in contributing! We welcome contributions from the community.

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🌍 Translate to other languages

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 14+ (or Oracle/MySQL) database of you choosing if you configure it. 
- Repository implementation is pretty basic sql little conflicts will arise from oracle specific or postgress SQL
- Docker & Docker Compose
- Git

### Local Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/Skopeto/Skopeto-API.git
cd Skopeto-API
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
uv sync
# or
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run the database**
```bash
docker compose up -d
```

6. **migrations**
- Run schema.sql dump inside docker container
- Note this is for development and fast setup only - safer persistance is required for production

7. **Start the development server**
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000`

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding tests

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation if needed

### 3. Run Tests
```bash
pytest
# Run with coverage
pytest --cov=app tests/
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add container health check feature"
```

**Commit message format:**
```
<type>: <description>

[optional body]

[optional footer]
```
**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add Slack notification integration
fix: resolve SSH connection timeout issue
docs: update installation instructions
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

## Pull Request Guidelines

### Before Submitting

- ✅ Code follows project style
- ✅ Tests pass (`pytest`)
- ✅ New features have tests
- ✅ Documentation is updated
- ✅ Commit messages are clear
- ✅ No merge conflicts

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test this?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Code Style

### Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) with some modifications:

- Line length: 100 characters (not 79)
- Use type hints
- Use async/await for I/O operations
- No comments per user preferences

**Format your code:**
```bash
# Install formatters
uv add --dev black isort

# Format code
black app/
isort app/
```

**Example:**
```python
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.domain.entity.user import User

router = APIRouter()

async def get_server_by_id(
    server_id: int,
    current_user: User = Depends(get_current_user)
) -> Server:
    server = await server_repo.get_by_id(server_id)
    
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    return server
```

### Project Structure
```
app/
├── core/                  # Core utilities
│   ├── security.py
│   └── db.py
├── modules/              # Feature modules
│   ├── auth/
│   │   ├── application/  # Use cases
│   │   ├── domain/       # Entities & interfaces
│   │   └── infrastructure/ # Repositories
│   └── monitoring/
└── main.py              # Application entry point
```

**Follow clean architecture principles:**
- Domain layer: Pure business logic
- Application layer: Use cases
- Infrastructure layer: External dependencies

## Testing

### Writing Tests

Place tests in `tests/` directory mirroring the app structure:
```
tests/
├── the_registry/
│   ├── unit_tests
│   │   └──test_collect_docker_container.py
│   └── cofntest.py

**Example unit test:**
```python
import pytest
from app.modules.auth.application.use_case.register_user_use_case import register_user_use_case

@pytest.mark.asyncio
async def test_register_user_success(mock_user_repository):
    request = RegisterUserRequest(
        user_name="johndoe",
        email="john@example.com",
        password="SecurePass123!",
        user_type=UserType.ADMIN
    )
    
    user = await register_user_use_case(request, mock_user_repository)
    
    assert user.user_name == "johndoe"
    assert user.email == "john@example.com"
```

### Running Tests
```bash
pytest

pytest tests/unit

pytest --cov=app --cov-report=html
```

## Documentation

### Updating Documentation

Documentation lives in:
- `README.md` - Main project overview
- `docs/` - Detailed guides
- Code docstrings - API documentation

**Docstring example:**
```python
async def check_server_health(server: Server) -> dict:
    """
    Check the health of a server via SSH.
    
    Args:
        server: Server entity with connection details
        
    Returns:
        dict: Health metrics including CPU, RAM, and disk usage
        
    Raises:
        SSHConnectionError: If SSH connection fails
    """
    ...
```

## Feature Requests

Have an idea? Great!

1. **Check existing issues** - Maybe it's already proposed
2. **Open a discussion** - In GitHub Discussions
3. **Describe the problem** - What are you trying to solve?
4. **Propose a solution** - How would you implement it?

## Bug Reports

Found a bug? Help us fix it!

### Bug Report Template
```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.12]
- Database: [e.g. PostgreSQL 16]

**Additional context**
Any other relevant information
```

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- No harassment or discrimination

### Getting Help

- 📖 Check [documentation](docs/)
- 💬 Ask in [GitHub Discussions](https://github.com/you/monitoring-tool/discussions)
- 🐛 Open an [issue](https://github.com/you/monitoring-tool/issues)

## Recognition

Contributors will be:
- Added to [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Mentioned in release notes
- Acknowledged in the README

## License

By contributing, you agree that your contributions will be licensed under the AGPL-3.0 License.

---

## Quick Contribution Checklist

- [ ] Forked and cloned the repo
- [ ] Created a feature branch
- [ ] Made changes following code style
- [ ] Added tests for new features
- [ ] All tests pass
- [ ] Updated documentation
- [ ] Committed with clear messages
- [ ] Pushed and created PR

---

**Questions?** Open a discussion or reach out at contribute@yourapp.com

Thank you for contributing! 🎉