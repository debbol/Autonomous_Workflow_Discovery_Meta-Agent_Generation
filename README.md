# Autonomous Workflow Discovery & Meta-Agent Generation

## Overview
This system analyzes desktop activity data, discovers high-value workflows, and dynamically generates autonomous agents to execute them.

## Features
- **Workflow Extraction**: Extract workflows from raw desktop activity data
- **Pattern Recognition**: Identify repeated workflow patterns
- **Multi-timeframe Analysis**: Count repetitions across 1-4 day periods
- **Meta-Agent Generation**: Automatically build agents for discovered workflows
- **Autonomous Execution**: Generated agents can execute workflows without human intervention

## Installation

```bash
# Clone repository
git clone <repository-url>
cd workflow-discovery-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
