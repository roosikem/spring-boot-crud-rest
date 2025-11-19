#!/usr/bin/env python3
"""
Technical Documentation Generator using GitHub Copilot
Uses GitHub CLI (gh) with Copilot extension and GitHub Models API
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

try:
    import requests
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


class GitHubCopilotClient:
    """Client for interacting with GitHub Copilot via GitHub CLI and Models API"""

    def __init__(self):
        self.check_gh_cli_installed()
        self.check_copilot_extension()
        self.github_token = self.get_github_token()

    def check_gh_cli_installed(self):
        """Check if GitHub CLI is installed"""
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✓ GitHub CLI installed: {result.stdout.split()[2]}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("\n❌ ERROR: GitHub CLI (gh) is not installed!")
            print("\nInstall it with:")
            print("  macOS:    brew install gh")
            print("  Windows:  winget install GitHub.cli")
            print("  Linux:    See https://github.com/cli/cli#installation")
            print("\nAfter installation, authenticate with: gh auth login")
            sys.exit(1)

    def check_copilot_extension(self):
        """Check if GitHub Copilot CLI extension is installed"""
        try:
            result = subprocess.run(
                ["gh", "extension", "list"],
                capture_output=True,
                text=True,
                check=True
            )
            if "gh-copilot" in result.stdout or "copilot" in result.stdout:
                print("✓ GitHub Copilot extension installed")
            else:
                print("\n⚠️  GitHub Copilot CLI extension not found. Installing...")
                subprocess.run(["gh", "extension", "install", "github/gh-copilot"], check=True)
                print("✓ GitHub Copilot extension installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Could not verify Copilot extension (might still work)")

    def get_github_token(self) -> Optional[str]:
        """Get GitHub authentication token"""
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                check=True
            )
            token = result.stdout.strip()
            if token:
                print("✓ GitHub authentication token found")
                return token
        except subprocess.CalledProcessError:
            print("⚠️  Not authenticated with GitHub CLI")
            print("   Run: gh auth login")
        return None

    def ask_copilot(self, prompt: str, use_cli: bool = True) -> str:
        """
        Ask GitHub Copilot a question using CLI

        Args:
            prompt: The question/prompt to send to Copilot
            use_cli: Whether to use gh copilot CLI (True) or API (False)
        """
        if use_cli:
            return self._ask_via_cli(prompt)
        else:
            return self._ask_via_models_api(prompt)

    def _ask_via_cli(self, prompt: str) -> str:
        """Ask Copilot via GitHub CLI"""
        try:
            # Use gh copilot suggest for code-related questions
            result = subprocess.run(
                ["gh", "copilot", "explain", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                # Fallback: try with suggest
                result = subprocess.run(
                    ["gh", "copilot", "suggest", prompt],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"

        except subprocess.TimeoutExpired:
            return "Error: Request timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def _ask_via_models_api(self, prompt: str) -> str:
        """Ask via GitHub Models API (if available)"""
        if not self.github_token:
            return "Error: GitHub token not available"

        try:
            # GitHub Models API endpoint
            url = "https://api.github.com/models/gpt-4o/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a technical documentation expert for Spring Boot applications."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=data, timeout=60)

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error calling GitHub Models API: {str(e)}"


class CodebaseAnalyzer:
    """Analyzes Java codebase structure"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.src_path = self.project_root / "src" / "main" / "java"

    def find_java_files(self) -> List[Path]:
        """Find all Java files in the project"""
        return list(self.src_path.rglob("*.java"))

    def read_file_content(self, file_path: Path) -> str:
        """Read content of a file"""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            return f"Error reading file: {e}"

    def analyze_structure(self) -> Dict[str, Any]:
        """Analyze project structure"""
        structure = {
            "controllers": [],
            "services": [],
            "repositories": [],
            "models": [],
            "dtos": [],
            "config": [],
            "all_files": []
        }

        java_files = self.find_java_files()

        for file in java_files:
            content = self.read_file_content(file)
            file_info = {
                "name": file.name,
                "path": str(file.relative_to(self.project_root)),
                "content": content
            }

            structure["all_files"].append(file_info)

            if "controller" in file.parent.name.lower():
                structure["controllers"].append(file_info)
            elif "service" in file.parent.name.lower():
                structure["services"].append(file_info)
            elif "repository" in file.parent.name.lower():
                structure["repositories"].append(file_info)
            elif "model" in file.parent.name.lower():
                if "dto" in file.parent.name.lower():
                    structure["dtos"].append(file_info)
                else:
                    structure["models"].append(file_info)
            elif "config" in file.parent.name.lower():
                structure["config"].append(file_info)

        return structure

    def read_pom_xml(self) -> str:
        """Read pom.xml content"""
        pom_path = self.project_root / "pom.xml"
        if pom_path.exists():
            return pom_path.read_text(encoding='utf-8')
        return ""

    def get_file_summary(self, file_info: Dict) -> str:
        """Get a summary of a file for documentation"""
        content = file_info['content']
        lines = content.split('\n')

        # Extract class name and annotations
        summary = f"**{file_info['name']}**\n"
        summary += f"Path: `{file_info['path']}`\n\n"

        # Look for class declaration and main annotations
        for line in lines[:30]:  # Check first 30 lines
            line = line.strip()
            if line.startswith('@') or line.startswith('public class') or line.startswith('public interface'):
                summary += f"- {line}\n"

        return summary


