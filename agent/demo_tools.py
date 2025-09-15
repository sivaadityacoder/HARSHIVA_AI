#!/usr/bin/env python3
"""
Demo Tool Execution - Simulates security tool outputs for testing
"""

import json
import time
import random
from typing import List, Dict, Any


def generate_demo_subfinder_output(domain: str) -> str:
    """Generate realistic subfinder JSON output"""
    subdomains = [
        f"www.{domain}",
        f"mail.{domain}",
        f"api.{domain}",
        f"admin.{domain}",
        f"test.{domain}",
        f"staging.{domain}",
        f"dev.{domain}"
    ]
    
    results = []
    for subdomain in subdomains:
        results.append({
            "host": subdomain,
            "source": ["crtsh", "virustotal"][random.randint(0, 1)]
        })
    
    return "\n".join([json.dumps(result) for result in results])


def generate_demo_httpx_output(url: str) -> str:
    """Generate realistic httpx JSON output"""
    result = {
        "timestamp": "2025-09-13T08:30:00Z",
        "url": url,
        "input": url,
        "title": "Example Domain",
        "scheme": "https",
        "port": 443,
        "status_code": 200,
        "content_length": 1256,
        "technologies": ["Apache", "PHP"],
        "webserver": "Apache/2.4.41",
        "response_time": "145ms"
    }
    return json.dumps(result)


def generate_demo_waybackurls_output(domain: str) -> str:
    """Generate realistic waybackurls output"""
    urls = [
        f"https://{domain}/",
        f"https://{domain}/admin/",
        f"https://{domain}/login.php",
        f"https://{domain}/api/v1/users",
        f"https://{domain}/backup/",
        f"https://{domain}/old/index.html",
        f"https://{domain}/test.php?id=123"
    ]
    return "\n".join(urls)


def generate_demo_nuclei_output(url: str) -> str:
    """Generate realistic nuclei JSONL output"""
    findings = [
        {
            "timestamp": "2025-09-13T08:35:00Z",
            "template": "http/technologies/apache-detect.yaml",
            "template-url": "https://templates.nuclei.sh/public/apache-detect",
            "template-id": "apache-detect",
            "info": {
                "name": "Apache HTTP Server Detection",
                "author": ["geeknik"],
                "tags": ["tech", "apache"],
                "severity": "info"
            },
            "type": "http",
            "host": url,
            "matched-at": url,
            "extracted-results": ["Apache/2.4.41"]
        },
        {
            "timestamp": "2025-09-13T08:35:15Z", 
            "template": "http/misconfiguration/server-status-enabled.yaml",
            "template-url": "https://templates.nuclei.sh/public/server-status-enabled",
            "template-id": "server-status-enabled",
            "info": {
                "name": "Apache Server Status Enabled",
                "author": ["hackergautam"],
                "tags": ["apache", "misconfig"],
                "severity": "low"
            },
            "type": "http",
            "host": url,
            "matched-at": f"{url}/server-status"
        }
    ]
    
    return "\n".join([json.dumps(finding) for finding in findings])


def run_demo_tool(tool_name: str, args: List[str], passive_only: bool = True) -> Dict[str, Any]:
    """
    Demo tool execution that simulates realistic outputs
    """
    print(f"🔧 [DEMO] Executing {tool_name} with args: {' '.join(args)}")
    
    # Simulate execution time
    time.sleep(random.uniform(0.5, 2.0))
    
    # Extract target from args for realistic output
    target = "example.com"
    for i, arg in enumerate(args):
        if arg in ["-d", "-u", "--domain", "--url"] and i + 1 < len(args):
            target = args[i + 1].replace("https://", "").replace("http://", "")
            break
        elif not arg.startswith("-") and "." in arg:
            target = arg.replace("https://", "").replace("http://", "")
    
    # Generate realistic demo outputs
    if tool_name == "subfinder":
        stdout = generate_demo_subfinder_output(target)
        return {
            "command": f"subfinder {' '.join(args)}",
            "stdout": stdout,
            "stderr": "",
            "returncode": 0,
            "timeout": False,
            "error": None
        }
    
    elif tool_name == "httpx":
        url = f"https://{target}" if not target.startswith("http") else target
        stdout = generate_demo_httpx_output(url)
        return {
            "command": f"httpx {' '.join(args)}",
            "stdout": stdout,
            "stderr": "",
            "returncode": 0,
            "timeout": False,
            "error": None
        }
    
    elif tool_name == "waybackurls":
        stdout = generate_demo_waybackurls_output(target)
        return {
            "command": f"waybackurls {' '.join(args)}",
            "stdout": stdout,
            "stderr": "",
            "returncode": 0,
            "timeout": False,
            "error": None
        }
    
    elif tool_name == "nuclei":
        url = f"https://{target}" if not target.startswith("http") else target
        stdout = generate_demo_nuclei_output(url)
        return {
            "command": f"nuclei {' '.join(args)}",
            "stdout": stdout,
            "stderr": "",
            "returncode": 0,
            "timeout": False,
            "error": None
        }
    
    elif tool_name == "amass":
        # Amass typically outputs similar to subfinder
        stdout = generate_demo_subfinder_output(target)
        return {
            "command": f"amass {' '.join(args)}",
            "stdout": stdout,
            "stderr": "",
            "returncode": 0,
            "timeout": False,
            "error": None
        }
    
    elif tool_name == "ffuf":
        if passive_only:
            return {
                "command": f"ffuf {' '.join(args)}",
                "stdout": "",
                "stderr": "ffuf disabled in passive-only mode",
                "returncode": 1,
                "timeout": False,
                "error": "ffuf disabled in passive mode"
            }
        else:
            # Simulate directory discovery results
            results = {
                "results": [
                    {"url": f"https://{target}/admin", "status": 200, "length": 1234},
                    {"url": f"https://{target}/login", "status": 200, "length": 567},
                    {"url": f"https://{target}/backup", "status": 403, "length": 890}
                ]
            }
            return {
                "command": f"ffuf {' '.join(args)}",
                "stdout": json.dumps(results),
                "stderr": "",
                "returncode": 0,
                "timeout": False,
                "error": None
            }
    
    else:
        return {
            "command": f"{tool_name} {' '.join(args)}",
            "stdout": "",
            "stderr": f"Demo mode: {tool_name} not implemented",
            "returncode": 1,
            "timeout": False,
            "error": f"Unknown tool in demo mode: {tool_name}"
        }