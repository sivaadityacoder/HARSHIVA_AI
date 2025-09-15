#!/usr/bin/env python3
"""
Unit tests for XBOW Web Hunter tools module
"""

import pytest
from unittest.mock import patch, MagicMock
import subprocess

# Import the module to test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent'))

from tools import run_command, run_tool, check_tool_available


class TestRunCommand:
    """Test the run_command function"""
    
    @patch('subprocess.run')
    def test_successful_command(self, mock_run):
        """Test successful command execution"""
        # Mock successful subprocess.run
        mock_result = MagicMock()
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        # Execute command
        result = run_command(['echo', 'test'], timeout=30)
        
        # Verify results
        assert result['stdout'] == "test output"
        assert result['stderr'] == ""
        assert result['returncode'] == 0
        assert result['timeout'] is False
        assert result['error'] is None
        assert 'echo test' in result['command']
    
    @patch('subprocess.run')
    def test_command_timeout(self, mock_run):
        """Test command timeout handling"""
        # Mock timeout exception
        mock_run.side_effect = subprocess.TimeoutExpired(['sleep', '10'], 5)
        
        # Execute command
        result = run_command(['sleep', '10'], timeout=5)
        
        # Verify timeout handling
        assert result['timeout'] is True
        assert 'timed out after 5 seconds' in result['error']
        assert result['returncode'] == -1
    
    @patch('subprocess.run')
    def test_command_not_found(self, mock_run):
        """Test handling of command not found"""
        # Mock FileNotFoundError
        mock_run.side_effect = FileNotFoundError("command not found")
        
        # Execute command
        result = run_command(['nonexistent_tool'], timeout=30)
        
        # Verify error handling
        assert 'not found in PATH' in result['error']
        assert result['returncode'] == -1
    
    @patch('subprocess.run')
    def test_generic_exception(self, mock_run):
        """Test handling of generic exceptions"""
        # Mock generic exception
        mock_run.side_effect = Exception("generic error")
        
        # Execute command
        result = run_command(['test'], timeout=30)
        
        # Verify error handling
        assert result['error'] == "generic error"
        assert result['returncode'] == -1


class TestCheckToolAvailable:
    """Test the check_tool_available function"""
    
    @patch('shutil.which')
    def test_tool_available(self, mock_which):
        """Test when tool is available"""
        mock_which.return_value = "/usr/bin/test_tool"
        
        result = check_tool_available('test_tool')
        
        assert result is True
        mock_which.assert_called_once_with('test_tool')
    
    @patch('shutil.which')
    def test_tool_not_available(self, mock_which):
        """Test when tool is not available"""
        mock_which.return_value = None
        
        result = check_tool_available('nonexistent_tool')
        
        assert result is False
        mock_which.assert_called_once_with('nonexistent_tool')


class TestRunTool:
    """Test the run_tool function"""
    
    @patch('tools.run_subfinder')
    def test_run_subfinder(self, mock_subfinder):
        """Test running subfinder tool"""
        # Mock subfinder function
        mock_subfinder.return_value = {
            'stdout': 'subdomain1.example.com\nsubdomain2.example.com',
            'stderr': '',
            'returncode': 0
        }
        
        # Execute tool
        result = run_tool('subfinder', ['-d', 'example.com'])
        
        # Verify execution
        mock_subfinder.assert_called_once_with(['-d', 'example.com'])
        assert result['returncode'] == 0
        assert 'subdomain1.example.com' in result['stdout']
    
    @patch('tools.run_nuclei')
    def test_run_nuclei_passive(self, mock_nuclei):
        """Test running nuclei in passive mode"""
        # Mock nuclei function
        mock_nuclei.return_value = {
            'stdout': '{"template": "tech-detect", "info": {"name": "Apache"}}',
            'stderr': '',
            'returncode': 0
        }
        
        # Execute tool in passive mode
        result = run_tool('nuclei', ['-u', 'https://example.com'], passive_only=True)
        
        # Verify passive mode is passed
        mock_nuclei.assert_called_once_with(['-u', 'https://example.com'], True)
        assert result['returncode'] == 0
    
    def test_unknown_tool(self):
        """Test handling of unknown tool"""
        result = run_tool('unknown_tool', ['arg1', 'arg2'])
        
        assert 'Unknown tool: unknown_tool' in result['error']
        assert result['returncode'] == 1
    
    @patch('tools.run_ffuf')
    def test_ffuf_passive_only_blocked(self, mock_ffuf):
        """Test that ffuf is blocked in passive-only mode"""
        # Mock ffuf to return blocked message
        mock_ffuf.return_value = {
            'error': 'ffuf disabled in passive mode',
            'stderr': 'Active fuzzing not allowed in passive-only mode',
            'returncode': 1
        }
        
        # Execute ffuf in passive mode
        result = run_tool('ffuf', ['-u', 'https://example.com/FUZZ'], passive_only=True)
        
        # Verify ffuf is blocked
        assert 'disabled in passive mode' in result['error']
        assert result['returncode'] == 1


class TestToolSpecificFunctions:
    """Test individual tool wrapper functions"""
    
    @patch('tools.check_tool_available')
    @patch('tools.run_command')
    def test_run_subfinder_with_json_output(self, mock_run_command, mock_check_tool):
        """Test subfinder with automatic JSON output"""
        # Mock tool availability and command execution
        mock_check_tool.return_value = True
        mock_run_command.return_value = {
            'stdout': 'test.example.com',
            'stderr': '',
            'returncode': 0
        }
        
        # Import and test subfinder function
        from tools import run_subfinder
        result = run_subfinder(['-d', 'example.com'])
        
        # Verify JSON output flag was added
        mock_run_command.assert_called_once()
        call_args = mock_run_command.call_args[0][0]  # First positional argument
        assert 'subfinder' in call_args
        assert '-d' in call_args
        assert 'example.com' in call_args
        assert '-oJ' in call_args  # JSON output flag should be added
    
    @patch('tools.check_tool_available')
    def test_tool_not_available_error(self, mock_check_tool):
        """Test error when tool is not available"""
        # Mock tool not available
        mock_check_tool.return_value = False
        
        # Import and test a tool function
        from tools import run_httpx
        result = run_httpx(['-u', 'https://example.com'])
        
        # Verify error handling
        assert 'not available' in result['error']
        assert result['returncode'] == 1


# Test fixtures and helper functions
@pytest.fixture
def mock_subprocess_success():
    """Fixture for successful subprocess execution"""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "success output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        yield mock_run


def test_run_command_returns_dict_structure(mock_subprocess_success):
    """Test that run_command always returns expected dict structure"""
    result = run_command(['echo', 'test'])
    
    # Verify all required keys are present
    required_keys = ['command', 'stdout', 'stderr', 'returncode', 'timeout', 'error']
    for key in required_keys:
        assert key in result
    
    # Verify data types
    assert isinstance(result['command'], str)
    assert isinstance(result['stdout'], str)
    assert isinstance(result['stderr'], str)
    assert isinstance(result['returncode'], int)
    assert isinstance(result['timeout'], bool)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])