# System Design Document: Autonomous Workflow Discovery & Meta-Agent Generation

## Project File Structure
workflow-discovery-agent/
├── src/
│ ├── task1_workflow_extractor/
│ │ ├── init.py
│ │ ├── data_loader.py
│ │ ├── workflow_extractor.py
│ │ ├── pattern_matcher.py
│ │ └── repetition_counter.py
│ ├── task2_meta_agent/
│ │ ├── init.py
│ │ ├── agent_builder.py
│ │ ├── code_generator.py
│ │ └── workflow_executor.py
│ ├── models/
│ │ ├── init.py
│ │ ├── event_models.py
│ │ └── workflow_schema.py
│ ├── utils/
│ │ ├── init.py
│ │ ├── image_analyzer.py
│ │ └── db_utils.py
│ └── main.py
├── tests/
│ └── test_workflow_extractor.py
├── output/
│ ├── extracted_workflows/
│ └── generated_agents/
├── requirements.txt
├── README.md
├── system_design.md
└── .gitignore

text

## Output Directory Structure (after execution)
output/
├── extracted_workflows/
│ ├── EMP-0025_workflows.json # Raw workflows for employee EMP-0025
│ ├── EMP-0025_patterns.json # Patterns with repetition counts
│ ├── EMP-0028_workflows.json
│ ├── EMP-0028_patterns.json
│ ├── EMP-0053_workflows.json
│ └── EMP-0053_patterns.json
├── generated_agents/
│ ├── P_99beac74/ # Pattern ID folder
│ │ ├── agent.py # Executable agent script
│ │ └── config.json # Agent configuration
│ ├── P_48e8f29c/
│ │ ├── agent.py
│ │ └── config.json
│ └── ... (additional pattern folders)
└── generation_summary.json # Summary of all generated agents


## 1. Overview
This system analyzes desktop activity data from a SQLite database, extracts workflows from user actions and screenshots, and dynamically generates autonomous agents to execute these workflows.

## 2. Architecture

### 2.1 Task 1: Workflow Extraction Architecture

#### Components:
1. **Data Loader Module**
   - Connects to SQLite database
   - Implements capture-first join strategy
   - Filters by employee and date ranges

2. **Workflow Extractor Module**
   - Segments continuous action sequences into logical workflows
   - Uses screenshot analysis for context validation
   - Implements sliding window algorithm for workflow detection

3. **Pattern Matcher Module**
   - Sequence alignment for pattern matching
   - Fuzzy matching for similar but not identical workflows
   - Abstract representation of actions for pattern matching

4. **Repetition Counter Module**
   - Multi-timeframe counting (daily, 2-day, 3-day, 4-day)
   - Persistence detection across non-consecutive days

### 2.2 Task 2: Meta-Agent Architecture

#### Components:
1. **Agent Builder System**
   - Reads workflow definitions from Task 1
   - Dynamically generates automation code
   - Creates configuration for each workflow

2. **Code Generator Module**
   - Template-based code generation
   - PyAutoGUI for screen interaction
   - Error handling and recovery logic

3. **Workflow Executor**
   - Runtime environment for generated agents
   - State management and execution monitoring

## 3. Methodology

### 3.1 Workflow Extraction Approach
- **Anchor to Captures**: Start from captures table and join to events
- **Workflow Segmentation**: Detect natural boundaries (app switches, long pauses)
- **Screenshot Priority**: Use computer vision to validate action sequences
- **Pattern Recognition**: N-gram analysis for repeated sequences

### 3.2 Meta-Agent Generation Approach
- **Dynamic Code Generation**: Python classes generated per workflow
- **Action Mapping**: Map extracted events to executable functions
- **Visual Validation**: Screenshot comparison for state verification
- **Self-Contained Agents**: Each agent independent with its own logic

## 4. Data Flow

1. **Input**: SQLite database with events and captures tables
2. **Processing**: Employee-independent workflow extraction
3. **Pattern Discovery**: Group similar workflows, count repetitions
4. **Agent Generation**: Create executable agents for high-value patterns
5. **Output**: Generated Python agents with configuration

## 5. Key Design Decisions

- **Capture-first approach**: Ensures workflows are aligned with visual evidence
- **Employee isolation**: Prevents mixing patterns across different users
- **Dynamic code generation**: Creates self-contained agents per workflow
- **Multi-timeframe analysis**: Identifies patterns with different persistence levels

## 6. Extensibility

The system is designed to be extended with:
- Additional action types
- Computer vision integration for screenshot analysis
- Machine learning for improved pattern matching
- Cloud deployment capabilities


