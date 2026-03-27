# Bonsai MCP Setup Guide
**M4Di CBai Platform — Design Tool Bridge**
*Last updated: 2026-03-27*

---

## What This Is

The Bonsai MCP server connects Claude (via CBai) directly to IFC building models open in Blender. It enables natural language queries against live building information models — asking Claude to pull quantities, inspect spatial structure, list elements, and export drawings without leaving the CBai conversation.

**Source:** `github.com/JotaDeRodriguez/Bonsai_mcp`
**Based on:** BlenderMCP (extended with IFC support via Bonsai BIM addon)
**Protocol:** Model Context Protocol (MCP) over TCP socket

---

## Prerequisites

Before starting, confirm the following are installed on the **design workstation** (Craig's or Travis's machine — not the server):

- [ ] Blender 4.0 or later
- [ ] Python 3.12 or later
- [ ] `uv` package manager
- [ ] Bonsai BIM addon for Blender
- [ ] Git

---

## Step 1 — Install Bonsai BIM Addon

1. Open Blender
2. Go to **Edit → Preferences → Add-ons**
3. Click **Get Extensions** (Blender 4.2+) or search online for Bonsai
4. Search for "Bonsai" in the Extensions marketplace
5. Install and enable the addon
6. Verify: a "Bonsai" panel should appear in the Properties sidebar

Alternatively, install via Blender's Extensions menu directly:
- `https://extensions.blender.org/add-ons/bonsai/`

---

## Step 2 — Install uv Package Manager

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
set Path=C:\Users\[username]\.local\bin;%Path%
```

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Step 3 — Clone the Bonsai MCP Repository

On the design workstation, open a terminal and run:

```bash
git clone https://github.com/JotaDeRodriguez/Bonsai_mcp
cd Bonsai_mcp
```

Note the full path to this directory — you will need it in Step 5.

---

## Step 4 — Install the Blender Addon Component

Inside the cloned repository, there is an `addon.py` file. This creates the socket server inside Blender that receives MCP commands.

1. In Blender: **Edit → Preferences → Add-ons → Install**
2. Navigate to the cloned `Bonsai_mcp` folder
3. Select `addon.py` and install
4. Enable the addon (checkbox)
5. In the addon preferences, note the **Host** and **Port** settings (default: `localhost:9999`)

---

## Step 5 — Configure Claude Desktop (or Open WebUI)

### For Claude Desktop (individual workstation use):

Edit `claude_desktop_config.json`:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this to the `mcpServers` section:

```json
{
  "mcpServers": {
    "Bonsai-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\your\\path\\to\\Bonsai_mcp",
        "run",
        "tools.py"
      ]
    }
  }
}
```

Replace `C:\\your\\path\\to\\Bonsai_mcp` with the actual path from Step 3.

### For Open WebUI (team server use):

Open WebUI MCP integration configuration — add the Bonsai MCP server as a tool endpoint in the Open WebUI admin panel. Point to the workstation's IP address and port 9999.

*Note: For remote team sessions, the workstation running Blender must be network-accessible from the server. Configure firewall rules accordingly.*

---

## Step 6 — Start the Connection

1. Open Blender on the design workstation
2. Load an IFC file via Bonsai (File → Open IFC or use Bonsai's IFC import)
3. In Blender's addon panel, click **Start Server** in the Bonsai MCP section
4. Open Claude Desktop or CBai
5. You should see a hammer icon (🔨) in the interface indicating MCP tools are available

---

## Available IFC Tools

Once connected, Claude has access to these tools:

| Tool | What it does | Example prompt |
|---|---|---|
| `get_ifc_project_info` | Project name, description, entity counts | *"What's the basic info on this IFC project?"* |
| `list_ifc_entities` | List elements by type | *"List all the walls in this model"* |
| `get_ifc_properties` | All properties of a specific element by GlobalId | *"What are the properties of this wall with ID 1Dvrgv7..."* |
| `get_ifc_spatial_structure` | Full spatial hierarchy | *"Show me the spatial structure of this building"* |
| `get_ifc_quantities` | Area, volume, length with filters | *"Give me the area of all ground floor spaces"* |
| `get_ifc_total_structure` | Complete hierarchy including all building elements | *"Show me the complete structure organized by floor"* |
| `export_drawing_png` | 2D/3D drawings as high-res PNG | *"Generate a floor plan PNG for the ground floor at 1920x1080"* |
| `get_ifc_georeferencing_info` | CRS and site coordinates | *"What are the geolocation coordinates for this project?"* |
| `export_bc3_budget` | Construction cost budget file | *"Export a budget file from this IFC model"* |
| `execute_blender_code` | Run arbitrary Python in Blender | Use with caution — save work first |

---

## Troubleshooting

**"Connection refused" error:**
- Make sure Blender is open and the addon server is started
- Check that the port (default 9999) is not blocked by firewall

**IFC model not loading:**
- Verify Bonsai BIM addon is installed and enabled in Blender
- Confirm an IFC file is loaded (not just a regular .blend file)

**Timeout errors:**
- Large IFC models slow down response time
- Break complex requests into smaller steps
- Try: *"List only the first 10 walls"* before asking for all elements

**Tool not appearing in Claude:**
- Restart Claude Desktop after editing config
- Verify the path in `claude_desktop_config.json` is correct and uses escaped backslashes on Windows

---

## Future Extensions (M4Di Roadmap)

The Bonsai MCP server is currently read-focused. Planned M4Di-specific extensions:

1. **Bi-directional editing** — modify IFC model based on natural language instructions
2. **OI Tool quantity sync** — pull IFC quantities directly into M4Di.Oi™ TAKEOFF sheet
3. **ALDi variance trigger** — flag when model changes push cost estimate beyond 15% variance from ROM
4. **Multi-model comparison** — analyze differences between design iterations

---

## Related Documents

- `CBai_Platform_Architecture.md` — full CBai system overview
- `Open_WebUI_Setup_Guide.md` — server-side setup
- `Design_Team_Workflow.md` — how Bonsai fits into the full workflow