class DocumentationGenerator:
    """Generates technical documentation using GitHub Copilot"""

    def __init__(self, copilot_client: GitHubCopilotClient, analyzer: CodebaseAnalyzer):
        self.copilot = copilot_client
        self.analyzer = analyzer

    def generate_project_overview(self, structure: Dict[str, Any], pom_content: str) -> str:
        """Generate project overview using Copilot"""
        print("  - Generating project overview with Copilot...")

        # Extract key info from pom.xml
        pom_lines = pom_content.split('\n')
        key_dependencies = [line.strip() for line in pom_lines if '<artifactId>' in line][:10]

        prompt = f"""
Analyze this Spring Boot project and write a comprehensive technical overview in Markdown format.

Project Structure:
- {len(structure['controllers'])} Controllers
- {len(structure['services'])} Services
- {len(structure['repositories'])} Repositories
- {len(structure['models'])} Domain Models
- {len(structure['dtos'])} DTOs

Key Dependencies (from pom.xml):
{chr(10).join(key_dependencies[:5])}

Controllers:
{chr(10).join([f"- {c['name']}" for c in structure['controllers']])}

Services:
{chr(10).join([f"- {s['name']}" for s in structure['services']])}

Write a technical overview covering:
1. Project Purpose
2. Technology Stack
3. Architecture Pattern (layered architecture)
4. Key Components Overview

Format in Markdown with headers.
"""

        response = self.copilot.ask_copilot(prompt)
        return response

    def generate_api_documentation(self, controllers: List[Dict]) -> str:
        """Generate API documentation using Copilot"""
        print("  - Generating API documentation with Copilot...")

        if not controllers:
            return "No controllers found."

        # Take the first controller as example
        controller = controllers[0]
        controller_code = controller['content'][:2000]  # First 2000 chars

        prompt = f"""
Analyze this Spring Boot REST controller and generate API documentation in Markdown:

{controller_code}

Include:
1. Base endpoint path
2. All API endpoints with HTTP methods
3. Request/Response formats
4. Path variables and request body parameters
5. HTTP status codes returned
6. Example curl requests

Format as clean Markdown with code blocks for examples.
"""

        response = self.copilot.ask_copilot(prompt)
        return response

    def generate_architecture_description(self, structure: Dict[str, Any]) -> str:
        """Generate architecture description using Copilot"""
        print("  - Generating architecture description with Copilot...")

        # Gather code snippets
        controller_names = [c['name'] for c in structure['controllers']]
        service_names = [s['name'] for s in structure['services']]
        repo_names = [r['name'] for r in structure['repositories']]

        prompt = f"""
Describe the software architecture of this Spring Boot application in Markdown format:

Components:
Controllers: {', '.join(controller_names)}
Services: {', '.join(service_names)}
Repositories: {', '.join(repo_names)}

Explain:
1. Layered Architecture Pattern (Presentation, Business, Persistence)
2. Component Responsibilities
3. Data Flow (Client -> Controller -> Service -> Repository -> Database)
4. Design Patterns Used (DTO pattern, Repository pattern, Dependency Injection)
5. Best Practices Applied

Use Markdown formatting with headers and bullet points.
"""

        response = self.copilot.ask_copilot(prompt)
        return response

    def generate_code_explanation(self, file_info: Dict) -> str:
        """Generate explanation for a specific code file"""
        print(f"  - Analyzing {file_info['name']} with Copilot...")

        code_snippet = file_info['content'][:1500]

        prompt = f"""
Explain this Spring Boot Java code in clear Markdown format:

File: {file_info['name']}
Path: {file_info['path']}

{code_snippet}

Provide:
1. Purpose of this class
2. Key methods and their functionality
3. Dependencies and annotations used
4. How it fits in the overall architecture

Format in Markdown.
"""

        response = self.copilot.ask_copilot(prompt)
        return response


