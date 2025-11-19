GitHub Copilot Spaces — Quick Guide (JetBrains-friendly)

Purpose
-------
A concise explanation and how-to for GitHub Copilot Spaces focused on developers using JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, etc.). This guide summarizes what Copilot Spaces is, common use cases, setup steps (web + JetBrains), collaboration/invite flows, limitations and security notes, pricing pointers, and quick tips.

1) What is GitHub Copilot Spaces?
---------------------------------
- High-level: Copilot Spaces is a collaborative, AI-powered coding workspace built by GitHub that combines a shared project context, Copilot AI assistance, and collaboration tools (editor sharing, chat, notes, task context). It helps teams pair-program, review code, and explore large projects with an AI assistant that understands the project's code and context.
- Purpose: accelerate pair programming, onboarding, code reviews, and exploratory development by providing an integrated AI + collaboration experience.

Note: product details and features evolve quickly. For latest official descriptions, search "GitHub Copilot Spaces" on the GitHub Docs site (docs.github.com) and the GitHub blog.

2) Key features & common use cases
----------------------------------
- Shared, persistent workspace (project-level context)
- AI assistant that uses repo context to generate code, tests, and suggestions
- Live collaboration / pair programming with voice/text/chat and synchronized files (real-time or follow mode)
- Task/notes panels to keep context for debugging or design work
- Useful for: pair programming, onboarding visits, design/code walkthroughs, focused debugging sessions, writing tests or refactors with context

3) Prerequisites & account requirements
--------------------------------------
- GitHub account: required.
- GitHub Copilot subscription: required for AI assistance. Team/Enterprise plans may be required for multi-user collaboration in some org setups — verify on the GitHub Copilot pricing page.
- Repo access: appropriate read/write permissions to the repository you open in a Space.
- JetBrains IDE: recent versions of IntelliJ IDEA (Community/Ultimate), PyCharm, WebStorm, etc. For best integration, keep IDE up-to-date.

4) Setup — Web (quick)
----------------------
Checklist (web-first):
- [ ] Sign into GitHub and ensure your account has a Copilot subscription/entitlement.
- [ ] From GitHub, open the repository you want to work on.
- [ ] Look for a "Spaces" or "Open with Copilot Spaces" option (GitHub UI) and create a new Space for the repo or branch.
- [ ] Configure the Space (branch, environment, notes) and start a session.
- [ ] Invite collaborators via the Space's invite UI (email/GitHub usernames). Set roles/permissions as needed.
- [ ] Use the built-in chat/notes to coordinate, and ask the Copilot assistant questions in the Space.

Note: exact button/flow names in the GitHub web UI may vary; consult GitHub's Copilot Spaces docs for the current UI flow.

5) Setup — JetBrains IDE (general guidance)
-------------------------------------------
Goal: use Copilot Spaces from JetBrains IDE or open a Space into your IDE for a richer editor experience.

Checklist (JetBrains):
- [ ] Install the official GitHub Copilot plugin from the JetBrains Marketplace (search "GitHub Copilot" in Settings > Plugins). If you already use the Copilot plugin for suggestions, ensure it's updated.
- [ ] Sign in to GitHub via the plugin (the plugin will open a browser OAuth flow). Authorize access for the IDE.
- [ ] (If available) Install any additional JetBrains/third-party plugin that provides "Open in IDE"/Spaces integration (feature availability may vary). Some flows are: "Open in JetBrains IDE" from the GitHub Space web UI, or JetBrains Gateway/Remote features.
- [ ] From the GitHub web Space, if you see "Open in IDE" or "Open in JetBrains"—click it. This may open JetBrains Gateway or prompt the IDE to clone/open the workspace.
- [ ] Alternatively, clone the repository locally and open it in your IDE normally; then sign in to the Copilot plugin to get AI suggestions that are informed by your repo code.

Notes & uncertainties:
- The exact "Open in JetBrains IDE" integration depends on current GitHub features and JetBrains support; it can change. If you don't see a direct open-in-IDE button, use the clone/open flow.
- If your organization uses Codespaces or a remote dev environment, the Spaces-to-IDE experience may use Codespaces or JetBrains Gateway under the hood.

6) Inviting collaborators & managing permissions
------------------------------------------------
- Typically done from the Space web UI: an "Invite" or "Share" button sends invites by GitHub username or email.
- Permission model:
  - Workspace-level roles (host, editor, viewer) — exact names may vary.
  - Repo permissions still control push/merge rights; Space permissions handle editing in-session.
- For org-managed repos, admins may need to configure allowed third-party apps or Copilot entitlements.

7) Known limitations & common gotchas
------------------------------------
- Subscription/licensing: collaborators usually each need a Copilot license if they use AI features; guest viewers may not need one for read-only presence — verify current GitHub policy.
- IDE integration: direct "Open in JetBrains" links may be limited or require extra tooling (Gateway, Codespaces bridge). If in doubt, clone locally and use the Copilot plugin.
- Context size: AI suggestions depend on supplied context; extremely large repos or binary files may not be fully included in context.
- Data handling: code and context may be sent to GitHub's services for AI processing — check your org's data policies and GitHub's privacy/security docs.

8) Pricing & limits (where to check)
------------------------------------
- Pricing and entitlements change often. Check these pages for up-to-date info:
  - GitHub Copilot pricing and plans on github.com (search "GitHub Copilot pricing").
  - GitHub Copilot Spaces documentation and any enterprise/team-level docs.

9) Quick tips & recommended workflows
-------------------------------------
- For pairing: start a Space and have one user host while others join in follow-mode. Use notes to record tasks and context.
- For reviews: create a Space for the PR branch, run tests, and ask Copilot to suggest changes or tests.
- For debugging: paste failing logs into the Space notes and ask Copilot to help narrow the cause; keep reproducible steps in the notes.
- For local work: clone locally and use JetBrains + Copilot plugin to get the best-editor experience while still sharing via a Space when needed.

10) Short FAQ
-------------
Q: Do collaborators need a Copilot subscription to join a Space?
A: Typically, to use AI features interactively they need a Copilot license; read-only viewing or non-AI participation may not require one. Confirm on the GitHub docs for the current policy.

Q: Can I open a Space directly in IntelliJ/PyCharm?
A: There may be an "Open in IDE" flow; if not available, clone the repo and open it in your IDE. Also check if your org uses Codespaces or JetBrains Gateway for smoother remote workflows.

Q: Is my code sent to GitHub?
A: Copilot processes content on GitHub servers to generate suggestions; review GitHub's privacy and data handling docs if you have sensitive data concerns.

Q: Where can I find authoritative docs?
A: Search "Copilot Spaces" on docs.github.com and check the GitHub blog/announcements and JetBrains Marketplace for plugin details.

11) Next steps & options I can do for you
-----------------------------------------
- Add a short step-by-step with screenshots for JetBrains (I can produce images and embed them).
- Add a checklist tailored for organization admins (permission, SSO, app allowlisting).
- Create a small README template you can paste into your repos to onboard teammates to using Spaces.

If you want I can add this file to the repo (documentation/Copilot-Spaces-Guide.md) now and optionally include screenshots or a README template — tell me which option you prefer.

(Disclaimer: I relied on knowledge available up to mid-2024 and general product flows; exact UI labels and integration steps may have changed — verify critical details on docs.github.com and the JetBrains Marketplace.)

