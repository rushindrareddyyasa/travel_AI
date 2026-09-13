import os
import re
import requests
import airportsdata
import pycountry

from dotenv import load_dotenv


load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

BASE_URL = "https://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load("IATA")

# Default origin for queries where the user gives only a destination.
# Change this if you want another default origin.
DEFAULT_ORIGIN_IATA = "HYD"


# ============================================================
# INTERNATIONAL COUNTRY ALIASES
# ============================================================

COUNTRY_ALIASES = {
    "usa": "US",
    "u.s.a": "US",
    "u.s.": "US",
    "america": "US",
    "united states": "US",

    "uk": "GB",
    "u.k.": "GB",
    "britain": "GB",
    "england": "GB",

    "uae": "AE",
    "dubai": "AE",

    "south korea": "KR",
    "korea": "KR",

    "russia": "RU",
    "vietnam": "VN",
    "bangladesh": "BD",

    "india": "IN",
    "japan": "JP",
    "china": "CN",
    "singapore": "SG",
    "malaysia": "MY",
    "thailand": "TH",
    "indonesia": "ID",
    "nepal": "NP",
    "qatar": "QA",
    "saudi arabia": "SA",
    "turkey": "TR",
    "canada": "CA",
    "australia": "AU",
    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
}


# ============================================================
# INTERNATIONAL COUNTRY → MAIN AIRPORT
# ============================================================

COUNTRY_MAIN_AIRPORT = {
    "BD": "DAC",
    "IN": "DEL",
    "JP": "NRT",
    "US": "JFK",
    "GB": "LHR",
    "AE": "DXB",
    "SG": "SIN",
    "MY": "KUL",
    "TH": "BKK",
    "ID": "CGK",
    "CN": "PEK",
    "KR": "ICN",
    "NP": "KTM",
    "QA": "DOH",
    "SA": "JED",
    "TR": "IST",
    "CA": "YYZ",
    "AU": "SYD",
    "DE": "FRA",
    "FR": "CDG",
    "IT": "FCO",
    "ES": "MAD",
}


# ============================================================
# INDIA STATE ALIASES
# ============================================================

INDIA_STATE_ALIASES = {
    "andhra pradesh": "AP",
    "ap": "AP",

    "arunachal pradesh": "AR",
    "arunachal": "AR",

    "assam": "AS",

    "bihar": "BR",

    "chhattisgarh": "CG",
    "chattisgarh": "CG",

    "goa": "GA",

    "gujarat": "GJ",

    "haryana": "HR",

    "himachal pradesh": "HP",
    "himachal": "HP",

    "jharkhand": "JH",

    "karnataka": "KA",

    "kerala": "KL",

    "madhya pradesh": "MP",
    "mp": "MP",

    "maharashtra": "MH",
    "mh": "MH",

    "manipur": "MN",

    "meghalaya": "ML",

    "mizoram": "MZ",

    "nagaland": "NL",

    "odisha": "OD",
    "orissa": "OD",

    "punjab": "PB",

    "rajasthan": "RJ",

    "sikkim": "SK",

    "tamil nadu": "TN",
    "tamilnadu": "TN",
    "tn": "TN",

    "telangana": "TS",
    "ts": "TS",

    "tripura": "TR",

    "uttar pradesh": "UP",
    "up": "UP",

    "uttarakhand": "UK",
    "uttaranchal": "UK",

    "west bengal": "WB",
    "bengal": "WB",

    "delhi": "DL",

    "jammu and kashmir": "JK",
    "jammu & kashmir": "JK",

    "ladakh": "LA",

    "chandigarh": "CH",

    "andaman and nicobar": "AN",
    "andaman and nicobar islands": "AN",

    "puducherry": "PY",
    "pondicherry": "PY",

    "lakshadweep": "LD",
}


# ============================================================
# INDIA STATE → PREFERRED MAIN AIRPORT
# ============================================================

