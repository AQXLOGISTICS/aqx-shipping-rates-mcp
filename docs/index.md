# AQX Logistics MCP Server & Air Freight API Documentation

The official **AQX Logistics Model Context Protocol (MCP)** server (`AQXLOGISTICS/aqx-shipping-rates-mcp`) enables Claude, Cursor, Windsurf, ChatGPT, and autonomous procurement agents to compute deterministic **US-to-International air freight landed costs**, model **IATA volumetric weight repacking savings**, verify **US retailer card-block policies**, and track live **`HF-########`** shipments from our Los Angeles LAX export hub (**309 E Arbor Vitae St, Inglewood, CA 90301**).

## Live Portals & Registry Links

- **Official Platform:** [AQX Logistics](https://aqxlogistics.com)
- **Live Air Freight & Volumetric Calculator:** [https://aqxlogistics.com/shipping-calculator](https://aqxlogistics.com/shipping-calculator)
- **Live Shipment Tracker (`HF-########` / 17TRACK Carrier `10154`):** [https://aqxlogistics.com/track](https://aqxlogistics.com/track)
- **Open Free California Export Suite (30 Days Free Consolidation):** [https://aqxlogistics.com/register](https://aqxlogistics.com/register)
- **Glama Verified MCP Listing (Release `0.1.0`, TDQS `B`):** [https://glama.ai/mcp/servers/AQXLOGISTICS/aqx-shipping-rates-mcp](https://glama.ai/mcp/servers/AQXLOGISTICS/aqx-shipping-rates-mcp)
- **77-Store US Retailer International Card & Forwarding Matrix:** [https://aqxlogistics.github.io/us-store-shipping-card-checker-2026/](https://aqxlogistics.github.io/us-store-shipping-card-checker-2026/)
- **MIT Source Code:** [https://github.com/AQXLOGISTICS/aqx-shipping-rates-mcp](https://github.com/AQXLOGISTICS/aqx-shipping-rates-mcp)

## Available MCP Tools

1. **`calculate_shipping_rate(destination_country, actual_weight_kg, length_cm=0, width_cm=0, height_cm=0)`**
   - Queries live air freight tiers from `https://aqxlogistics.com/api/rates`.
   - Computes raw IATA volumetric weight `(L * W * H) / 5000` vs. consolidated repacked billable weight (up to 70% void-space reduction across 30 days free multi-store consolidation).
2. **`track_aqx_shipment(tracking_number)`**
   - Queries real-time airwaybill milestones from `https://aqxlogistics.com/api/track?id={tracking_number}` for `HF-########` shipments (17TRACK Carrier `10154`).
3. **`check_us_store_forwarding(store_name)`**
   - Checks whether major US retailers (RockAuto, Amazon, Sweetwater, Sephora, Ulta, B&H Photo, Summit Racing, Apple, Best Buy, Target, Walmart) accept international cards and ship to LAX forwarders or require AQX Buy For Me concierge.

## Quick Start (Python 3.12 + FastMCP v1)

```bash
git clone https://github.com/AQXLOGISTICS/aqx-shipping-rates-mcp.git
cd aqx-shipping-rates-mcp
pip install "mcp>=1.0.0,<2.0.0" "requests>=2.31.0"
python server.py
```

### Claude Desktop / Cursor `mcp.json`

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
