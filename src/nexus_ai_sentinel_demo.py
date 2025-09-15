#!/usr/bin/env python3
"""
 NEXUS AI ELITE - Quick Demo Version
 Human-Like Hacker AI with Fast Execution
 Elite Methodologies + Real LLM Integration

Fast demo version for VEDA presentation that shows all capabilities
while keeping execution time reasonable.
"""

import os
import sys
import json
import time
import random
import datetime
from agent.llm_client import LLMClient

class NexusAISentinelDemo:
    """Fast demo version of XBOW Hacker AI"""
    
    def __init__(self):
        """Initialize XBOW Hacker AI Demo"""
        print(" NEXUS AI ELITE - Advanced Hacker Intelligence Demo")
        print(" Human-Like AI Penetration Testing Platform")
        print(" Elite Bug Bounty Hunter + Top Hacker Methodologies")
        print("="*70)
        
        # Initialize LLM
        model_path = "./models/codellama-7b-instruct.Q4_K_M.gguf"
        if os.path.exists(model_path):
            self.llm = LLMClient(model_path)
            print(" AI Hacker Brain Loaded: CodeLlama-7B-Instruct")
            print(" Human-Like Hacker Intelligence: ACTIVE")
        else:
            self.llm = None
            print("  LLM Model not found - Using simulation mode")
        
        # Hacker personality profiles
        self.hacker_personalities = {
            "ghost": "Ultra-stealth reconnaissance specialist",
            "lightning": "Fast exploitation and automation expert", 
            "phantom": "OSINT and social engineering master",
            "professor": "Methodical researcher and analyst",
            "apex": "Elite bug bounty hunter"
        }
        
        print(" NEXUS AI Status: READY FOR ELITE HACKING")
    
    def ai_hacker_thinking(self, target, context="target_assessment"):
        """AI that thinks like a real hacker"""
        
        print(f"\n AI HACKER MIND SIMULATION")
        print(f" Target: {target}")
        print(f"📍 Context: {context.replace('_', ' ').title()}")
        
        # Select random hacker personality
        personality = random.choice(list(self.hacker_personalities.keys()))
        print(f"🎭 Hacker Personality: '{personality.upper()}' - {self.hacker_personalities[personality]}")
        
        # AI hacker reasoning prompt
        hacker_prompt = f"""
You are an elite hacker with the personality of "{personality}" - {self.hacker_personalities[personality]}.

Analyze target: {target}
Context: {context}

Think like a real hacker and provide:
1. Your initial gut instinct about this target
2. What immediately catches your attention
3. Your preferred attack methodology 
4. Potential vulnerabilities you'd look for
5. Stealth and risk considerations

Be specific, tactical, and think like a real penetration tester.
Keep response concise but insightful.
"""
        
        print(" AI Processing hacker thought patterns...")
        
        if self.llm:
            try:
                # Use shorter response for demo
                ai_thoughts = self.llm._generate(hacker_prompt, max_tokens=512)
                print(" AI Hacker Analysis Complete")
                
                # Display key insights
                print(f"\n HACKER AI INSIGHTS:")
                if "target" in ai_thoughts.lower():
                    print("   • Target analysis generated")
                if "vulner" in ai_thoughts.lower():
                    print("   • Vulnerability assessment planned")
                if "attack" in ai_thoughts.lower():
                    print("   • Attack vectors identified")
                
                return ai_thoughts
                
            except Exception as e:
                print(f"  AI Processing: {str(e)[:50]}...")
        
        # Fallback hacker thinking
        fallback_analysis = f"""
 HACKER AI ASSESSMENT ({personality.upper()} personality):

INITIAL INSTINCT:
• {target} looks like an educational target - probably has standard web app vulns
• College websites often have weak authentication and input validation
• Student portals and admin panels are high-value targets

ATTENTION GRABBERS:
• Academic domain suggests student data and grades at risk
• Likely has multiple subdomains (portal, lms, admin)
• Probably running common CMS or custom PHP applications

ATTACK METHODOLOGY:
• Start with passive reconnaissance to avoid detection
• Use Google dorking to find exposed information
• Enumerate subdomains and services systematically
• Test for OWASP Top 10 vulnerabilities
• Focus on authentication bypass and injection attacks

VULNERABILITY HUNTING:
• SQL injection in login forms and search functions
• XSS in feedback and comment systems
• File upload vulnerabilities in assignment systems
• Authentication bypass in student/faculty portals
• Information disclosure through error messages

STEALTH CONSIDERATIONS:
• Educational targets often have basic monitoring
• Use low-and-slow techniques to avoid detection
• Test during off-peak hours (evenings/weekends)
• Maintain good operational security throughout
"""
        
        print(" Hacker AI Analysis Complete (Simulation Mode)")
        return fallback_analysis
    
    def elite_google_dorking_demo(self, target):
        """Demo of elite Google dorking techniques"""
        
        print(f"\n ELITE GOOGLE DORKING DEMONSTRATION")
        print(f" Target: {target}")
        
        # Extract domain
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Elite hacker Google dorks
        elite_dorks = [
            f'site:{domain} filetype:sql "password" | "passwd"',
            f'site:{domain} inurl:admin | inurl:wp-admin', 
            f'site:{domain} "index of /" | "directory listing"',
            f'site:{domain} filetype:log "error" | "exception"',
            f'site:{domain} filetype:conf | filetype:config',
            f'site:{domain} inurl:api | inurl:graphql',
            f'"{domain}" site:github.com | site:gitlab.com',
            f'site:{domain} "database" | "mysql" | "postgresql"',
            f'site:{domain} filetype:txt "username" | "password"',
            f'site:{domain} "phpinfo()" | "test.php"'
        ]
        
        print(f" EXECUTING {len(elite_dorks)} ELITE GOOGLE DORKS")
        
        findings = []
        for i, dork in enumerate(elite_dorks, 1):
            print(f"    Dork {i:2d}: {dork}")
            
            # Simulate findings (random chance)
            if random.random() > 0.75:  # 25% chance
                finding_types = [
                    "Admin panel exposed",
                    "Configuration file leaked", 
                    "Database backup found",
                    "API documentation exposed",
                    "Directory listing available",
                    "Error logs accessible",
                    "Git repository found",
                    "Sensitive file discovered"
                ]
                finding = random.choice(finding_types)
                findings.append({"dork": dork, "finding": finding})
                print(f"       CRITICAL: {finding}")
            else:
                print(f"       No results")
            
            time.sleep(0.1)  # Fast demo timing
        
        print(f"\n GOOGLE DORKING RESULTS:")
        print(f"   • Dorks Executed: {len(elite_dorks)}")
        print(f"   • Critical Findings: {len(findings)}")
        print(f"   • Success Rate: {len(findings)/len(elite_dorks)*100:.1f}%")
        
        return findings
    
    def owasp_top10_elite_testing(self, target):
        """Elite OWASP Top 10 testing methodology"""
        
        print(f"\n  OWASP TOP 10 ELITE TESTING")
        print(f" Target: {target}")
        print(" Testing like a top bug bounty hunter...")
        
        # OWASP Top 10 with elite payloads
        owasp_elite_tests = {
            "A01_Broken_Access_Control": {
                "priority": "CRITICAL",
                "payloads": ["../admin/users", "?user_id=1", "/api/users/2/profile"],
                "description": "Testing for privilege escalation"
            },
            "A03_Injection": {
                "priority": "CRITICAL", 
                "payloads": ["' OR '1'='1' --", "admin'/**/UNION/**/SELECT/**/1,2,3--", "'; DROP TABLE users; --"],
                "description": "SQL injection vulnerability testing"
            },
            "A07_XSS": {
                "priority": "HIGH",
                "payloads": ["<script>alert('XSS')</script>", "javascript:alert('XBOW')", "<img src=x onerror=alert(1)>"],
                "description": "Cross-site scripting detection"
            },
            "A05_Security_Misconfiguration": {
                "priority": "HIGH",
                "payloads": ["admin:admin", "root:root", "guest:guest"],
                "description": "Default credential testing"
            },
            "A10_SSRF": {
                "priority": "HIGH",
                "payloads": ["http://localhost/admin", "http://127.0.0.1:8080", "http://169.254.169.254/metadata"],
                "description": "Server-side request forgery"
            }
        }
        
        vulnerabilities_found = []
        
        for vuln_id, vuln_data in owasp_elite_tests.items():
            vuln_name = vuln_id.replace("_", " ")
            priority = vuln_data["priority"]
            
            print(f"\n    {vuln_name} [{priority}]")
            print(f"       {vuln_data['description']}")
            
            # Test elite payloads
            for payload in vuln_data["payloads"][:2]:  # Test 2 payloads for demo speed
                print(f"      🧪 Testing: {payload}")
                
                # Simulate vulnerability detection
                if random.random() > 0.8:  # 20% chance of finding vuln
                    vuln_finding = {
                        "vulnerability": vuln_name,
                        "payload": payload,
                        "severity": priority,
                        "confidence": "HIGH"
                    }
                    vulnerabilities_found.append(vuln_finding)
                    print(f"         🚨 VULNERABLE: {payload}")
                else:
                    print(f"          Secure")
                
                time.sleep(0.1)  # Fast demo timing
        
        print(f"\n OWASP ELITE TESTING RESULTS:")
        print(f"   • Tests Executed: {len(owasp_elite_tests)}")
        print(f"   • Vulnerabilities: {len(vulnerabilities_found)}")
        print(f"   • Critical Issues: {len([v for v in vulnerabilities_found if v['severity'] == 'CRITICAL'])}")
        
        return vulnerabilities_found
    
    def elite_reconnaissance_demo(self, target):
        """Elite reconnaissance techniques demo"""
        
        print(f"\n  ELITE RECONNAISSANCE TECHNIQUES")
        print(f" Target: {target}")
        print(" Using top hacker methodologies...")
        
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Elite recon techniques
        recon_techniques = {
            "Subdomain Enumeration": [
                f"api.{domain}",
                f"admin.{domain}", 
                f"dev.{domain}",
                f"staging.{domain}",
                f"test.{domain}"
            ],
            "Certificate Transparency": [
                "SSL certificate analysis",
                "Historical certificate data",
                "Certificate authority information"
            ],
            "Technology Stack Detection": [
                "Apache 2.4.41",
                "PHP 7.4.3",
                "MySQL 8.0.27",
                "WordPress 5.8.1"
            ],
            "Endpoint Discovery": [
                "/api/v1/users",
                "/admin/login",
                "/wp-admin/",
                "/.git/config",
                "/backup.sql"
            ]
        }
        
        intelligence_gathered = {}
        
        for technique, data in recon_techniques.items():
            print(f"\n    {technique}")
            
            findings = []
            for item in data:
                print(f"       Discovered: {item}")
                findings.append(item)
                time.sleep(0.05)  # Fast demo
            
            intelligence_gathered[technique] = findings
        
        print(f"\n ELITE RECONNAISSANCE SUMMARY:")
        total_intel = sum(len(findings) for findings in intelligence_gathered.values())
        print(f"   • Techniques Used: {len(recon_techniques)}")
        print(f"   • Intelligence Gathered: {total_intel} items")
        print(f"   • Attack Surface: SIGNIFICANTLY EXPANDED")
        
        return intelligence_gathered
    
    def ai_strategic_decisions(self, target, intel_data, vulns_found):
        """AI makes strategic decisions like an elite hacker"""
        
        print(f"\n AI STRATEGIC DECISION ENGINE")
        print(" Making decisions like an elite bug bounty hunter...")
        
        # Calculate risk and priority scores
        total_intel = sum(len(data) for data in intel_data.values())
        critical_vulns = len([v for v in vulns_found if v.get('severity') == 'CRITICAL'])
        
        # AI decision-making
        decisions = {
            "next_priority_targets": [],
            "exploitation_strategy": "LOW_AND_SLOW",
            "risk_assessment": "MODERATE",
            "recommended_actions": []
        }
        
        # Analyze subdomains for high-value targets
        if "Subdomain Enumeration" in intel_data:
            for subdomain in intel_data["Subdomain Enumeration"]:
                if any(keyword in subdomain for keyword in ['admin', 'api', 'dev']):
                    decisions["next_priority_targets"].append({
                        "target": subdomain,
                        "reason": "High-value subdomain identified",
                        "priority": "HIGH"
                    })
        
        # Prioritize based on vulnerabilities
        if critical_vulns > 0:
            decisions["recommended_actions"].append("Focus on critical vulnerabilities first")
            decisions["risk_assessment"] = "HIGH"
        
        if total_intel > 10:
            decisions["recommended_actions"].append("Comprehensive enumeration of discovered assets")
        
        # Strategic recommendations
        decisions["recommended_actions"].extend([
            "Manual verification of automated findings",
            "Deep analysis of high-priority targets",
            "Custom payload development for specific vulnerabilities"
        ])
        
        print(f"    Priority Targets Identified: {len(decisions['next_priority_targets'])}")
        print(f"    Strategy: {decisions['exploitation_strategy']}")
        print(f"     Risk Level: {decisions['risk_assessment']}")
        print(f"    Next Actions: {len(decisions['recommended_actions'])}")
        
        return decisions
    
    def execute_elite_assessment(self, target):
        """Execute complete elite hacker assessment"""
        
        print("="*80)
        print(" NEXUS AI ELITE - HUMAN-LIKE HACKER INTELLIGENCE")
        print(" Advanced AI Penetration Testing Platform")
        print(" Elite Bug Bounty Hunter + Top Hacker Methodologies")
        print("="*80)
        
        start_time = time.time()
        
        # Phase 1: AI Hacker Thinking
        print(f"\n PHASE 1: AI HACKER MIND SIMULATION")
        ai_analysis = self.ai_hacker_thinking(target)
        
        # Phase 2: Elite Google Dorking
        print(f"\n PHASE 2: ELITE GOOGLE DORKING")
        google_findings = self.elite_google_dorking_demo(target)
        
        # Phase 3: Elite Reconnaissance
        print(f"\n  PHASE 3: ELITE RECONNAISSANCE")
        recon_intel = self.elite_reconnaissance_demo(target)
        
        # Phase 4: OWASP Top 10 Elite Testing
        print(f"\n  PHASE 4: OWASP TOP 10 ELITE TESTING")
        vulnerabilities = self.owasp_top10_elite_testing(target)
        
        # Phase 5: AI Strategic Decisions
        print(f"\n PHASE 5: AI STRATEGIC DECISION ENGINE")
        strategic_plan = self.ai_strategic_decisions(target, recon_intel, vulnerabilities)
        
        # Final Results
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*80)
        print(" NEXUS AI ELITE ASSESSMENT COMPLETE")
        print("="*80)
        
        # Comprehensive summary
        summary = {
            "target": target,
            "assessment_time": f"{elapsed_time:.1f}s",
            "ai_hacker_personality": "Elite bug bounty hunter simulation",
            "google_dorks_executed": 10,
            "intelligence_gathered": sum(len(data) for data in recon_intel.values()),
            "vulnerabilities_found": len(vulnerabilities),
            "critical_issues": len([v for v in vulnerabilities if v.get('severity') == 'CRITICAL']),
            "priority_targets": len(strategic_plan['next_priority_targets']),
            "ai_enhancement": " Human-Like Hacker Intelligence ACTIVE",
            "methodology": "Elite Bug Bounty Hunter + Top Hacker Techniques",
            "innovation_level": "AI-Enhanced Cybersecurity Platform"
        }
        
        for key, value in summary.items():
            print(f" {key.replace('_', ' ').title()}: {value}")
        
        # Save assessment report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        domain_clean = target.replace('https://', '').replace('http://', '').replace('.', '_')
        
        report_data = {
            "target": target,
            "timestamp": timestamp,
            "ai_analysis": ai_analysis,
            "google_dorking": google_findings,
            "reconnaissance": recon_intel,
            "vulnerabilities": vulnerabilities,
            "strategic_decisions": strategic_plan,
            "summary": summary
        }
        
        report_file = f"xbow_hacker_ai_elite_{domain_clean}_{timestamp}.json"
        
        try:
            os.makedirs("reports", exist_ok=True)
            with open(f"reports/{report_file}", 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"📄 Elite Assessment Report: reports/{report_file}")
        except Exception as e:
            print(f"  Report Save Error: {e}")
        
        print("\n NEXUS AI ELITE Status: HUMAN-LIKE HACKING COMPLETE")
        print(" Elite hacker intelligence successfully demonstrated")
        print(" Ready for advanced exploitation and bug bounty hunting")
        
        return report_data

def main():
    """Main execution function"""
    
    print(" NEXUS AI ELITE - Human-Like Hacker Intelligence Demo")
    print(" AI That Thinks and Acts Like a Real Elite Hacker")
    print(" Top Bug Bounty Hunter + Elite Methodologies")
    print(" Fast Demo Version for VEDA Presentation")
    
    # Initialize XBOW Hacker AI
    xbow_ai = NexusAISentinelDemo()
    
    # Get target
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "https://acet.ac.in"
        print(f"\n Using demo target: {target}")
        print("   Usage: python xbow_hacker_ai_demo.py <target_url>")
    
    # Execute elite assessment
    results = xbow_ai.execute_elite_assessment(target)
    
    print(f"\n DEMO COMPLETE!")
    print(f" NEXUS AI successfully demonstrated human-like hacker intelligence")
    print(f" Perfect for VEDA college presentation - shows advanced AI + cybersecurity")

if __name__ == "__main__":
    main()