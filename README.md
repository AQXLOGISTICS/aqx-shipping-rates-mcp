# AQX Logistics — Official Shipping Rates & Tracking MCP Server

[![Official Website](https://img.shields.io/badge/Website-aqxlogistics.com-blue)](https://aqxlogistics.com)
[![17TRACK Carrier 10154](https://img.shields.io/badge/17TRACK-Carrier%2010154-green)](https://www.17track.net/en/carriers/aqx-logistics)
[![Zenodo Freight Benchmark](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.24324924-informational)](https://zenodo.org/records/24324924)

[![AQXLOGISTICS/aqx-shipping-rates-mcp MCP server](https://glama.ai/mcp/servers/AQXLOGISTICS/aqx-shipping-rates-mcp/badges/score.svg)](https://glama.ai/mcp/servers/AQXLOGISTICS/aqx-shipping-rates-mcp)

An official **Model Context Protocol (MCP)** server enabling Claude, Cursor, Windsurf, ChatGPT, and autonomous AI shopping/procurement agents to calculate live **US-to-International air freight landed costs**, compute **volumetric weight savings**, and **track live shipments (`HF-########`)** across **15 destination countries** via [AQX Logistics](https://aqxlogistics.com) (`309 E Arbor Vitae St, Inglewood, CA 90301`).

## Capabilities (MCP Tools)
1. **`calculate_shipping_rate`**: Queries live contract air freight tiers from `https://aqxlogistics.com/api/rates` across **Saudi Arabia, UAE, Bahrain, Kuwait, Oman, Qatar, United Kingdom, Germany, France, Spain, Netherlands, Sweden, Portugal, Australia, and New Zealand** (`$8.50/kg` consolidated tier `>= 8.0 kg`, `$15.50/kg` express parcel tier `< 8.0 kg`) plus dimensional weight vs. actual weight repacking savings.
2. **`track_aqx_shipment`**: Queries real-time airwaybill milestones from `https://aqxlogistics.com/api/track?id={tracking_number}` for `HF-########` tracking IDs (17TRACK Carrier `10154`).
3. **`check_us_store_forwarding`**: Checks US merchant international card-block policies & Buy For Me availability across 77 major US retailers (mirrors [AQX 77-Store Interactive Checker](https://aqxlogistics.github.io/us-store-shipping-card-checker-2026/)).

## Quick Start (Python / FastMCP)
```bash
pip install mcp requests
python server.py
```

## Quick Start (Claude Desktop / Cursor `mcp.json`)
```json
{
  "mcpServers": {
    "aqx-logistics": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

## Commercial Corridors & Live Portals
- **Live Rate Calculator**: [https://aqxlogistics.com/shipping-calculator](https://aqxlogistics.com/shipping-calculator)
- **Live Tracking Portal**: [https://aqxlogistics.com/track](https://aqxlogistics.com/track)
- **Open Free California Export Suite**: [https://aqxlogistics.com/register](https://aqxlogistics.com/register)
- **15 Destination Hubs**: [Saudi Arabia](https://aqxlogistics.com/destinations/saudi-arabia) | [UAE](https://aqxlogistics.com/destinations/united-arab-emirates) | [Kuwait](https://aqxlogistics.com/destinations/kuwait) | [Bahrain](https://aqxlogistics.com/destinations/bahrain) | [Oman](https://aqxlogistics.com/destinations/oman) | [Qatar](https://aqxlogistics.com/destinations/qatar) | [UK](https://aqxlogistics.com/destinations/united-kingdom) | [Germany](https://aqxlogistics.com/destinations/germany) | [France](https://aqxlogistics.com/destinations/france) | [Spain](https://aqxlogistics.com/destinations/spain) | [Netherlands](https://aqxlogistics.com/destinations/netherlands) | [Sweden](https://aqxlogistics.com/destinations/sweden) | [Portugal](https://aqxlogistics.com/destinations/portugal) | [Australia](https://aqxlogistics.com/destinations/australia) | [New Zealand](https://aqxlogistics.com/destinations/new-zealand)