def generate_mermaid_diagrams(structure: Dict[str, Any]) -> str:
    """Generate Mermaid diagram syntax"""

    controller_names = [c['name'].replace('.java', '') for c in structure['controllers']]
    service_names = [s['name'].replace('.java', '') for s in structure['services']]
    repo_names = [r['name'].replace('.java', '') for r in structure['repositories']]
    model_names = [m['name'].replace('.java', '') for m in structure['models']]

    # Architecture Diagram
    arch_diagram = f"""
## System Architecture Diagram

```mermaid
graph TB
    Client[REST Client]

    subgraph "Presentation Layer"
        {chr(10).join([f"        C{i}[{name}]" for i, name in enumerate(controller_names)])}
    end

    subgraph "Business Layer"
        {chr(10).join([f"        S{i}[{name}]" for i, name in enumerate(service_names)])}
    end

    subgraph "Persistence Layer"
        {chr(10).join([f"        R{i}[{name}]" for i, name in enumerate(repo_names)])}
    end

    DB[(H2 Database)]

    Client -->|HTTP/REST| C0
    {chr(10).join([f"    C{i} -->|calls| S{i}" for i in range(min(len(controller_names), len(service_names)))])}
    {chr(10).join([f"    S{i} -->|uses| R{i}" for i in range(min(len(service_names), len(repo_names)))])}
    {chr(10).join([f"    R{i} -->|JPA| DB" for i in range(len(repo_names))])}

    style Client fill:#e1f5ff
    style DB fill:#ffe1e1
```
"""

    # Sequence Diagram
    seq_diagram = """
## Request Flow Sequence

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant Repository
    participant Database

    Client->>Controller: HTTP Request
    activate Controller
    Controller->>Controller: Validate Input
    Controller->>Service: Call Business Logic
    activate Service
    Service->>Repository: Data Access
    activate Repository
    Repository->>Database: SQL Query
    Database-->>Repository: Result Set
    Repository-->>Service: Domain Object
    deactivate Repository
    Service-->>Controller: DTO
    deactivate Service
    Controller-->>Client: HTTP Response
    deactivate Controller
```
"""

    return arch_diagram + "\n" + seq_diagram


# python

def main():
    print("=" * 70)
    print("Technical Documentation Generator using GitHub Copilot")
    print("=" * 70)
    print()

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "documentation")
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    print("[1/5] Initializing GitHub Copilot...")
    try:
        copilot_client = GitHubCopilotClient()
    except SystemExit:
        return
    print()

    print("[2/5] Analyzing codebase structure...")
    analyzer = CodebaseAnalyzer(PROJECT_ROOT)
    structure = analyzer.analyze_structure()
    pom_content = analyzer.read_pom_xml()

    print(f"  Found: {len(structure['controllers'])} controllers, "
          f"{len(structure['services'])} services, "
          f"{len(structure['repositories'])} repositories")
    print()

    print("[3/5] Generating architecture diagrams...")
    mermaid_diagrams = generate_mermaid_diagrams(structure)
    print("  ✓ Mermaid diagrams generated")
    print()

    print("[4/5] Generating documentation with GitHub Copilot...")
    doc_gen = DocumentationGenerator(copilot_client, analyzer)

    overview = doc_gen.generate_project_overview(structure, pom_content)
    architecture = doc_gen.generate_architecture_description(structure)
    api_docs = doc_gen.generate_api_documentation(structure['controllers'])

    component_docs = "## Component Details\n\n"
    for controller in structure['controllers'][:2]:
        component_docs += doc_gen.generate_code_explanation(controller) + "\n\n---\n\n"
    for service in structure['services'][:2]:
        component_docs += doc_gen.generate_code_explanation(service) + "\n\n---\n\n"

    print("  ✓ All documentation sections generated")
    print()

    print("[5/5] Compiling final documentation...")

    full_documentation = f"""# Spring Boot CRUD REST Application
## Technical Documentation
### Generated with GitHub Copilot

---

{overview}

---

{architecture}

---

{api_docs}

---

{component_docs}

---

{mermaid_diagrams}

---

## Project File Structure

### Controllers
{chr(10).join([f"- **{c['name']}** - `{c['path']}`" for c in structure['controllers']])}

### Services
{chr(10).join([f"- **{s['name']}** - `{s['path']}`" for s in structure['services']])}

### Repositories
{chr(10).join([f"- **{r['name']}** - `{r['path']}`" for r in structure['repositories']])}

### Domain Models
{chr(10).join([f"- **{m['name']}** - `{m['path']}`" for m in structure['models']])}

### DTOs
{chr(10).join([f"- **{d['name']}** - `{d['path']}`" for d in structure['dtos']])}

---

*Generated automatically using GitHub Copilot*
*Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Tool: GitHub CLI with Copilot Extension*
"""

    doc_path = Path(OUTPUT_DIR) / "tech_final.md"
    doc_path.write_text(full_documentation, encoding='utf-8')
    print(f"  ✓ Documentation saved to: {doc_path}")
    print()

    print("=" * 70)
    print("DOCUMENTATION GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nGenerated file:")
    print(f"  📄 {doc_path}")
    print(f"\nDocumentation includes:")
    print(f"  • Project Overview (generated by Copilot)")
    print(f"  • Architecture Description (generated by Copilot)")
    print(f"  • API Documentation (generated by Copilot)")
    print(f"  • Component Explanations (generated by Copilot)")
    print(f"  • Architecture Diagrams (Mermaid)")
    print(f"\nView diagrams on GitHub/GitLab or at: https://mermaid.live")
    print()

if __name__ == "__main__":
    main()
