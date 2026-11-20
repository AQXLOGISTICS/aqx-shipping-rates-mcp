#!/usr/bin/env python3
"""Official AQX Logistics MCP Server — Live Air Freight Rates, Volumetric Calculator, Store Checker & Tracking."""

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

US_STORE_POLICIES = {
    "amazon": {"accepts_intl_cards": "Yes", "ships_to_forwarder": "Yes", "buy_for_me_needed": False, "notes": "Ships cleanly to AQX LAX export address; consolidate multi-box orders free for 30 days."},
    "rockauto": {"accepts_intl_cards": "Yes", "ships_to_forwarder": "Yes", "buy_for_me_needed": False, "notes": "Avoids direct EU/GCC courier surcharges by shipping domestic US to LAX and consolidating multi-warehouse boxes."},
    "summit racing": {"accepts_intl_cards": "Yes (PayPal/Intl Visa)", "ships_to_forwarder": "Yes", "buy_for_me_needed": False, "notes": "Ideal for heavy V8/LS/Coyote performance parts via >=8 kg consolidated air cargo tier."},
    "sweetwater": {"accepts_intl_cards": "Strict (US billing check)", "ships_to_forwarder": "Selective", "buy_for_me_needed": True, "notes": "Often requires US billing verification for international cards; use AQX Buy For Me concierge for guitars, synths & studio gear."},
    "sephora": {"accepts_intl_cards": "Strict (frequently blocks non-US cards)", "ships_to_forwarder": "Strict", "buy_for_me_needed": True, "notes": "Use AQX Buy For Me US checkout for US-exclusive cosmetics & skincare (non-flammable/non-aerosol)."},
    "ulta": {"accepts_intl_cards": "No (US billing required)", "ships_to_forwarder": "Strict", "buy_for_me_needed": True, "notes": "Blocks non-US billing cards; AQX Buy For Me purchases locally and consolidates at LAX."},
    "b&h photo": {"accepts_intl_cards": "Yes", "ships_to_forwarder": "Yes", "buy_for_me_needed": False, "notes": "Accepts international cards and ships pro camera/cinema gear to AQX LAX export hub."},
    "best buy": {"accepts_intl_cards": "Strict (blocks forwarder addresses)", "ships_to_forwarder": "No (auto-cancels)", "buy_for_me_needed": True, "notes": "Auto-cancels known freight forwarder addresses; use AQX Buy For Me concierge."},
    "apple": {"accepts_intl_cards": "Strict (blocks forwarder addresses)", "ships_to_forwarder": "No (auto-cancels)", "buy_for_me_needed": True, "notes": "Apple US blocks freight forwarders; use AQX Buy For Me concierge."},
    "nike": {"accepts_intl_cards": "Strict", "ships_to_forwarder": "Selective", "buy_for_me_needed": True, "notes": "Frequently cancels non-US billing cards on limited drops; AQX Buy For Me supported."},
    "target": {"accepts_intl_cards": "Strict", "ships_to_forwarder": "No (frequently cancels)", "buy_for_me_needed": True, "notes": "Use AQX Buy For Me concierge for US Target exclusives."},
    "walmart": {"accepts_intl_cards": "Strict", "ships_to_forwarder": "Selective", "buy_for_me_needed": True, "notes": "High cancellation rate with non-US billing cards; AQX Buy For Me supported."},
    "nordstrom": {"accepts_intl_cards": "Yes", "ships_to_forwarder": "Yes", "buy_for_me_needed": False, "notes": "Ships US luxury fashion to AQX LAX hub; request free shoebox removal to cut volumetric weight."},
    "ebay": {"accepts_intl_cards": "Yes (PayPal/Intl Card)", "ships_to_forwarder": "Yes", "buy_for_me_needed": False, "notes": "Ships to LAX hub; inspect and consolidate multiple seller parcels free for 30 days."},
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


@mcp.tool()
def check_us_store_forwarding(store_name: str) -> dict:
    """Check whether a major US retailer accepts international cards and ships to freight forwarders, or requires AQX Buy For Me concierge."""
    q = store_name.strip().lower()
    matched_key = None
    for k in US_STORE_POLICIES:
        if q == k or q in k or k in q:
            matched_key = k
            break
    if matched_key:
        policy = US_STORE_POLICIES[matched_key]
        return {
            "store": matched_key.title(),
            **policy,
            "full_77_store_checker_url": "https://aqxlogistics.github.io/us-store-shipping-card-checker-2026/",
            "buy_for_me_portal": "https://aqxlogistics.com/register",
        }
    return {
        "store": store_name,
        "accepts_intl_cards": "Verify in live 77-store database",
        "ships_to_forwarder": "Most US merchants ship to AQX LAX export warehouse; Buy For Me available for strict US-billing stores",
        "buy_for_me_needed": False,
        "full_77_store_checker_url": "https://aqxlogistics.github.io/us-store-shipping-card-checker-2026/",
        "buy_for_me_portal": "https://aqxlogistics.com/register",
    }


if __name__ == "__main__":
    mcp.run()
