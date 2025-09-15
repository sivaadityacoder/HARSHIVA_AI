#!/usr/bin/env python3
"""
XBOW-style Autonomous Web Bug Hunter - Main Agent
Orchestrates reconnaissance and vulnerability triage using local LLM
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from llm_client import LLMClient
from tools import run_tool


def ensure_output_dir():
    """Ensure the output directory exists"""
    Path("out").mkdir(exist_ok=True)


def save_tool_output(tool_name: str, output: Dict[str, Any]) -> str:
    """Save tool output to timestamped JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"out/{tool_name}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    return filename


def save_findings(findings: List[Dict], raw_results: List[Dict]):
    """Save triage findings and generate report"""
    # Save structured findings
    with open("out/findings.json", 'w') as f:
        json.dump(findings, f, indent=2)
    
    # Generate markdown report
    report_lines = [
        "# Security Assessment Report",
        f"\nGenerated: {datetime.now().isoformat()}",
        f"\nTotal Findings: {len(findings)}",
        "\n## Executive Summary\n",
    ]
    
    severity_counts = {}
    for finding in findings:
        sev = finding.get('severity', 'unknown')
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    for severity, count in severity_counts.items():
        report_lines.append(f"- {severity.title()}: {count}")
    
    report_lines.extend([
        "\n## Detailed Findings\n",
    ])
    
    for i, finding in enumerate(findings, 1):
        report_lines.extend([
            f"### {i}. {finding.get('title', 'Unknown Issue')}",
            f"\n**Severity**: {finding.get('severity', 'Unknown')}",
            f"\n**Affected URL**: {finding.get('affected_url', 'N/A')}",
            f"\n**Description**: {finding.get('justification', 'No description provided')}",
            f"\n**Exploitability**: {finding.get('exploitability', 'Unknown')}",
            "\n**Proof of Concept Steps**:",
        ])
        
        poc_steps = finding.get('poc_steps', [])
        if isinstance(poc_steps, list):
            for step in poc_steps:
                report_lines.append(f"1. {step}")
        else:
            report_lines.append(f"1. {poc_steps}")
            
        report_lines.extend([
            f"\n**Mitigation**: {finding.get('mitigation', 'No mitigation provided')}",
            "\n---\n",
        ])
    
    with open("out/report.md", 'w') as f:
        f.write('\n'.join(report_lines))


def check_authorization() -> bool:
    """Check if user has explicit authorization for active scanning"""
    print("\n  AUTHORIZATION CHECK ")
    print("This tool performs security testing activities.")
    print("You must have explicit written authorization to test the target(s).")
    print("Unauthorized testing may violate laws and terms of service.")
    
    response = input("\nDo you have explicit authorization to test the specified target(s)? (yes/no): ")
    return response.lower() in ['yes', 'y']


def main():
    parser = argparse.ArgumentParser(description="XBOW-style Autonomous Web Bug Hunter")
    parser.add_argument("targets", nargs="+", help="Target domains to assess")
    parser.add_argument("--passive-only", action="store_true", 
                      help="Only passive reconnaissance (no active scanning)")
    parser.add_argument("--dry-run", action="store_true",
                      help="Show planned tool calls without execution")
    parser.add_argument("--config", default="configs/settings.yaml",
                      help="Configuration file path")
    
    args = parser.parse_args()
    
    # Check for required model path
    model_path = os.getenv("LLM_MODEL_PATH")
    if not model_path:
        print("Error: LLM_MODEL_PATH environment variable not set")
        print("Please download a GGUF model and set LLM_MODEL_PATH")
        sys.exit(1)
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        sys.exit(1)
    
    # Authorization check for non-passive modes
    if not args.passive_only and not args.dry_run:
        if not check_authorization():
            print("Authorization denied. Use --passive-only for passive reconnaissance.")
            sys.exit(1)
    
    ensure_output_dir()
    
    print(f" Initializing XBOW Bug Hunter")
    print(f"📁 Model: {model_path}")
    print(f" Targets: {', '.join(args.targets)}")
    print(f" Mode: {'Passive Only' if args.passive_only else 'Full Scan'}")
    
    try:
        # Initialize LLM client
        llm_client = LLMClient(model_path)
        
        # Plan reconnaissance
        print("\n Planning reconnaissance strategy...")
        plan = llm_client.plan_recon(args.targets, passive_only=args.passive_only)
        
        if not plan or 'tool_calls' not in plan:
            print("Error: Failed to generate reconnaissance plan")
            sys.exit(1)
        
        tool_calls = plan['tool_calls']
        print(f" Planned {len(tool_calls)} tool executions")
        
        if args.dry_run:
            print("\n Dry run mode - showing planned tool calls:")
            for i, call in enumerate(tool_calls, 1):
                print(f"{i}. {call.get('tool', 'unknown')} {' '.join(call.get('args', []))}")
                print(f"   Notes: {call.get('notes', 'N/A')}")
            return
        
        # Execute tool calls
        results = []
        for i, call in enumerate(tool_calls, 1):
            tool_name = call.get('tool', 'unknown')
            tool_args = call.get('args', [])
            notes = call.get('notes', '')
            
            print(f"\n🔧 Executing {i}/{len(tool_calls)}: {tool_name}")
            print(f"📝 Notes: {notes}")
            
            # Execute tool with safety wrapper
            output = run_tool(tool_name, tool_args, passive_only=args.passive_only)
            
            # Save raw output
            output_file = save_tool_output(tool_name, output)
            print(f"💾 Output saved to {output_file}")
            
            # Feed output back to LLM for context
            llm_client.feed_tool_output(call, output)
            
            results.append({
                'tool_call': call,
                'output': output,
                'output_file': output_file
            })
            
            # Small delay between tools
            time.sleep(1)
        
        # Triage results
        print("\n Triaging findings...")
        findings = llm_client.triage(results)
        
        # Save findings and generate report
        save_findings(findings, results)
        
        print(f"\n Assessment complete!")
        print(f" Found {len(findings)} potential issues")
        print(f"📄 Reports saved to out/findings.json and out/report.md")
        
        # Print summary
        if findings:
            print("\n Finding Summary:")
            for finding in findings[:5]:  # Show first 5
                severity = finding.get('severity', 'unknown')
                title = finding.get('title', 'Unknown')
                print(f"  [{severity.upper()}] {title}")
            
            if len(findings) > 5:
                print(f"  ... and {len(findings) - 5} more findings")
        
    except KeyboardInterrupt:
        print("\n  Assessment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Error during assessment: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()