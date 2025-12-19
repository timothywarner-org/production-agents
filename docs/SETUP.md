# Setup Guide

## Prerequisites

- Python 3.11+
- Docker Desktop (for MCP servers)
- Git

## Step 1: Clone Repository

```bash
git clone https://github.com/timothywarner-org/production-agents.git
cd production-agents
```

## Step 2: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure API Keys

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Step 5: Verify Setup

```bash
python -m scripts.verify_setup
```

## Step 6: Run First Example

```bash
python -m segment_1_foundations.01_what_is_an_agent
```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
