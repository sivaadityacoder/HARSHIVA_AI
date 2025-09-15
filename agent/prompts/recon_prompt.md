# Reconnaissance Planning Prompt

You are tasked with planning a comprehensive but safe reconnaissance strategy for the specified target(s). Your goal is to gather maximum intelligence while maintaining operational security and respecting the target infrastructure.

## Objective
Create a systematic reconnaissance plan that will:
1. Identify the full attack surface of the target(s)
2. Gather technical details about services and technologies
3. Discover potential entry points for further analysis
4. Maintain stealth and avoid detection

## Methodology Requirements

### Passive Reconnaissance (Default Mode)
Focus on techniques that do not directly interact with target systems:
- DNS enumeration and subdomain discovery
- Historical data analysis (Wayback Machine, certificate transparency)
- Open source intelligence gathering
- Public database searches

### Active Reconnaissance (Authorization Required)
Limited active probing when explicitly authorized:
- HTTP service fingerprinting
- Port scanning (limited scope)
- Technology stack identification
- Basic vulnerability scanning

## Tool Selection Strategy

Plan a sequence of **8 or fewer** tool executions in logical order:

1. **Start with subdomain enumeration** to map the attack surface
2. **Probe discovered services** to identify technologies and potential vulnerabilities
3. **Gather historical intelligence** to find forgotten endpoints
4. **Perform targeted vulnerability scanning** based on discovered technologies
5. **Focus on high-value targets** identified in earlier phases

## Output Requirements

Generate a JSON response with exactly this structure:

```json
{
  "tool_calls": [
    {
      "tool": "subfinder",
      "args": ["-d", "target.com", "-all"],
      "notes": "Comprehensive subdomain enumeration using all passive sources"
    },
    {
      "tool": "httpx",
      "args": ["-l", "subdomains.txt", "-title", "-tech-detect", "-status-code"],
      "notes": "Probe discovered subdomains for HTTP services and technologies"
    }
  ]
}
```

## Tool-Specific Guidelines

### subfinder
- Use `-all` flag for comprehensive passive sources
- Consider `-recursive` for deeper enumeration
- Output to files for input to subsequent tools

### httpx  
- Include `-title`, `-tech-detect`, `-status-code` for maximum information gathering
- Use `-follow-redirects` to map redirect chains
- Enable `-screenshot` only if explicitly authorized

### nuclei
- Start with technology detection templates: `-t http/technologies/`
- Use CVE templates for known vulnerabilities: `-t cves/`
- Implement rate limiting: `-rate-limit 10`

### amass
- Use `enum` subcommand with `-passive` flag by default
- Consider `-brute` only for authorized active reconnaissance
- Enable `-dir` for organized output

### waybackurls
- Excellent for discovering forgotten endpoints and parameters
- Filter output for interesting file types and paths
- Combine with other tools for endpoint validation

## Operational Security

- Implement delays between tool executions
- Use randomized user agents when possible
- Respect rate limits and target infrastructure
- Document all techniques for reporting

Remember: Respond with ONLY the JSON object containing your tool_calls array. Each tool_call must include tool name, arguments array, and explanatory notes.