#!/usr/bin/env python3
"""
Demo LLM Client - Simulates local LLM responses for testing
"""

import json
import time
from typing import List, Dict, Any


class DemoLLMClient:
    """Demo LLM client that simulates responses for testing purposes"""
    
    def __init__(self, model_path: str = "demo", context_size: int = 4096):
        """Initialize demo client"""
        self.model_path = model_path
        self.context_size = context_size
        self.conversation_log = []
        print(f"🤖 Demo LLM Client initialized (simulating model: {model_path})")
    
    def plan_recon(self, targets: List[str], passive_only: bool = True) -> Dict[str, Any]:
        """Generate demo reconnaissance plan"""
        print(f" Planning reconnaissance for targets: {', '.join(targets)}")
        print(f" Mode: {'Passive-only' if passive_only else 'Full'}")
        
        # Simulate thinking time
        time.sleep(1)
        
        # Generate demo plan based on targets
        target = targets[0] if targets else "example.com"
        
        demo_plan = {
            "tool_calls": [
                {
                    "tool": "subfinder",
                    "args": ["-d", target, "-all"],
                    "notes": f"Enumerate subdomains for {target} using passive DNS sources"
                },
                {
                    "tool": "httpx",
                    "args": ["-u", f"https://{target}", "-title", "-tech-detect", "-status-code"],
                    "notes": f"Probe main domain {target} for HTTP service information"
                },
                {
                    "tool": "waybackurls", 
                    "args": [target],
                    "notes": f"Discover historical URLs for {target} from Wayback Machine"
                }
            ]
        }
        
        if not passive_only:
            demo_plan["tool_calls"].extend([
                {
                    "tool": "nuclei",
                    "args": ["-u", f"https://{target}", "-t", "http/technologies/", "-rate-limit", "10"],
                    "notes": f"Scan {target} for known vulnerabilities and misconfigurations"
                },
                {
                    "tool": "ffuf",
                    "args": ["-u", f"https://{target}/FUZZ", "-w", "/usr/share/wordlists/common.txt", "-rate", "5"],
                    "notes": f"Directory and file discovery on {target}"
                }
            ])
        
        print(f" Generated plan with {len(demo_plan['tool_calls'])} steps")
        return demo_plan
    
    def feed_tool_output(self, tool_call: Dict, output: Dict) -> None:
        """Log tool execution for context"""
        tool_name = tool_call.get('tool', 'unknown')
        success = output.get('returncode', 1) == 0
        
        log_entry = {
            'tool': tool_name,
            'success': success,
            'stdout_length': len(output.get('stdout', '')),
            'stderr_length': len(output.get('stderr', '')),
            'has_error': 'error' in output
        }
        
        self.conversation_log.append(log_entry)
        print(f"📝 Logged {tool_name} execution: {' Success' if success else ' Failed'}")
    
    def triage(self, results: List[Dict]) -> List[Dict]:
        """Generate demo vulnerability findings"""
        print(" Analyzing tool outputs for security findings...")
        
        # Simulate analysis time
        time.sleep(2)
        
        # Generate demo findings based on tool results
        demo_findings = []
        
        for i, result in enumerate(results):
            tool_name = result['tool_call'].get('tool', 'unknown')
            output = result['output']
            
            if tool_name == "httpx" and output.get('returncode') == 0:
                demo_findings.append({
                    "id": f"finding-{i+1:03d}",
                    "title": "HTTP Service Information Disclosure",
                    "affected_url": "https://example.com",
                    "severity": "info",
                    "justification": "HTTP response headers reveal server technology and version information that could aid attackers in reconnaissance.",
                    "exploitability": "Low - Information disclosure only, but useful for targeted attacks",
                    "poc_steps": [
                        "Send HTTP request to target URL",
                        "Examine response headers for Server, X-Powered-By, etc.",
                        "Note technology stack information disclosed"
                    ],
                    "mitigation": "Configure web server to suppress or obfuscate version information in HTTP headers"
                })
            
            elif tool_name == "subfinder" and output.get('returncode') == 0:
                demo_findings.append({
                    "id": f"finding-{i+2:03d}",
                    "title": "Subdomain Enumeration Successful",
                    "affected_url": "*.example.com",
                    "severity": "info", 
                    "justification": "Multiple subdomains discovered through passive DNS enumeration, expanding attack surface.",
                    "exploitability": "Low - Reconnaissance finding that enables further testing",
                    "poc_steps": [
                        "Run subfinder against target domain",
                        "Analyze discovered subdomains for interesting services",
                        "Prioritize subdomains for further testing"
                    ],
                    "mitigation": "Review subdomain exposure and disable unnecessary services"
                })
            
            elif tool_name == "nuclei" and not output.get('error'):
                demo_findings.append({
                    "id": f"finding-{i+3:03d}",
                    "title": "Potential Security Misconfiguration",
                    "affected_url": "https://example.com",
                    "severity": "medium",
                    "justification": "Nuclei scan detected potential security misconfigurations that could be exploited.",
                    "exploitability": "Medium - Depends on specific misconfiguration found",
                    "poc_steps": [
                        "Run nuclei with technology detection templates",
                        "Review identified misconfigurations",
                        "Assess impact and exploitability"
                    ],
                    "mitigation": "Review and harden server configuration based on findings"
                })
        
        # Add a default finding if no tools succeeded
        if not demo_findings:
            demo_findings.append({
                "id": "finding-001",
                "title": "Limited Reconnaissance Data",
                "affected_url": "example.com",
                "severity": "info",
                "justification": "Reconnaissance tools were unable to gather significant information, possibly due to security controls or tool availability.",
                "exploitability": "N/A - No exploitable issues identified",
                "poc_steps": [
                    "Verify tool availability and configuration",
                    "Check network connectivity to target",
                    "Consider alternative reconnaissance approaches"
                ],
                "mitigation": "Continue monitoring and testing with additional tools"
            })
        
        print(f" Identified {len(demo_findings)} security findings")
        return demo_findings