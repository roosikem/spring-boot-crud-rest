# tech_doc_generator.py

import os
from pathlib import Path
from generate_docs_github_copilot import (
    GitHubCopilotClient,
    CodebaseAnalyzer,
    DocumentationGenerator,
    generate_mermaid_diagrams,
)

def main():
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "documentation")
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    copilot_client = GitHubCopilotClient()
    analyzer = CodebaseAnalyzer(PROJECT_ROOT)
    structure = analyzer.analyze_structure()
    pom_content = analyzer.read_pom_xml()

    mermaid_diagrams = generate_mermaid_diagrams(structure)
    doc_gen = DocumentationGenerator(copilot_client, analyzer)

    overview = doc_gen.generate_project_overview(structure, pom_content)
    architecture = doc_gen.generate_architecture_description(structure)
    api_docs = doc_gen.generate_api_documentation(structure['controllers'])

    component_docs = "## Component Details\n\n"
    for controller in structure['controllers'][:2]:
        component_docs += doc_gen.generate_code_explanation(controller) + "\n\n---\n\n"
    for service in structure['services'][:2]:
        component_docs += doc_gen.generate_code_explanation(service) + "\n\n---\n\n"

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
    print(f"✓ Documentation saved to: {doc_path}")

if __name__ == "__main__":
    main()
