# System Design Document: Autonomous Workflow Discovery & Meta-Agent Generation
# file structure

workflow-discovery-agent/
├── src/
│   ├── task1_workflow_extractor/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── workflow_extractor.py
│   │   ├── pattern_matcher.py
│   │   └── repetition_counter.py
│   ├── task2_meta_agent/
│   │   ├── __init__.py
│   │   ├── agent_builder.py
│   │   ├── code_generator.py
│   │   └── workflow_executor.py
│   ├── models/
│   │   ├── workflow_schema.py
│   │   └── event_models.py
│   └── utils/
│       ├── image_analyzer.py
│       └── db_utils.py
├── tests/
├── output/
│   ├── extracted_workflows/
│   └── generated_agents/
├── requirements.txt
├── README.md
└── system_design.md

##Output Structure 

output/
├── extracted_workflows/
│   ├── EMP-0025_workflows.json
│   ├── EMP-0025_patterns.json
│   └── ...
└── generated_agents/
    ├── P_abc12345/
    │   ├── agent.py
    │   └── config.json
    └── ...

    
## 1. Overview
This system analyzes desktop activity data from SQLite database, extracts workflows from user actions and screenshots, and dynamically generates autonomous agents to execute these workflows.

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

## 3. Data Flow

1. **Input**: SQLite database with events and captures tables
2. **Processing**: Employee-independent workflow extraction
3. **Pattern Discovery**: Group similar workflows, count repetitions
4. **Agent Generation**: Create executable agents for high-value patterns
5. **Output**: Generated Python agents with configuration

## 4. Key Design Decisions

- **Capture-first approach**: Ensures workflows are aligned with visual evidence
- **Employee isolation**: Prevents mixing patterns across different users
- **Dynamic code generation**: Creates self-contained agents per workflow
- **Multi-timeframe analysis**: Identifies patterns with different persistence levels

## 5. Extensibility

The system is designed to be extended with:
- Additional action types
- Computer vision integration for screenshot analysis
- Machine learning for improved pattern matching
- Cloud deployment capabilities