INDIA_STATE_MAIN_AIRPORT = {
    "AP": "VGA",
    "AR": "HGI",
    "AS": "GAU",
    "BR": "PAT",
    "CG": "RPR",
    "GA": "GOI",
    "GJ": "AMD",
    "HR": "DEL",
    "HP": "SLV",
    "JH": "IXR",
    "KA": "BLR",
    "KL": "COK",
    "MP": "IDR",
    "MH": "BOM",
    "MN": "IMF",
    "ML": "SHL",
    "MZ": "AJL",
    "NL": "DMU",
    "OD": "BBI",
    "PB": "ATQ",
    "RJ": "JAI",
    "SK": "PYG",
    "TN": "MAA",
    "TS": "HYD",
    "TR": "IXA",
    "UP": "LKO",
    "UK": "DED",
    "WB": "CCU",
    "DL": "DEL",
    "JK": "SXR",
    "LA": "IXL",
    "CH": "IXC",
    "AN": "IXZ",
    "PY": "PNY",
    "LD": "AGX",
}


# ============================================================
# INDIA CITY → PREFERRED MAIN AIRPORT
# ============================================================

INDIA_CITY_MAIN_AIRPORT = {

    # Andhra Pradesh
    "vijayawada": "VGA",
    "amaravati": "VGA",
    "visakhapatnam": "VTZ",
    "vizag": "VTZ",
    "tirupati": "TIR",
    "rajahmundry": "RJA",
    "kakinada": "RJA",

    # Arunachal Pradesh
    "itanagar": "HGI",
    "holongi": "HGI",

    # Assam
    "guwahati": "GAU",
    "dibrugarh": "DIB",
    "silchar": "IXS",
    "jorhat": "JRH",

    # Bihar
    "patna": "PAT",
    "gaya": "GAY",
    "darbhanga": "DBR",

    # Chhattisgarh
    "raipur": "RPR",
    "bilaspur": "PAB",

    # Goa
    "goa": "GOI",
    "panaji": "GOI",
    "panjim": "GOI",
    "mopa": "GOX",

    # Gujarat
    "ahmedabad": "AMD",
    "vadodara": "BDQ",
    "baroda": "BDQ",
    "surat": "STV",
    "rajkot": "HSR",
    "bhuj": "BHJ",
    "jamnagar": "JGA",
    "bhavnagar": "BHU",

    # Haryana
    "gurgaon": "DEL",
    "gurugram": "DEL",
    "faridabad": "DEL",

    # Himachal Pradesh
    "shimla": "SLV",
    "dharamshala": "DHM",
    "kangra": "DHM",
    "kullu": "KUU",
    "manali": "KUU",

    # Jharkhand
    "ranchi": "IXR",
    "jamshedpur": "IXW",
    "deoghar": "DGH",

    # Karnataka
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "banglore": "BLR",
    "mysore": "MYQ",
    "mysuru": "MYQ",
    "mangalore": "IXE",
    "mangaluru": "IXE",
    "hubli": "HBX",
    "hubballi": "HBX",
    "belgaum": "IXG",
    "belagavi": "IXG",

    # Kerala
    "kochi": "COK",
    "cochin": "COK",
    "thiruvananthapuram": "TRV",
    "trivandrum": "TRV",
    "kozhikode": "CCJ",
    "calicut": "CCJ",
    "kannur": "CNN",

    # Madhya Pradesh
    "indore": "IDR",
    "bhopal": "BHO",
    "gwalior": "GWL",
    "jabalpur": "JLR",

    # Maharashtra
    "mumbai": "BOM",
    "bombay": "BOM",
    "pune": "PNQ",
    "nagpur": "NAG",
    "nashik": "ISK",
    "aurangabad": "IXU",
    "chhatrapati sambhajinagar": "IXU",
    "kolhapur": "KLH",
    "shirdi": "SAG",

    # Manipur
    "imphal": "IMF",

    # Meghalaya
    "shillong": "SHL",

    # Mizoram
    "aizawl": "AJL",

    # Nagaland
    "dimapur": "DMU",

    # Odisha
    "bhubaneswar": "BBI",
    "bbsr": "BBI",
    "cuttack": "BBI",
    "rourkela": "RRK",
    "jharsuguda": "VEJ",

    # Punjab
    "amritsar": "ATQ",
    "ludhiana": "LUH",
    "pathankot": "IXP",

    # Rajasthan
    "jaipur": "JAI",
    "jodhpur": "JDH",
    "udaipur": "UDR",
    "jaisalmer": "JSA",
    "kota": "KTU",

    # Sikkim
    "gangtok": "PYG",
    "pakyong": "PYG",

    # Tamil Nadu
    "chennai": "MAA",
    "madras": "MAA",
    "coimbatore": "CJB",
    "madurai": "IXM",
    "tiruchirappalli": "TRZ",
    "trichy": "TRZ",
    "thoothukudi": "TCR",
    "tuticorin": "TCR",
    "salem": "SXV",

    # Telangana
    "hyderabad": "HYD",
    "secunderabad": "HYD",
    "shamshabad": "HYD",
    "warangal": "WGC",

    # Tripura
    "agartala": "IXA",

    # Uttar Pradesh
    "lucknow": "LKO",
    "varanasi": "VNS",
    "banaras": "VNS",
    "kashi": "VNS",
    "kanpur": "KNU",
    "agra": "AGR",
    "prayagraj": "IXD",
    "allahabad": "IXD",
    "gorakhpur": "GOP",
    "bareilly": "BEK",
    "ayodhya": "AYJ",

    # Uttarakhand
    "dehradun": "DED",
    "rishikesh": "DED",
    "haridwar": "DED",
    "pantnagar": "PGH",

    # West Bengal
    "kolkata": "CCU",
    "calcutta": "CCU",
    "siliguri": "IXB",
    "darjeeling": "IXB",
    "bagdogra": "IXB",
    "durgapur": "RDP",

    # Delhi
    "delhi": "DEL",
    "new delhi": "DEL",
    "ncr": "DEL",

    # Jammu & Kashmir
    "srinagar": "SXR",
    "jammu": "IXJ",

    # Ladakh
    "leh": "IXL",
    "ladakh": "IXL",

    # Chandigarh
    "chandigarh": "IXC",

    # Andaman & Nicobar
    "port blair": "IXZ",
    "andaman": "IXZ",

    # Puducherry
    "puducherry": "PNY",
    "pondicherry": "PNY",

    # Lakshadweep
    "agatti": "AGX",
    "lakshadweep": "AGX",
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:
    text = text.lower().strip()

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    stop_words = [
        "flight",
        "flights",
        "ticket",
        "tickets",
        "trip",
        "travel",
        "plan",
        "complete",
        "days",
        "day",
        "including",
        "hotel",
        "hotels",
        "sightseeing",
        "under",
        "budget",
        "info",
        "information",
    ]

    words = [
        word
        for word in text.split()
        if word not in stop_words
    ]

    return " ".join(words).strip()


# ============================================================
# COUNTRY NAME → COUNTRY CODE
# ============================================================

def country_name_to_code(text: str):

    text = clean_text(text)

    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2

    except LookupError:
        pass

    # Detect country name inside longer text
    for country in pycountry.countries:

        country_name = country.name.lower()

        if country_name in text:
            return country.alpha_2

    # Detect aliases inside longer text
    for alias, code in COUNTRY_ALIASES.items():

        if alias in text:
            return code

    return None


# ============================================================
# CHECK AIRPORT COUNTRY
# ============================================================

def airport_country_matches(
    airport: dict,
    country_code: str
) -> bool:

    airport_country = (
        str(airport.get("country", ""))
        .upper()
        .strip()
    )

    if airport_country == country_code:
        return True

    try:

        country = pycountry.countries.get(
            alpha_2=country_code
        )

        if (
            country
            and airport_country.lower()
            == country.name.lower()
        ):
            return True

    except Exception:
        pass

    return False


# ============================================================
# BEST AIRPORT FOR COUNTRY
# ============================================================

def get_best_airport_for_country(country_code: str):

    preferred = COUNTRY_MAIN_AIRPORT.get(country_code)

    if preferred and preferred in AIRPORTS:
        return preferred

    candidates = []

    for iata, airport in AIRPORTS.items():

        if not iata:
            continue

        if airport_country_matches(
            airport,
            country_code
        ):

            name = str(
                airport.get("name", "")
            ).lower()

            city = str(
                airport.get("city", "")
            ).lower()

            score = 0

            if "international" in name:
                score += 50

            if "intl" in name:
                score += 40

            if "capital" in name:
                score += 20

            if city:
                score += 5

            candidates.append(
                (score, iata)
            )

    if not candidates:
        return None

    candidates.sort(reverse=True)

    return candidates[0][1]


# ============================================================
# RESOLVE LOCATION → IATA
# ============================================================

def resolve_location_to_iata(location: str):
    """
    Converts city/state/country/airport/IATA
    into an IATA airport code.

    Examples:

    Hyderabad       → HYD
    Telangana       → HYD
    Mumbai          → BOM
    Maharashtra     → BOM
    India           → DEL
    Japan           → NRT
    Tokyo           → NRT
    HYD             → HYD
    """

    if not location:
        return None

    raw_location = location.strip()

    # --------------------------------------------------------
    # 1. Direct IATA code
    # --------------------------------------------------------

    if re.fullmatch(
        r"[A-Za-z]{3}",
        raw_location
    ):

        code = raw_location.upper()

        if code in AIRPORTS:
            return code

    location_clean = clean_text(
        raw_location
    )

    if not location_clean:
        return None

    # --------------------------------------------------------
    # 2. Indian city
    # --------------------------------------------------------

    if location_clean in INDIA_CITY_MAIN_AIRPORT:

        return INDIA_CITY_MAIN_AIRPORT[
            location_clean
        ]

    # --------------------------------------------------------
    # 3. Indian state
    # --------------------------------------------------------

    if location_clean in INDIA_STATE_ALIASES:

        state_code = INDIA_STATE_ALIASES[
            location_clean
        ]

        airport = INDIA_STATE_MAIN_AIRPORT.get(
            state_code
        )

        if airport and airport in AIRPORTS:
            return airport

    # --------------------------------------------------------
    # 4. International country
    # --------------------------------------------------------

    country_code = country_name_to_code(
        location_clean
    )

    if country_code:

        airport = get_best_airport_for_country(
            country_code
        )

        if airport:
            return airport

    # --------------------------------------------------------
    # 5. Exact city match from airport database
    # --------------------------------------------------------

    city_matches = []

    for iata, airport in AIRPORTS.items():

        city = str(
            airport.get("city", "")
        ).lower().strip()

        name = str(
            airport.get("name", "")
        ).lower().strip()

        score = 0

        if city == location_clean:
            score += 100

        elif location_clean in city:
            score += 70

        if location_clean in name:
            score += 50

        if "international" in name:
            score += 10

        if score > 0:
            city_matches.append(
                (score, iata)
            )

    if city_matches:

        city_matches.sort(
            reverse=True
        )

        return city_matches[0][1]

    return None


# ============================================================
# FIND LOCATIONS INSIDE QUERY
# ============================================================

def find_location_mentions(query: str):

    q = query.lower()

    mentions = []

    # --------------------------------------------------------
    # International country aliases
    # --------------------------------------------------------

    for alias in COUNTRY_ALIASES:

        if re.search(
            rf"\b{re.escape(alias)}\b",
            q
        ):
            mentions.append(alias)

    # --------------------------------------------------------
    # Country names from pycountry
    # --------------------------------------------------------

    for country in pycountry.countries:

        name = country.name.lower()

        if (
            len(name) >= 4
            and re.search(
                rf"\b{re.escape(name)}\b",
                q
            )
        ):
            mentions.append(name)

    # --------------------------------------------------------
    # Indian states
    # --------------------------------------------------------

    for state in INDIA_STATE_ALIASES:

        if re.search(
            rf"\b{re.escape(state)}\b",
            q
        ):
            mentions.append(state)

    # --------------------------------------------------------
    # Indian cities
    # --------------------------------------------------------

    for city in INDIA_CITY_MAIN_AIRPORT:

        if re.search(
            rf"\b{re.escape(city)}\b",
            q
        ):
            mentions.append(city)

    # Remove duplicates while preserving order
    unique_mentions = []

    for item in mentions:

        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions


# ============================================================
# PARSE ROUTE
# ============================================================

def parse_route(query: str):

    """
    Returns:

    dep_iata, arr_iata

    Examples:

    None, None
        → global live flights

    HYD, BOM
        → Hyderabad to Mumbai

    HYD, None
        → flights from Hyderabad

    None, BOM
        → flights to Mumbai
    """

    q = query.strip()

    q_lower = q.lower()

    # --------------------------------------------------------
    # Global flight query
    # --------------------------------------------------------

    global_keywords = [
        "all country",
        "all countries",
        "global flight",
        "global flights",
        "all flight",
        "all flights",
        "worldwide flight",
        "worldwide flights",
    ]

    if any(
        keyword in q_lower
        for keyword in global_keywords
    ):
        return None, None

    # --------------------------------------------------------
    # Direct IATA route
    # Example: HYD to BOM
    # --------------------------------------------------------

    codes = re.findall(
        r"\b[A-Z]{3}\b",
        q
    )

    valid_codes = [
        code.upper()
        for code in codes
        if code.upper() in AIRPORTS
    ]

    if len(valid_codes) >= 2:

        return (
            valid_codes[0],
            valid_codes[1]
        )

    # --------------------------------------------------------
    # from X to Y
    # --------------------------------------------------------

    match = re.search(
        r"\bfrom\s+(.+?)\s+\bto\s+(.+?)"
        r"(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:

        origin_text = match.group(1)

        destination_text = match.group(2)

        dep_iata = resolve_location_to_iata(
            origin_text
        )

        arr_iata = resolve_location_to_iata(
            destination_text
        )

        return dep_iata, arr_iata

    # --------------------------------------------------------
    # to Y from X
    # --------------------------------------------------------

    match = re.search(
        r"\bto\s+(.+?)\s+\bfrom\s+(.+?)"
        r"(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:

        destination_text = match.group(1)

        origin_text = match.group(2)

        dep_iata = resolve_location_to_iata(
            origin_text
        )

        arr_iata = resolve_location_to_iata(
            destination_text
        )

        return dep_iata, arr_iata

    # --------------------------------------------------------
    # flights from X
    # --------------------------------------------------------

    match = re.search(
        r"\bfrom\s+(.+?)(?:[.!?]|$)",
        q_lower
    )

    if match:

        origin_text = match.group(1)

        dep_iata = resolve_location_to_iata(
            origin_text
        )

        return dep_iata, None

    # --------------------------------------------------------
    # flights to X
    # --------------------------------------------------------

    match = re.search(
        r"\bto\s+(.+?)(?:[.!?]|$)",
        q_lower
    )

    if match:

        destination_text = match.group(1)

        arr_iata = resolve_location_to_iata(
            destination_text
        )

        return None, arr_iata

    # --------------------------------------------------------
    # Fallback location detection
    # --------------------------------------------------------

    mentions = find_location_mentions(q)

    if len(mentions) >= 2:

        dep_iata = resolve_location_to_iata(
            mentions[0]
        )

        arr_iata = resolve_location_to_iata(
            mentions[1]
        )

        return dep_iata, arr_iata

    if len(mentions) == 1:

        arr_iata = resolve_location_to_iata(
            mentions[0]
        )

        return DEFAULT_ORIGIN_IATA, arr_iata

    return None, None


# ============================================================
# FORMAT FLIGHT
# ============================================================

def format_flight(flight: dict):

    airline = (
        flight.get("airline", {}).get("name")
        or "Unknown airline"
    )

    flight_number = (
        flight.get("flight", {}).get("iata")
        or "Unknown flight number"
    )

    status = (
        flight.get("flight_status")
        or "Unknown"
    )

    dep = flight.get(
        "departure",
        {}
    ) or {}

    arr = flight.get(
        "arrival",
        {}
    ) or {}

    dep_airport = (
        dep.get("airport")
        or "Unknown departure airport"
    )

    dep_iata = (
        dep.get("iata")
        or "Unknown"
    )

    dep_terminal = (
        dep.get("terminal")
        or "N/A"
    )

    dep_gate = (
        dep.get("gate")
        or "N/A"
    )

    dep_scheduled = (
        dep.get("scheduled")
        or "Unknown"
    )

    dep_delay = dep.get("delay")

    dep_delay_text = (
        f"{dep_delay} minutes"
        if dep_delay is not None
        else "N/A"
    )

    arr_airport = (
        arr.get("airport")
        or "Unknown arrival airport"
    )

    arr_iata = (
        arr.get("iata")
        or "Unknown"
    )

    arr_terminal = (
        arr.get("terminal")
        or "N/A"
    )

    arr_gate = (
        arr.get("gate")
        or "N/A"
    )

    arr_scheduled = (
        arr.get("scheduled")
        or "Unknown"
    )

    arr_delay = arr.get("delay")

    arr_delay_text = (
        f"{arr_delay} minutes"
        if arr_delay is not None
        else "N/A"
    )

    return f"""
Airline: {airline}
Flight: {flight_number}
Status: {status}

Departure:
- Airport: {dep_airport}
- IATA: {dep_iata}
- Terminal: {dep_terminal}
- Gate: {dep_gate}
- Scheduled: {dep_scheduled}
- Delay: {dep_delay_text}

Arrival:
- Airport: {arr_airport}
- IATA: {arr_iata}
- Terminal: {arr_terminal}
- Gate: {arr_gate}
- Scheduled: {arr_scheduled}
- Delay: {arr_delay_text}
""".strip()


# ============================================================
# SEARCH FLIGHTS
# ============================================================

def search_flights(
    query: str,
    limit: int = 10
):

    if not API_KEY:

        return (
            "Flight API error: "
            "AVIATIONSTACK_API_KEY is missing.\n"
            "Please add this in your .env file:\n"
            "AVIATIONSTACK_API_KEY=your_api_key_here"
        )

    dep_iata, arr_iata = parse_route(
        query
    )

    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    if dep_iata:
        params["dep_iata"] = dep_iata

    if arr_iata:
        params["arr_iata"] = arr_iata

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )

        data = response.json()

    except requests.exceptions.RequestException as e:

        return (
            f"Flight API request failed: {e}"
        )

    except ValueError:

        return (
            "Flight API returned invalid JSON."
        )

    if "error" in data:

        error = data["error"]

        return (
            "Flight API error:\n"
            f"Code: {error.get('code', 'Unknown')}\n"
            f"Message: "
            f"{error.get('message', 'Unknown error')}"
        )

    flight_data = data.get(
        "data",
        []
    )

    if not flight_data:

        route_text = ""

        if dep_iata and arr_iata:

            route_text = (
                f" for route "
                f"{dep_iata} to {arr_iata}"
            )

        elif dep_iata:

            route_text = (
                f" from {dep_iata}"
            )

        elif arr_iata:

            route_text = (
                f" to {arr_iata}"
            )

        return (
            f"No live flight data found"
            f"{route_text}.\n\n"
            "Note: AviationStack provides "
            "live/status flight data, not ticket prices. "
            "For actual fare prices, use a "
            "flight-pricing API such as Amadeus."
        )

    # --------------------------------------------------------
    # Route information
    # --------------------------------------------------------

    route_info = "Global live flights"

    if dep_iata and arr_iata:

        route_info = (
            f"Live flights from "
            f"{dep_iata} to {arr_iata}"
        )

    elif dep_iata:

        route_info = (
            f"Live flights from {dep_iata}"
        )

    elif arr_iata:

        route_info = (
            f"Live flights to {arr_iata}"
        )

    formatted_flights = [
        format_flight(flight)
        for flight in flight_data[:limit]
    ]

    return (
        f"{route_info}\n\n"
        + "\n\n---\n\n".join(
            formatted_flights
        )
    )

