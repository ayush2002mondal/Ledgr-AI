from pathlib import Path
import re
import csv
from datetime import datetime


# Location of our invoice folder
BASE_DIR = Path(__file__).parent

INVOICE_DIR = BASE_DIR / "data" / "invoices"

LEDGER_PATH = BASE_DIR / "data" / "ledger.csv"



def find_latest_invoice(vendor):
    """
    Find the latest invoice using exact, partial, or fuzzy vendor matching.
    """

    from difflib import SequenceMatcher

    def normalize(text):
        return re.sub(r"[^a-z0-9]", "", text.lower())

    matching_invoices = []

    search_name = normalize(vendor)

    if not search_name:
        return None

    for file_path in INVOICE_DIR.glob("*.txt"):

        data = extract_invoice_data(file_path)

        if data is None:
            continue

        actual_vendor = data["vendor"]
        actual_name = normalize(actual_vendor)

        # Exact or short-name matching
        is_match = (
            search_name == actual_name
            or (
                len(search_name) >= 3
                and search_name in actual_name
            )
        )

        # Match short vendor prefixes, e.g. xyz -> XYZ Solutions
        if not is_match and len(search_name) >= 3:
            is_match = any(
                word.startswith(search_name)
                for word in re.findall(r"[a-z0-9]+", actual_vendor.lower())
            )

        # Allow minor spelling mistakes in longer names
        if not is_match and len(search_name) >= 5:
            similarity = SequenceMatcher(
                None,
                search_name,
                actual_name
            ).ratio()

            is_match = similarity >= 0.80

        if is_match:
            matching_invoices.append(data)

    if not matching_invoices:
        return None

    matching_invoices.sort(
        key=lambda x: x["invoice_date"],
        reverse=True
    )

    return matching_invoices[0]

def extract_invoice_data(file_path):
    """
    Read an invoice and extract its fields.
    """

    text = file_path.read_text(encoding="utf-8")

    fields = [
        "Vendor",
        "Invoice Number",
        "Invoice Date",
        "Amount",
        "Due Date"
    ]

    extracted = {}

    for field in fields:

        pattern = rf"^{re.escape(field)}:\s*(.+)$"

        match = re.search(
            pattern,
            text,
            re.MULTILINE | re.IGNORECASE
        )

        if not match:
            return None

        extracted[field] = match.group(1).strip()

    try:
        datetime.strptime(extracted["Invoice Date"], "%Y-%m-%d")
        datetime.strptime(extracted["Due Date"], "%Y-%m-%d")
        amount = float(extracted["Amount"])

    except ValueError:
        return None

    return {
        "vendor": extracted["Vendor"],
        "invoice_number": extracted["Invoice Number"],
        "invoice_date": extracted["Invoice Date"],
        "amount": amount,
        "due_date": extracted["Due Date"],
        "source_file": file_path.name
    }


def record_invoice(invoice):
    """
    Save invoice information into the company ledger.
    """

    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LEDGER_PATH.exists()

    columns = [
        "vendor",
        "invoice_number",
        "invoice_date",
        "amount",
        "due_date",
        "source_file"
    ]

    if file_exists:
        with open(LEDGER_PATH, "r", newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

        if any(
            row["invoice_number"] == invoice["invoice_number"]
            for row in existing
        ):
            return False

    with open(
        LEDGER_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(f, fieldnames=columns)

        if not file_exists:
            writer.writeheader()

        writer.writerow(invoice)

    return True

def verify_invoice(invoice_number):

    if not LEDGER_PATH.exists():
        return False

    with open(LEDGER_PATH, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:

        if row["invoice_number"] == invoice_number:
            return True

    return False