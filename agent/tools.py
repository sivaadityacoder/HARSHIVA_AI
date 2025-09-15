#!/usr/bin/env python3
"""
Tool execution wrappers for security reconnaissance
Provides safe, rate-limited execution of external security tools
"""

import json
import subprocess
import time
import shutil
from typing import List, Dict, Any, Optional
from pathlib import Path


# Tool timeout configuration (seconds)
TOOL_TIMEOUTS = {
    'subfinder': 300,
    'nuclei': 600,
    'amass': 900,
    'httpx': 180,
    'ffuf': 300,
    'waybackurls': 120,
    'default': 300
}

# Rate limiting delays (seconds)
RATE_LIMITS = {
    'nuclei': 2,
    'ffuf': 1,
    'default': 0.5
}


def check_tool_available(tool_name: str) -> bool:
    """Check if a tool is available in PATH"""
    return shutil.which(tool_name) is not None


def run_command(cmd: List[str], timeout: int = 300) -> Dict[str, Any]:
    """
    Safely execute a command with timeout and capture output
    
    Args:
        cmd: Command as list of strings
        timeout: Timeout in seconds
        
    Returns:
        Dict with stdout, stderr, returncode, and execution info
    """
    result = {
        'command': ' '.join(cmd),
        'stdout': '',
        'stderr': '',
        'returncode': -1,
        'timeout': False,
        'error': None
    }
    
    try:
        # Execute command with timeout
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        result['stdout'] = proc.stdout
        result['stderr'] = proc.stderr
        result['returncode'] = proc.returncode
        
    except subprocess.TimeoutExpired:
        result['timeout'] = True
        result['error'] = f"Command timed out after {timeout} seconds"
        
    except FileNotFoundError:
        result['error'] = f"Tool '{cmd[0]}' not found in PATH"
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def run_subfinder(args: List[str]) -> Dict[str, Any]:
    """Execute subfinder for subdomain enumeration"""
    if not check_tool_available('subfinder'):
        return {'error': 'subfinder not available', 'stdout': '', 'stderr': '', 'returncode': 1}
    
    # Build safe command
    cmd = ['subfinder'] + args
    
    # Add JSON output flag if not present
    if '-o' not in args and '-oJ' not in args:
        cmd.extend(['-oJ'])
    
    timeout = TOOL_TIMEOUTS.get('subfinder', TOOL_TIMEOUTS['default'])
    return run_command(cmd, timeout)


def run_nuclei(args: List[str], passive_only: bool = True) -> Dict[str, Any]:
    """Execute nuclei for vulnerability scanning"""
    if not check_tool_available('nuclei'):
        return {'error': 'nuclei not available', 'stdout': '', 'stderr': '', 'returncode': 1}
    
    # Build safe command
    cmd = ['nuclei'] + args
    
    # Add passive-only restrictions
    if passive_only:
        # Only use passive templates
        if '-t' not in args:
            cmd.extend(['-t', 'http/technologies/', '-t', 'ssl/'])
        
        # Reduce rate to be respectful
        if '-rate-limit' not in args and '-rl' not in args:
            cmd.extend(['-rl', '10'])
    
    # Add JSON output
    if '-jsonl' not in args and '-json' not in args:
        cmd.append('-jsonl')
    
    timeout = TOOL_TIMEOUTS.get('nuclei', TOOL_TIMEOUTS['default'])
    
    # Apply rate limiting
    time.sleep(RATE_LIMITS.get('nuclei', RATE_LIMITS['default']))
    
    return run_command(cmd, timeout)


def run_amass(args: List[str], passive_only: bool = True) -> Dict[str, Any]:
    """Execute amass for domain reconnaissance"""
    if not check_tool_available('amass'):
        return {'error': 'amass not available', 'stdout': '', 'stderr': '', 'returncode': 1}
    
    # Build safe command
    cmd = ['amass'] + args
    
    # Force passive mode if requested
    if passive_only and 'enum' in args:
        if '-passive' not in args:
            cmd.append('-passive')
    
    timeout = TOOL_TIMEOUTS.get('amass', TOOL_TIMEOUTS['default'])
    return run_command(cmd, timeout)


