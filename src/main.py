# src/main.py
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.task1_workflow_extractor.data_loader import DataLoader
from src.task1_workflow_extractor.workflow_extractor import WorkflowExtractor
from src.task1_workflow_extractor.pattern_matcher import PatternMatcher
from src.task1_workflow_extractor.repetition_counter import RepetitionCounter
from src.task2_meta_agent.agent_builder import AgentBuilder
from src.task2_meta_agent.workflow_executor import WorkflowExecutor

def main():
    """Main orchestration function"""
    
    # Configuration
    DB_PATH = "test_data.db"
    OUTPUT_DIR = "output"
    
    # Check if database exists
    if not Path(DB_PATH).exists():
        print(f"❌ Database file not found: {DB_PATH}")
        print("Please place the test_data.db file in the project root directory")
        return
    
    # Create output directories
    workflows_dir = Path(OUTPUT_DIR) / "extracted_workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    data_loader = DataLoader(DB_PATH)
    extractor = WorkflowExtractor(min_workflow_length=2, max_pause_seconds=30)
    matcher = PatternMatcher(similarity_threshold=0.8)
    agent_builder = AgentBuilder()
    executor = WorkflowExecutor()
    
    try:
        # Connect to database
        print("Connecting to database...")
        data_loader.connect()
        
        # Get all employees
        employees = data_loader.get_employees()
        print(f"Found employees: {employees}")
        
        if not employees:
            print("No employees found in database")
            return
        
        all_patterns = []
        
        # Process each employee independently
        for employee_id in employees:
            print(f"\n{'='*50}")
            print(f"Processing employee: {employee_id}")
            print('='*50)
            
            # Get date range for employee
            start_date, end_date = data_loader.get_date_range(employee_id)
            print(f"Date range: {start_date} to {end_date}")
            
            # Generate list of dates in range
            date_range = []
            current_date = start_date
            while current_date <= end_date:
                date_range.append(current_date)
                current_date += timedelta(days=1)
            
            # Load captures with events
            print("Loading captures...")
            captures = data_loader.load_captures_with_events(
                employee_id, start_date, end_date
            )
            print(f"Loaded {len(captures)} captures")
            
            if not captures:
                print("No captures found for this employee")
                continue
            
            # Extract workflows
            print("Extracting workflows...")
            workflows = extractor.extract_workflows(captures, employee_id)
            print(f"Extracted {len(workflows)} workflows")
            
            if not workflows:
                print("No workflows found for this employee")
                continue
            
            # Save raw workflows
            workflows_file = workflows_dir / f"{employee_id}_workflows.json"
            with open(workflows_file, 'w') as f:
                json.dump([w.to_dict() for w in workflows], f, indent=2, default=str)
            print(f"Saved workflows to {workflows_file}")
            
            # Group into patterns
            print("Identifying patterns...")
            patterns = matcher.group_into_patterns(workflows)
            print(f"Found {len(patterns)} unique patterns")
            
            # Count repetitions
            counter = RepetitionCounter(date_range)
            patterns = counter.count_repetitions(patterns)
            
            # Filter high-value patterns
            high_value_patterns = counter.filter_high_value_patterns(patterns, min_occurrences=2)
            print(f"Found {len(high_value_patterns)} high-value patterns (occurred at least twice)")
            
            # Save patterns
            patterns_file = workflows_dir / f"{employee_id}_patterns.json"
            with open(patterns_file, 'w') as f:
                json.dump([p.to_dict() for p in patterns], f, indent=2, default=str)
            print(f"Saved patterns to {patterns_file}")
            
            all_patterns.extend(high_value_patterns)
        
        # Task 2: Build agents for high-value patterns
        print(f"\n{'='*50}")
        print("Building Agents for High-Value Patterns")
        print('='*50)
        
        if all_patterns:
            # Build agents
            generated_agents = agent_builder.build_agents(all_patterns)
            print(f"Generated {len(generated_agents)} agents")
            
            # List available agents
            agents = executor.list_agents()
            print("\nAvailable agents:")
            for agent in agents:
                config = agent.get('config', {})
                occurrences = config.get('repetition_stats', {}).get('total_occurrences', 0)
                print(f"  - {agent['pattern_id']}: {occurrences} occurrences")
                
            # Save summary
            summary = {
                'total_patterns': len(all_patterns),
                'total_agents': len(generated_agents),
                'agents': [
                    {
                        'pattern_id': pid,
                        'path': path,
                        'config': agent_builder._generate_config(
                            next(p for p in all_patterns if p.pattern_id == pid)
                        )
                    }
                    for pid, path in generated_agents.items()
                ]
            }
            
            summary_file = Path(OUTPUT_DIR) / "generation_summary.json"
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            print(f"\nSaved generation summary to {summary_file}")
            
        else:
            print("No high-value patterns found for agent generation")
        
        print("\n✅ Processing complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        data_loader.close()

if __name__ == "__main__":
    main()
