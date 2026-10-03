from tools import find_latest_invoice, record_invoice, verify_invoice


def run_agent(vendor):

    logs = []

    # Step 1: Understand the task
    logs.append("Understanding request...")
    logs.append(f"Task: Process latest invoice from {vendor}")

    # Step 2: Create a plan
    plan = [
        "Search for matching invoices",
        "Select the latest invoice",
        "Extract invoice details",
        "Record invoice in company ledger",
        "Verify the saved record"
    ]

    logs.append("Execution plan created.")

    # Step 3: Find invoice
    logs.append("Searching invoice files...")

    invoice = find_latest_invoice(vendor)

    if invoice is None:
        logs.append("No valid invoice found.")
        return {
            "status": "failed",
            "message": "Could not find a valid invoice.",
            "logs": logs,
            "invoice": None
        }

    logs.append(
        f"Found invoice: {invoice['invoice_number']}"
    )

    # Step 4: Record invoice
    logs.append("Recording invoice...")

    saved = record_invoice(invoice)

    if not saved:
        logs.append("Decision: Invoice already exists, so no duplicate record was created.")

    # Step 5: Verify
    logs.append("Verifying ledger...")

    verified = verify_invoice(invoice["invoice_number"])

    if verified:
        logs.append("Verification successful: Invoice number was found in the company ledger.")

        return {
            "status": "completed",
            "message": "Invoice successfully processed and verified.",
            "logs": logs,
            "invoice": invoice
        }

    logs.append("Verification failed.")

    return {
        "status": "failed",
        "message": "Invoice could not be verified.",
        "logs": logs,
        "invoice": invoice
    }