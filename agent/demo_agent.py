#!/usr/bin/env python3
"""
XBOW-style Autonomous Web Bug Hunter - Demo Version
Demonstrates functionality without requiring real LLM models or security tools
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Import demo versions for testing
from demo_llm_client import DemoLLMClient
from demo_tools import run_demo_tool


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
        "# Security Assessment Report - DEMO",
        f"\nGenerated: {datetime.now().isoformat()}",
        f"\nTotal Findings: {len(findings)}",
        "\n## Executive Summary\n",
        "**Note**: This is a DEMO run with simulated outputs.",
        "",
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
    parser = argparse.ArgumentParser(description="XBOW-style Autonomous Web Bug Hunter - DEMO")
    parser.add_argument("targets", nargs="+", help="Target domains to assess")
    parser.add_argument("--passive-only", action="store_true", 
                      help="Only passive reconnaissance (no active scanning)")
    parser.add_argument("--dry-run", action="store_true",
                      help="Show planned tool calls without execution")
    parser.add_argument("--demo", action="store_true",
                      help="Run in demo mode with simulated outputs")
    parser.add_argument("--config", default="configs/settings.yaml",
                      help="Configuration file path")
    
    args = parser.parse_args()
    
    # Enable demo mode automatically if no LLM model available
    if not os.getenv("LLM_MODEL_PATH") or args.demo:
        args.demo = True
        print("🎭 Running in DEMO mode with simulated outputs")
    
    # Authorization check for non-passive modes
    if not args.passive_only and not args.dry_run and not args.demo:
        if not check_authorization():
            print("Authorization denied. Use --passive-only for passive reconnaissance.")
            sys.exit(1)
    
    ensure_output_dir()
    
    print(f" Initializing XBOW Bug Hunter {'[DEMO MODE]' if args.demo else ''}")
    if args.demo:
        print(f"🤖 Using simulated LLM and tool outputs")
    print(f" Targets: {', '.join(args.targets)}")
    print(f" Mode: {'Passive Only' if args.passive_only else 'Full Scan'}")
    
    try:
        # Initialize LLM client (demo or real)
        if args.demo:
            llm_client = DemoLLMClient("demo-model")
        else:
            from llm_client import LLMClient
            model_path = os.getenv("LLM_MODEL_PATH")
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
            args_list = call.get('args', [])
            notes = call.get('notes', '')
            
            print(f"\n🔧 Executing {i}/{len(tool_calls)}: {tool_name}")
            print(f"📝 Notes: {notes}")
            
            # Execute tool with safety wrapper (demo or real)
            if args.demo:
                output = run_demo_tool(tool_name, args_list, passive_only=args.passive_only)
            else:
                from tools import run_tool
                output = run_tool(tool_name, args_list, passive_only=args.passive_only)
            
            # Save raw output
            output_file = save_tool_output(tool_name, output)
            print(f"💾 Output saved to {output_file}")
            
            # Show preview of output
            if output.get('stdout'):
                preview = output['stdout'][:200]
                print(f"📄 Preview: {preview}{'...' if len(output['stdout']) > 200 else ''}")
            
            if output.get('error'):
                print(f"  Error: {output['error']}")
            
            # Feed output back to LLM for context
            llm_client.feed_tool_output(call, output)
            
            results.append({
                'tool_call': call,
                'output': output,
                'output_file': output_file
            })
            
            # Small delay between tools
            time.sleep(0.5)
        
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
        
        if args.demo:
            print("\n🎭 DEMO MODE: All outputs were simulated for demonstration purposes.")
            print("    For real assessments, install security tools and download an LLM model.")
        
    except KeyboardInterrupt:
        print("\n  Assessment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n Error during assessment: {e}")
        if args.demo:
            print("This error occurred in demo mode - check your Python environment")
        sys.exit(1)


if __name__ == "__main__":
    main()