def run_httpx(args: List[str]) -> Dict[str, Any]:
    """Execute httpx for HTTP probing"""
    if not check_tool_available('httpx'):
        return {'error': 'httpx not available', 'stdout': '', 'stderr': '', 'returncode': 1}
    
    # Build safe command
    cmd = ['httpx'] + args
    
    # Add JSON output and safe options
    if '-json' not in args:
        cmd.append('-json')
    
    # Add rate limiting if not specified
    if '-rate-limit' not in args and '-rl' not in args:
        cmd.extend(['-rl', '20'])
    
    # Add timeout if not specified
    if '-timeout' not in args:
        cmd.extend(['-timeout', '10'])
    
    timeout = TOOL_TIMEOUTS.get('httpx', TOOL_TIMEOUTS['default'])
    return run_command(cmd, timeout)


def run_ffuf(args: List[str], passive_only: bool = True) -> Dict[str, Any]:
    """Execute ffuf for directory/file fuzzing"""
    if not check_tool_available('ffuf'):
        return {'error': 'ffuf not available', 'stdout': '', 'stderr': '', 'returncode': 1}
    
    # Prevent active fuzzing in passive mode
    if passive_only:
        return {
            'error': 'ffuf disabled in passive mode',
            'stdout': '',
            'stderr': 'Active fuzzing not allowed in passive-only mode',
            'returncode': 1
        }
    
    # Build safe command
    cmd = ['ffuf'] + args
    
    # Add JSON output
    if '-of' not in args:
        cmd.extend(['-of', 'json'])
    
    # Add rate limiting
    if '-rate' not in args and '-r' not in args:
        cmd.extend(['-rate', '10'])
    
    timeout = TOOL_TIMEOUTS.get('ffuf', TOOL_TIMEOUTS['default'])
    
    # Apply rate limiting
    time.sleep(RATE_LIMITS.get('ffuf', RATE_LIMITS['default']))
    
    return run_command(cmd, timeout)


def run_waybackurls(args: List[str]) -> Dict[str, Any]:
    """Execute waybackurls for historical URL discovery"""
    if not check_tool_available('waybackurls'):
        return {'error': 'waybackurls not available', 'stdout': '', 'stderr': '', 'returncode': 1}
    
    # Build safe command
    cmd = ['waybackurls'] + args
    
    timeout = TOOL_TIMEOUTS.get('waybackurls', TOOL_TIMEOUTS['default'])
    return run_command(cmd, timeout)


def run_tool(tool_name: str, args: List[str], passive_only: bool = True) -> Dict[str, Any]:
    """
    Main entry point for tool execution
    
    Args:
        tool_name: Name of the tool to execute
        args: Arguments to pass to the tool
        passive_only: Whether to restrict to passive-only operations
        
    Returns:
        Dict containing execution results
    """
    
    # Map tool names to execution functions
    tool_functions = {
        'subfinder': run_subfinder,
        'nuclei': lambda args: run_nuclei(args, passive_only),
        'amass': lambda args: run_amass(args, passive_only),
        'httpx': run_httpx,
        'ffuf': lambda args: run_ffuf(args, passive_only),
        'waybackurls': run_waybackurls,
    }
    
    if tool_name not in tool_functions:
        return {
            'error': f'Unknown tool: {tool_name}',
            'stdout': '',
            'stderr': f'Tool {tool_name} not supported',
            'returncode': 1
        }
    
    try:
        return tool_functions[tool_name](args)
    except Exception as e:
        return {
            'error': f'Tool execution failed: {str(e)}',
            'stdout': '',
            'stderr': str(e),
            'returncode': 1
        }