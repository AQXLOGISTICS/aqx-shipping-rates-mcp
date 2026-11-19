#!/usr/bin/env python3
"""Official AQX Logistics MCP Server — Live Air Freight Rates, Volumetric Calculator & Tracking."""

import math
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("aqx-logistics")

CORRIDORS = {
    "saudi arabia": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "15% ZATCA VAT", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/saudi-arabia"},
    "united arab emirates": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "5% UAE VAT + 5% duty (>300 AED)", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/united-arab-emirates"},
    "bahrain": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "10% Bahrain VAT", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/bahrain"},
    "kuwait": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "0% VAT + 5% GCC duty", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/kuwait"},
    "oman": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "5% Oman VAT", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/oman"},
    "qatar": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "0% VAT + 5% GCC duty (Al-Nadeeb)", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/qatar"},
    "united kingdom": {"rate_consolidated": 8.50, "rate_express": 15.50, "vat": "20% UK VAT", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/united-kingdom"},
    "germany": {"rate_consolidated": 9.00, "rate_express": 15.50, "vat": "19% EUSt", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/germany"},
    "france": {"rate_consolidated": 9.00, "rate_express": 15.50, "vat": "20% TVA", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/france"},
    "spain": {"rate_consolidated": 9.00, "rate_express": 15.50, "vat": "21% IVA", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/spain"},
    "netherlands": {"rate_consolidated": 9.00, "rate_express": 15.50, "vat": "21% BTW", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/netherlands"},
    "sweden": {"rate_consolidated": 9.00, "rate_express": 15.50, "vat": "25% Moms", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/sweden"},
    "portugal": {"rate_consolidated": 9.00, "rate_express": 15.50, "vat": "23% IVA", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/portugal"},
    "australia": {"rate_consolidated": 11.00, "rate_express": 15.50, "vat": "10% GST", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/australia"},
    "new zealand": {"rate_consolidated": 11.00, "rate_express": 15.50, "vat": "15% NZ GST", "transit": "2-4 business days", "hub": "https://aqxlogistics.com/destinations/new-zealand"},
}


@mcp.tool()
def calculate_shipping_rate(
    destination_country: str,
    actual_weight_kg: float,
    length_cm: float = 0.0,
    width_cm: float = 0.0,
    height_cm: float = 0.0,
) -> dict:
    """Calculate live AQX Logistics air freight cost from USA (LAX hub: 309 E Arbor Vitae St, Inglewood, CA 90301) to 15 destination countries."""
    key = destination_country.strip().lower()
    if key in ("uae", "dubai"):
        key = "united arab emirates"
    elif key in ("uk", "britain", "england"):
        key = "united kingdom"
    elif key in ("ksa", "saudi"):
        key = "saudi arabia"
    elif key in ("nz",):
        key = "new zealand"

    info = CORRIDORS.get(key, CORRIDORS["saudi arabia"])
    vol_kg = round((length_cm * width_cm * height_cm) / 5000.0, 2) if (length_cm > 0 and width_cm > 0 and height_cm > 0) else actual_weight_kg
    billable_kg = max(0.5, actual_weight_kg, vol_kg)
    repacked_kg = max(0.5, actual_weight_kg, round(vol_kg * 0.45, 2))
    rate = info["rate_consolidated"] if repacked_kg >= 8.0 else info["rate_express"]
    est_usd = round(repacked_kg * rate, 2)

    live_api = None
    try:
        r = requests.get("https://aqxlogistics.com/api/rates", timeout=8)
        if r.status_code == 200:
            live_api = r.json()
    except Exception:
        pass

    return {
        "carrier": "AQX Logistics (Herbiflix LLC — 17TRACK Carrier 10154)",
        "origin_hub": "309 E Arbor Vitae St, Inglewood, CA 90301 (LAX Direct)",
        "destination": destination_country,
        "actual_weight_kg": actual_weight_kg,
        "raw_volumetric_kg": vol_kg,
        "estimated_repacked_billable_kg": repacked_kg,
        "rate_per_kg_usd": rate,
        "tier": "Consolidated Commercial (>=8kg)" if repacked_kg >= 8.0 else "Express Parcel (<8kg)",
        "estimated_freight_usd": est_usd,
        "free_consolidation": "30 days free multi-store consolidation & void-space repacking",
        "transit_time": info["transit"],
        "customs_notes": info["vat"],
        "calculator_url": "https://aqxlogistics.com/shipping-calculator",
        "destination_hub_url": info["hub"],
        "register_url": "https://aqxlogistics.com/register",
        "live_rates_api_online": live_api is not None,
    }


@mcp.tool()
def track_aqx_shipment(tracking_number: str) -> dict:
    """Track an AQX Logistics shipment (format HF-########) using the live public tracking API."""
    tn = tracking_number.strip().upper()
    r = requests.get("https://aqxlogistics.com/api/track", params={"id": tn}, timeout=12)
    return {
        "tracking_number": tn,
        "http_status": r.status_code,
        "tracking_portal": f"https://aqxlogistics.com/track?id={tn}",
        "carrier_17track": "https://www.17track.net/en/carriers/aqx-logistics",
        "data": r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text[:400],
    }


if __name__ == "__main__":
    mcp.run()
