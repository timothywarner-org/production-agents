# Troubleshooting

## Common Issues

### API Key Errors

```text
AuthenticationError: Invalid API key
```

**Fix**: Verify your API key is set correctly:

```bash
echo $ANTHROPIC_API_KEY
```

### Package Import Errors

```text
ModuleNotFoundError: No module named 'langgraph'
```

**Fix**: Install dependencies:

```bash
pip install -r requirements.txt
```

### CrewAI Not Working

```text
ImportError: cannot import name 'Agent' from 'crewai'
```

**Fix**: Upgrade CrewAI:

```bash
pip install --upgrade crewai
```

### MCP Server Won't Start

**Fix**: Check Docker is running:

```bash
docker ps
```

### Rate Limit Errors

```text
RateLimitError: Rate limit exceeded
```

**Fix**:

- Wait and retry
- Use a smaller model
- Reduce request frequency

## Getting Help

1. Check [O'Reilly platform](https://learning.oreilly.com/)
2. Open an issue on GitHub
3. Ask during the live session
