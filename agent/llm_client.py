#!/usr/bin/env python3
"""
Local LLM Client using llama-cpp-python
Handles reconnaissance planning and vulnerability triage
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from llama_cpp import Llama
except ImportError:
    print("Error: llama-cpp-python not installed. Run: pip install llama-cpp-python")
    raise


class LLMClient:
    """Local LLM client for security reconnaissance and triage"""
    
    def __init__(self, model_path: str, context_size: int = 4096):
        """
        Initialize LLM client
        
        Args:
            model_path: Path to GGUF/GGML model file
            context_size: Maximum context window size
        """
        self.model_path = model_path
        self.context_size = context_size
        self.conversation_log = []
        
        # Initialize llama-cpp model
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=context_size,
                verbose=False,
                n_threads=4,  # Adjust based on CPU cores
                n_gpu_layers=0,  # Set >0 if using GPU
            )
        except Exception as e:
            raise Exception(f"Failed to load model {model_path}: {e}")
    
    def _load_prompt(self, prompt_name: str) -> str:
        """Load prompt template from file"""
        prompt_path = Path(__file__).parent / "prompts" / f"{prompt_name}.md"
        
        if not prompt_path.exists():
            # Fallback to basic prompt
            return f"You are a cybersecurity expert. {prompt_name.replace('_', ' ').title()}."
        
        try:
            return prompt_path.read_text()
        except Exception:
            return f"You are a cybersecurity expert. {prompt_name.replace('_', ' ').title()}."
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from LLM response with fallback logic
        
        Args:
            text: Raw LLM response text
            
        Returns:
            Parsed JSON dict or None if extraction fails
        """
        # Try to find JSON in code blocks first
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```',
            r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # Try to parse the entire text as JSON
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass
        
        # Last resort: try to extract from lines containing {
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def _generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """
        Generate text using the local LLM
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=0.1,  # Low temperature for consistent output
                top_p=0.9,
                stop=["</response>", "\n\n---"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            print(f"LLM generation error: {e}")
            return ""
    
    def plan_recon(self, targets: List[str], passive_only: bool = True) -> Dict[str, Any]:
        """
        Plan reconnaissance strategy for given targets
        
        Args:
            targets: List of target domains
            passive_only: Whether to restrict to passive reconnaissance
            
        Returns:
            Dict containing tool_calls list
        """
        system_prompt = self._load_prompt("system_prompt")
        recon_prompt = self._load_prompt("recon_prompt")
        
        # Build the full prompt
        target_list = ", ".join(targets)
        mode = "passive-only" if passive_only else "full"
        
        full_prompt = f"""{system_prompt}

{recon_prompt}

TARGETS: {target_list}
MODE: {mode}

Generate a reconnaissance plan as a JSON object with a "tool_calls" array. Each tool_call should have:
- "tool": tool name (subfinder, nuclei, httpx, amass, waybackurls)
- "args": array of command line arguments
- "notes": brief explanation of the step

Respond with ONLY valid JSON."""
        
        # Generate response
        response = self._generate(full_prompt, max_tokens=1024)
        
        # Extract JSON
        parsed = self._extract_json(response)
        
        if parsed and 'tool_calls' in parsed:
            # Validate tool calls
            valid_tools = {'subfinder', 'nuclei', 'httpx', 'amass', 'waybackurls', 'ffuf'}
            validated_calls = []
            
            for call in parsed['tool_calls']:
                if isinstance(call, dict) and 'tool' in call:
                    tool_name = call['tool']
                    if tool_name in valid_tools:
                        # Ensure args is a list
                        if 'args' not in call:
                            call['args'] = []
                        elif not isinstance(call['args'], list):
                            call['args'] = [str(call['args'])]
                        
                        validated_calls.append(call)
            
            return {'tool_calls': validated_calls}
        
        # Fallback plan if JSON extraction fails
        fallback_calls = [
            {
                "tool": "subfinder",
                "args": ["-d", targets[0]] if targets else ["-d", "example.com"],
                "notes": "Enumerate subdomains"
            },
            {
                "tool": "httpx",
                "args": ["-l", "/dev/stdin"] if targets else [targets[0]],
                "notes": "Probe HTTP services"
            }
        ]
        
        if not passive_only:
            fallback_calls.append({
                "tool": "nuclei",
                "args": ["-u", targets[0]] if targets else ["-u", "https://example.com"],
                "notes": "Vulnerability scan"
            })
        
        return {'tool_calls': fallback_calls}
    
    def feed_tool_output(self, tool_call: Dict, output: Dict) -> None:
        """
        Feed tool execution output back to the model for context
        
        Args:
            tool_call: Original tool call dict
            output: Tool execution output
        """
        # Log the tool execution for context in triage
        log_entry = {
            'tool': tool_call.get('tool', 'unknown'),
            'args': tool_call.get('args', []),
            'success': output.get('returncode', 1) == 0,
            'stdout_length': len(output.get('stdout', '')),
            'stderr_length': len(output.get('stderr', '')),
            'has_error': 'error' in output
        }
        
        self.conversation_log.append(log_entry)
    
    def triage(self, results: List[Dict]) -> List[Dict]:
        """
        Triage tool results to identify security findings
        
        Args:
            results: List of tool execution results
            
        Returns:
            List of security findings
        """
        system_prompt = self._load_prompt("system_prompt")
        triage_prompt = self._load_prompt("triage_prompt")
        
        # Prepare results summary for the LLM
        results_summary = []
        for result in results:
            tool_name = result['tool_call'].get('tool', 'unknown')
            output = result['output']
            
            # Truncate large outputs
            stdout = output.get('stdout', '')[:2000]
            stderr = output.get('stderr', '')[:500]
            
            summary = {
                'tool': tool_name,
                'success': output.get('returncode', 1) == 0,
                'stdout_preview': stdout,
                'stderr_preview': stderr,
                'has_error': 'error' in output
            }
            results_summary.append(summary)
        
        # Build triage prompt
        full_prompt = f"""{system_prompt}

{triage_prompt}

TOOL RESULTS:
{json.dumps(results_summary, indent=2)}

Analyze these results and identify security findings. Return ONLY a JSON array of findings, each with:
- id: unique identifier
- title: brief finding title
- affected_url: relevant URL or domain
- severity: critical/high/medium/low/info
- justification: explanation of the issue
- exploitability: assessment of how exploitable this is
- poc_steps: array of proof-of-concept steps
- mitigation: recommended fix

Respond with ONLY valid JSON array."""
        
        # Generate triage response
        response = self._generate(full_prompt, max_tokens=2048)
        
        # Extract JSON array
        parsed = self._extract_json(response)
        
        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict) and 'findings' in parsed:
            return parsed['findings']
        
        # Fallback: return empty findings if parsing fails
        return []