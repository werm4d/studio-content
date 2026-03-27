# Open WebUI Setup Guide
**M4Di CBai Platform — Team Interface**
*Last updated: 2026-03-27*

---

## What This Is

Open WebUI is the team-facing interface for CBai. It is a self-hosted, Docker-based web application that gives all four M4Di partners a shared browser-based chat interface connected to the Anthropic API. It looks and feels like Claude but runs on M4Di's local server, stores all conversation history locally, and is configured with the CBai system prompt and project workspace structure.

**Repository:** `github.com/open-webui/open-webui`
**License:** MIT (free, open source)
**Stars:** 45,000+ (as of early 2026)
**Deployment:** Docker on ThinkPad M550

---

## Server Hardware

**Target machine:** ThinkPad M550 (currently configured as local Ollama server)

Open WebUI does not run the LLM locally — it routes API calls to Anthropic. Hardware requirements are therefore minimal:
- Any modern machine with 4GB+ RAM
- Docker Desktop or Docker Engine installed
- Network accessible to all team members (local network or VPN)

---

## Prerequisites

- [ ] Docker Desktop (Windows/Mac) or Docker Engine (Linux) installed on M550
- [ ] Anthropic API key (from console.anthropic.com)
- [ ] Network access from all team workstations to M550's IP address
- [ ] Port 3000 open on M550's firewall (or configure alternate port)

---

## Step 1 — Install Docker

**On ThinkPad M550 (likely running Ubuntu or Windows):**

Ubuntu/Linux:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Windows: Download Docker Desktop from docker.com and install.

Verify installation:
```bash
docker --version
docker compose version
```

---

## Step 2 — Pull and Run Open WebUI

**Basic installation (Anthropic API backend, no local Ollama required):**

```bash
docker run -d \
  -p 3000:8080 \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

Replace `your_key_here` with the actual Anthropic API key.

**Access:** Open a browser and navigate to `http://[M550-IP-address]:3000`

---

## Step 3 — Initial Configuration

### First launch
1. Navigate to `http://[M550-IP-address]:3000`
2. Create an admin account (use Craig's email)
3. This becomes the CBai admin account

### Add Anthropic as a model provider
1. Go to **Admin Panel → Settings → Connections**
2. Add Anthropic API connection
3. Enter API key
4. Select model: `claude-sonnet-4-6` (or current Sonnet version)
5. Test connection

### Create team accounts
Create accounts for each partner:
- Trevor Knight
- Leo Lynch
- Travis Davis
- David Ainsworth (Craig)

Set roles: Admin (Craig), User (Trevor, Leo, Travis)

---

## Step 4 — Set the CBai System Prompt

The system prompt is what makes Open WebUI behave as CBai rather than a generic Claude interface.

1. Go to **Admin Panel → Settings → Interface**
2. Find the "System Prompt" or "Default Model System Prompt" field
3. Paste the contents of `CBai_System_Prompt_DRAFT.md` (see private docs)

**Important:** The system prompt is M4Di proprietary IP. Do not commit it to any public repository.

---

## Step 5 — Create Project Workspaces

Open WebUI supports workspace organization. Create a workspace for each active project:

Suggested naming convention:
```
[Client] — [Project Name] — [Gate]
Example: CB CDC — Harrison St / Concord Ave — P1
Example: MaxWellness — IDD Campus — P2
Example: WHACC — Athletic Improvements — ROM
```

Each workspace should have its relevant documents uploaded:
- Current OI Tool output (PDF or Excel export)
- Site data and zoning scan
- Client brief or RFP
- ALDi Budget Tracker status
- Any grant package materials

---

## Step 6 — Configure Remote Access (Optional)

For team members working remotely, options:

**Option A — VPN (recommended):**
Set up a VPN server on M550 (WireGuard is lightweight and free). Team members connect via VPN and access `http://[M550-local-IP]:3000` as if on the local network.

**Option B — Cloudflare Tunnel (alternative):**
Use Cloudflare Tunnel to expose Open WebUI via a public URL with authentication. Free tier available.

**Option C — Tailscale (easiest):**
Install Tailscale on M550 and all team workstations. Creates a private mesh network. Free for personal use (up to 3 users — may require upgrade for 4 team members).

---

## Step 7 — Connect Bonsai MCP (Per Workstation)

For design sessions where Claude needs to query the active Blender/IFC model:

1. Ensure Bonsai MCP server is running on the design workstation (see `Bonsai_MCP_Setup_Guide.md`)
2. In Open WebUI admin panel, add the MCP server endpoint
3. Point to the workstation's IP address and port 9999
4. The MCP tools will appear as available in the CBai interface during that session

---

## Maintenance

### Updating Open WebUI
```bash
docker pull ghcr.io/open-webui/open-webui:main
docker stop open-webui
docker rm open-webui
# Re-run the docker run command from Step 2
```

Data persists in the `open-webui` Docker volume — conversations and settings are not lost on update.

### Backup
```bash
docker run --rm \
  -v open-webui:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/open-webui-backup-$(date +%Y%m%d).tar.gz /data
```

Run weekly or before any major update.

### Monitor API usage
Check Anthropic console at `console.anthropic.com` monthly to monitor token usage and costs. Alert threshold: $200/month (investigate if exceeded).

---

## Cost Summary

| Component | Cost |
|---|---|
| Open WebUI | Free (open source) |
| Docker | Free |
| Anthropic API | ~$50–150/month usage |
| Server hardware (M550) | Already owned |
| VPN/Tailscale | Free (personal tier) |

**Total monthly cost: $50–150 in API usage only.**

---

## Troubleshooting

**Can't access from other machines:**
- Verify M550's firewall allows port 3000
- Confirm you're using M550's IP address, not `localhost`
- Check Docker container is running: `docker ps`

**Slow responses:**
- Normal for large document contexts
- Keep project workspace documents focused — don't upload everything, only what's relevant to the current session

**Lost conversation history:**
- History is stored in the Docker volume, not the container
- As long as the volume is intact, history survives container restarts and updates

**API key errors:**
- Verify key is active in Anthropic console
- Check for trailing spaces in the key field

---

## Related Documents

- `CBai_Platform_Architecture.md` — full system overview
- `Bonsai_MCP_Setup_Guide.md` — design tool bridge setup
- `hardware_specs.md` — M550 server specifications (existing doc)
- `CBai_System_Prompt_DRAFT.md` — **PRIVATE / GITIGNORED**
