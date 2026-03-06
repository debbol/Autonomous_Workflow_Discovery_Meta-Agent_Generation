# src/task2_meta_agent/agent_builder.py
from typing import List, Dict, Any
from ..models.workflow_schema import WorkflowPattern, Workflow
from .code_generator import CodeGenerator
import os
import json
from pathlib import Path

class AgentBuilder:
    def __init__(self, output_dir: str = "output/generated_agents"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.code_generator = CodeGenerator()
        
    def build_agents(self, patterns: List[WorkflowPattern]) -> Dict[str, str]:
        """Build agents for each workflow pattern"""
        generated_agents = {}
        
        for pattern in patterns:
            if not pattern.workflows:
                continue
                
            # Use the first workflow as template
            template_workflow = pattern.workflows[0]
            
            # Generate agent code
            agent_code = self.code_generator.generate_agent(
                pattern, 
                template_workflow
            )
            
            # Save agent
            agent_path = self._save_agent(pattern.pattern_id, agent_code)
            generated_agents[pattern.pattern_id] = agent_path
            
            # Generate configuration
            config = self._generate_config(pattern)
            self._save_config(pattern.pattern_id, config)
            
        return generated_agents
    
    def _save_agent(self, pattern_id: str, code: str) -> str:
        """Save agent code to file"""
        agent_dir = self.output_dir / pattern_id
        agent_dir.mkdir(exist_ok=True)
        
        agent_file = agent_dir / "agent.py"
        with open(agent_file, 'w') as f:
            f.write(code)
            
        return str(agent_file)
    
    def _generate_config(self, pattern: WorkflowPattern) -> Dict[str, Any]:
        """Generate configuration for agent"""
        return {
            'pattern_id': pattern.pattern_id,
            'signature': pattern.signature,
            'repetition_stats': pattern.repetition_counts,
            'steps_config': [
                {
                    'action_type': step.action_type.value,
                    'details': step.details,
                    'validation_required': bool(step.screenshot_path)
                }
                for step in pattern.workflows[0].steps
            ] if pattern.workflows else []
        }
    
    def _save_config(self, pattern_id: str, config: Dict[str, Any]):
        """Save configuration to file"""
        config_file = self.output_dir / pattern_id / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2, default=str)
