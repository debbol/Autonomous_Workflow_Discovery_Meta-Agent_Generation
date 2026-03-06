# src/task2_meta_agent/workflow_executor.py
from typing import Dict, Any, List
import subprocess
import sys
from pathlib import Path
import json

class WorkflowExecutor:
    def __init__(self, agents_dir: str = "output/generated_agents"):
        self.agents_dir = Path(agents_dir)
        
    def execute_agent(self, pattern_id: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a generated agent"""
        agent_dir = self.agents_dir / pattern_id
        agent_script = agent_dir / "agent.py"
        config_file = agent_dir / "config.json"
        
        if not agent_script.exists():
            return {'success': False, 'error': 'Agent not found'}
            
        try:
            # Run the agent
            cmd = [sys.executable, str(agent_script)]
            if config_file.exists():
                cmd.extend(['--config', str(config_file)])
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Execution timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all generated agents"""
        agents = []
        
        if not self.agents_dir.exists():
            return agents
            
        for agent_dir in self.agents_dir.iterdir():
            if agent_dir.is_dir():
                config_file = agent_dir / "config.json"
                agent_info = {
                    'pattern_id': agent_dir.name,
                    'path': str(agent_dir),
                    'has_config': config_file.exists()
                }
                
                if config_file.exists():
                    with open(config_file, 'r') as f:
                        agent_info['config'] = json.load(f)
                        
                agents.append(agent_info)
                
        return agents
