"""
Generate social media post drafts from project.md files.
Runs automatically via GitHub Actions on content push.
Can also be run manually: python generate-social.py
"""

import os
import glob
import json
from pathlib import Path
from datetime import datetime

try:
    import anthropic
    import frontmatter
except ImportError:
    print("Run: pip install anthropic python-frontmatter")
    raise

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

FIRM_CONTEXT = {
    "aubyn-architecture": {
        "name": "Aubyn Architecture LLC",
        "tagline": "Form Function Fusion",
        "voice": "sophisticated, design-forward, confident. Emphasizes design integrity, craft, and the architect as guide throughout the entire process.",
        "ig_hashtags": "#architecture #architecturalphotography #designbuild #residentialdesign #aubynarchitecture",
        "li_hashtags": "#architecture #designthinking #ALDB #designbuild #AubynArchitecture",
    },
    "merge4design": {
        "name": "Merge 4 Design LLC",
        "tagline": "Wilmington-Rooted. Built to Deliver.",
        "voice": "direct, community-focused, trustworthy. Emphasizes local knowledge, accessibility, and accountability. Plain-spoken but professional.",
        "ig_hashtags": "#architecture #wilmington #delawarearchitecture #communitydesign #merge4design",
        "li_hashtags": "#architecture #wilmington #communitybuilding #merge4design",
    },
}


def find_updated_projects():
    """Find project.md files modified in the last commit."""
    projects = []
    for firm in ["aubyn-architecture", "merge4design"]:
        pattern = f"{firm}/projects/*/project.md"
        for path in glob.glob(pattern):
            if "_template" not in path:
                projects.append((firm, path))
    return projects


def generate_post(firm_key, project_path, platform):
    """Call Claude API to generate a social post."""
    firm = FIRM_CONTEXT[firm_key]
    project_text = Path(project_path).read_text()

    platform_instructions = {
        "instagram": (
            "Write an Instagram caption. "
            "Opening line must stop the scroll. "
            "3-5 sentences. End with a CTA. "
            "Then hashtags on a new line. Under 2200 chars total. "
        ),
        "linkedin": (
            "Write a LinkedIn post. "
            "Hook in the first line. 3-5 short paragraphs. "
            "End with a question or CTA. 5-8 hashtags at end. "
            "150-300 words. "
        ),
    }

    prompt = f"""You are a social media writer for {firm['name']} — {firm['tagline']}.
Brand voice: {firm['voice']}

Here is the project information:
{project_text}

{platform_instructions[platform]}
Respond ONLY with JSON: {{"post": "...", "hashtags": "..."}}
No markdown, no preamble."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    return json.loads(raw.replace("```json", "").replace("```", "").strip())


def save_draft(firm_key, project_path, platform, content):
    """Save generated post to social/drafts/."""
    project_name = Path(project_path).parent.name
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{project_name}_{platform}.md"
    output_path = Path(f"{firm_key}/social/drafts/{filename}")

    draft = f"""# {platform.title()} — {project_name}
Generated: {date_str}
Project: {project_path}

---

{content['post']}

{content['hashtags']}
"""
    output_path.write_text(draft)
    print(f"  Saved: {output_path}")


def main():
    projects = find_updated_projects()
    if not projects:
        print("No updated projects found.")
        return

    print(f"Found {len(projects)} project(s) to process.")
    for firm_key, project_path in projects:
        print(f"\nProcessing: {project_path}")
        for platform in ["instagram", "linkedin"]:
            try:
                content = generate_post(firm_key, project_path, platform)
                save_draft(firm_key, project_path, platform, content)
            except Exception as e:
                print(f"  Error generating {platform} post: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
