"""
Aubyn Architecture LLC — TD Bank CSV Importer
Maps TD Bank business account exports into the Aubyn Architecture bookkeeping workbook.

Usage
-----
  python3 Aubyn_TD_Importer.py TD-BANK-2025.csv --workbook Aubyn_Architecture_2025_Bookkeeping_v1.xlsx
  python3 Aubyn_TD_Importer.py TD-BANK-2025.csv --workbook Aubyn_Architecture_2025_Bookkeeping_v1.xlsx --year 2025
  python3 Aubyn_TD_Importer.py TD-BANK-2025.csv --workbook Aubyn_Architecture_2025_Bookkeeping_v1.xlsx --output reviewed.xlsx

TD Bank CSV columns: Date, Bank RTN, Account Number, Transaction Type, Description, Debit, Credit, Check Number, Account Running Balance

Rules engine
------------
  1. Transfer detection    (internal moves → Transfer: Between Accounts)
  2. Type-based rules      (DIRECTDEP, DEP, CHECK, etc.)
  3. Vendor keyword rules  (Bluebeam → Software, FedEx → Printing, etc.)
  4. Venture tagging       (Autobooks, ShipStation, DutchLabelShop → FUN2FORM, etc.)
  5. FLAGGED               (unmatched → orange, needs review)

Repo: github.com/werm4d/studio-content
"""

import argparse
import csv
import os
import re
import sys
from collections import Counter
from datetime import datetime

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ── CONSTANTS ──────────────────────────────────────────────────────────────────
ACCOUNT_NAME = "TD Bank ...1406"

# Venture tags — written into col N (Venture) of the workbook
VENTURE_TAGS = {
    "Architecture":   ["BLUEBEAM", "AUTODESK", "SNAPTRUDE", "GREEN BUILD", "REVIT",
                       "ICC ", "INT L CODE", "CONSUMER PROT LICENSE", "DEVLIN LAW",
                       "PARCELS INC", "COMM OF PA", "DE REVENUE", "DE BUSINESS TAX",
                       "PROTON", "HARLAND CLARKE"],
    "FUN2FORM":       ["AUTOBOOKS", "SHIPSTATION", "AUCTANE", "DUTCHLABEL",
                       "BIGCOMMERCE", "SQUARESPACE", "SQ  SQUARE WEEBLY",
                       "PAYPAL INST XFER", "PAYPAL TRANSFER", "M1 PAYMENTS",
                       "MODERN MILL", "USPS PO", "UPS STORE",
                       "FACEBK", "FACEBOOK"],
    "Pattern Signal": ["SHIPSTATION ADD FUNDS"],
    "FORM4FUN":       ["DESCRIPT", "MIDJOURNEY", "YOUTUBE", "VIMEO"],
    "M4Di":           ["PERPLEXITY", "ANTHROPIC"],
    "Mixed":          ["OPENAI", "CHATGPT", "STAPLES", "AMAZON"],
}

def detect_venture(desc_upper):
    for venture, keywords in VENTURE_TAGS.items():
        if any(k in desc_upper for k in keywords):
            return venture
    return ""

# ── RULES ENGINE ──────────────────────────────────────────────────────────────
def make_rules():
    return [
        # ── Transfers ─────────────────────────────────────────────────────────
        (10, lambda d,u,t,deb,cred:
             "ZELLE SENT" in u or "TD ZELLE SENT" in u,
         "Transfer: Between Accounts", "No"),

        # ── Owner draws (Autobooks disbursements OUT) ─────────────────────────
        (12, lambda d,u,t,deb,cred:
             "AUTOBOOKS FUNDS DISB" in u and deb > 0,
         "Equity: Owner Draw", "No"),

        # ── Income — Autobooks funds received ────────────────────────────────
        (12, lambda d,u,t,deb,cred:
             "AUTOBOOKS FUNDS DISB" in u and cred > 0,
         "Income: Architecture Fees", "No"),

        # ── Autobooks platform fee ────────────────────────────────────────────
        (13, lambda d,u,t,deb,cred:
             "AUTOBOOKS" in u and "DISB" not in u,
         "Expense: E-commerce Platform", "No"),

        # ── Income — Zelle received ───────────────────────────────────────────
        (15, lambda d,u,t,deb,cred:
             ("TD ZELLE RECEIVED" in u or "ZELLE RECEIVED" in u) and cred > 0,
         "Income: Architecture Fees", "No"),

        # ── Income — direct deposit (Schwab, payroll) ─────────────────────────
        (15, lambda d,u,t,deb,cred:
             t == "DIRECTDEP" and cred > 0 and "PAYPAL" not in u,
         "Income: Other", "No"),

        # ── Income — PayPal transfer in ───────────────────────────────────────
        (15, lambda d,u,t,deb,cred:
             "PAYPAL TRANSFER" in u and cred > 0,
         "Income: Product Sales", "No"),

        # ── Income — M1 Payments (product refund/credit) ─────────────────────
        (15, lambda d,u,t,deb,cred:
             "M1 PAYMENTS" in u and cred > 0,
         "Income: Product Sales", "No"),

        # ── Income — deposits ─────────────────────────────────────────────────
        (18, lambda d,u,t,deb,cred:
             t in ("DEP", "DIRECTDEP") and cred > 0,
         "Income: Architecture Fees", "No"),

        # ── Amazon refund/credit ──────────────────────────────────────────────
        (18, lambda d,u,t,deb,cred:
             "AMAZON" in u and t == "CREDIT" and cred > 0,
         "Income: Other", "No"),

        # ── Check payments ────────────────────────────────────────────────────
        (20, lambda d,u,t,deb,cred:
             t == "CHECK" and deb > 0,
         "Expense: Consultants (1099)", ""),  # flagged — check payee manually

        # ── Licenses & Permits ────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["DE BUSINESS TAX", "DE REVENUE TAX", "COMM OF PA",
                                   "CONSUMER PROT LICENSE", "PHILA26", "PHILA REV"]),
         "Expense: Licenses & Permits", "No"),

        # ── Insurance ─────────────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["HARTFORD", "INSUREON", "HISCOX", "INSURANCE"]),
         "Expense: Insurance (E&O / General)", "No"),

        # ── Legal / Professional ──────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["DEVLIN LAW", "ATTORNEY", "LAW FIRM", "LEGAL"]),
         "Expense: Professional Fees (Legal)", "No"),

        # ── Software — Architecture ───────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["BLUEBEAM", "AUTODESK", "SNAPTRUDE",
                                   "REVIT", "ENSCAPE", "RHINO", "FORMIT"]),
         "Expense: Software & Subscriptions", "No"),

        # ── Software — AI tools ───────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["OPENAI", "CHATGPT", "MIDJOURNEY",
                                   "PERPLEXITY", "ANTHROPIC", "CLAUDE"]),
         "Expense: AI Tools", "No"),

        # ── Software — general / hosting ─────────────────────────────────────
        (32, lambda d,u,t,deb,cred:
             any(k in u for k in ["BLUEHOST", "HOSTINGER", "SQUARESPACE",
                                   "PROTON", "NOTION", "GITHUB", "INTUIT", "QBOOKS"]),
         "Expense: Software & Subscriptions", "No"),

        # ── Media production ─────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["DESCRIPT", "ADOBE", "PREMIERE", "FINAL CUT"]),
         "Expense: Media Production", "No"),

        # ── E-commerce platforms ──────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["BIGCOMMERCE", "SQ  SQUARE WEEBLY", "SHOPIFY",
                                   "SQUARESPACE", "WEEBLY"]),
         "Expense: E-commerce Platform", "No"),

        # ── Product development / fulfillment ─────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["DUTCHLABEL", "MODERN MILL", "SANMAR",
                                   "PRINTFUL", "PRINTIFY"]),
         "Expense: Product Development", "No"),

        # ── Shipping & postage ────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["SHIPSTATION", "AUCTANE", "USPS", "UPS STORE",
                                   "FEDEX", "PARCELS INC"]),
         "Expense: Postage & Shipping", "No"),

        # ── PayPal fees ───────────────────────────────────────────────────────
        (32, lambda d,u,t,deb,cred:
             "PAYPAL INST XFER" in u and deb > 0 and deb < 50,
         "Expense: Bank & Payment Fees", "No"),

        # ── PayPal larger payments (product purchases) ────────────────────────
        (35, lambda d,u,t,deb,cred:
             "PAYPAL INST XFER" in u and deb >= 50,
         "Expense: Product Development", "No"),

        # ── Advertising / social ──────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["FACEBK", "FACEBOOK", "INSTAGRAM",
                                   "GOOGLE ADS", "META ADS"]),
         "Expense: Advertising & Marketing", "No"),

        # ── Printing / office ─────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["STAPLES", "FEDEX OFFIC", "KINKOS"]),
         "Expense: Printing & Repro", "No"),

        # ── Office supplies / Amazon ──────────────────────────────────────────
        (35, lambda d,u,t,deb,cred:
             any(k in u for k in ["AMAZON MKTPL", "AMAZON MKTPLACE", "OFFICE DEPOT"]),
         "Expense: Office Supplies", "No"),

        # ── Continuing education ──────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["GREEN BUILD", "INT L CODE", "ICC ",
                                   "AIA ", "CONTINUING ED", "UDEMY", "COURSERA"]),
         "Expense: Continuing Education", "No"),

        # ── Equipment > $2,500 (Lenovo laptop) ───────────────────────────────
        (30, lambda d,u,t,deb,cred:
             "LENOVO" in u and deb >= 2500,
         "Expense: Equipment (>$2,500 capitalize)", "No"),

        # ── Equipment < $2,500 ────────────────────────────────────────────────
        (32, lambda d,u,t,deb,cred:
             any(k in u for k in ["LENOVO", "BEST BUY", "B&H", "ADORAMA",
                                   "HOME DEPOT", "LOWES"]),
         "Expense: Equipment (<$2,500)", "No"),

        # ── Meals ─────────────────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["JAVA BEAN", "RESTAURANT", "CAFE", "TST*",
                                   "HUMMINGBIRD", "DOORDASH", "GRUBHUB", "STARBUCKS",
                                   "SP PLUS"]),  # SP Plus = parking/food venue
         "Expense: Meals (50% deductible)", "No"),

        # ── Travel ────────────────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["AMTRAK", "UNITED", "DELTA", "SOUTHWEST",
                                   "MARRIOTT", "HILTON", "AIRBNB", "UBER", "LYFT"]),
         "Expense: Travel", "No"),

        # ── Bank fees ────────────────────────────────────────────────────────
        (30, lambda d,u,t,deb,cred:
             any(k in u for k in ["HARLAND CLARKE", "CHK ORDERS", "WIRE FEE",
                                   "SERVICE CHARGE", "INTL T XN FEE"]),
         "Expense: Bank & Payment Fees", "No"),

        # ── Research & Dev tracking ───────────────────────────────────────────
        # Nothing auto-assigned here — flag for manual decision
    ]

RULES = make_rules()

def parse_amt(s):
    if not s: return 0.0
    try: return float(str(s).strip().replace(',',''))
    except: return 0.0

def extract_payee(desc, type_):
    """Extract clean payee name from TD Bank description."""
    # Zelle received
    m = re.search(r'Zelle\s+(.+?)$', desc, re.I)
    if m: return m.group(1).strip()[:40]
    # VISA DDA PUR — extract merchant name
    m = re.search(r'VISA DDA (?:PUR|REF) AP \d+\s+(.+?)\s{2,}', desc)
    if m:
        raw = m.group(1).strip()
        raw = re.sub(r'\s+\d{3}[\s-]x\d+', '', raw).strip()
        return raw[:40]
    # Direct debit
    m = re.search(r'(?:DIRECTDEBIT|DIRECTDEP)\s+(.+?)$', desc, re.I)
    if m: return m.group(1).strip()[:40]
    # Default — first 40 chars cleaned
    return re.sub(r'\s+', ' ', desc).strip()[:40]

def categorize(row):
    desc  = row['Description'] or ''
    type_ = row['Transaction Type'] or ''
    deb   = parse_amt(row['Debit'])
    cred  = parse_amt(row['Credit'])
    upper = desc.upper()

    category   = None
    is1099     = ""
    flag       = False
    payee      = extract_payee(desc, type_)
    venture    = detect_venture(upper)

    # CHECK payments — always flag for manual payee entry
    if type_ == "CHECK" and deb > 0:
        category = "Expense: Consultants (1099)"
        is1099   = ""
        flag     = True
        payee    = f"Check #{row.get('Check Number','').strip()}"

    if not category:
        for priority, match_fn, cat, i9 in sorted(RULES, key=lambda x: x[0]):
            try:
                if match_fn(row, upper, type_, deb, cred):
                    category = cat
                    if i9: is1099 = i9
                    break
            except Exception:
                continue

    if not category:
        category = ""
        flag = True

    # Deposits without clear source — flag for project assignment
    if type_ in ("DEP", "DIRECTDEP") and cred > 0 and not flag:
        flag = True  # needs ProjectClient annotation

    # Lenovo laptop $2,300 — flag for CPA (capitalize vs expense decision)
    if "LENOVO" in upper and deb > 0:
        flag = True

    return {
        'category': category,
        'payee':    payee,
        'is1099':   is1099,
        'venture':  venture,
        'flag':     flag,
        'category_auto': bool(category and not flag),
    }

# ── WORKBOOK WRITER ───────────────────────────────────────────────────────────
def import_csv(csv_path, workbook_path, output_path, year_filter=None):
    wb = load_workbook(workbook_path)
    ws = wb['01_Transactions']

    last_row = 2
    for row in ws.iter_rows(min_row=3):
        if any(c.value is not None for c in row[:6]):
            last_row = row[0].row

    # Dedup set
    existing = set()
    for row in ws.iter_rows(min_row=3, values_only=True):
        if row[0] and row[5] is not None:
            try:
                d = row[0]
                if hasattr(d,'date'): d = d.date()
                existing.add((str(d), str(row[5])[:20]))
            except: pass

    ORANGE = "FCE4D6"; LGRAY = "F2F2F2"; DGRAY = "595959"
    BLK = "000000"; BLUE_IN = "0000FF"; GREEN_L = "008000"; RED_W = "C00000"

    def hf(c): return PatternFill("solid", start_color=c, end_color=c)
    def tb():
        s = Side(style="thin", color="BFBFBF")
        return Border(left=s,right=s,top=s,bottom=s)

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        csv_rows = list(csv.DictReader(f))

    stats = {'imported':0,'skipped_dup':0,'flagged':0,'auto_cat':0}
    import_rows = []

    for csv_row in csv_rows:
        desc  = (csv_row.get('Description') or '').strip()
        deb   = parse_amt(csv_row.get('Debit',''))
        cred  = parse_amt(csv_row.get('Credit',''))
        type_ = (csv_row.get('Transaction Type') or '').strip()
        amt   = cred - deb  # signed amount

        try:
            txn_date = datetime.strptime(csv_row['Date'].strip(), '%m/%d/%Y').date()
        except:
            continue

        if year_filter and txn_date.year != year_filter:
            continue

        dup_key = (str(txn_date), str(round(amt,2))[:20])
        if dup_key in existing:
            stats['skipped_dup'] += 1
            continue

        result = categorize(csv_row)
        q_num  = (txn_date.month - 1) // 3 + 1

        import_rows.append({
            'date':       txn_date,
            'account':    ACCOUNT_NAME,
            'banktype':   type_,
            'desc':       desc[:120],
            'payee':      result['payee'][:50],
            'amount':     amt,
            'debit':      deb,
            'credit':     cred,
            'category':   result['category'],
            'taxline':    "",
            'is1099':     result['is1099'],
            'contractor': "",
            'project':    "",
            'venture':    result['venture'],
            'memo':       "",
            'reviewed':   "",
            'quarter':    f"Q{q_num}",
            'month':      txn_date.month,
            'flag':       result['flag'],
            'category_auto': result['category_auto'],
        })
        existing.add(dup_key)
        if result['flag']:     stats['flagged'] += 1
        if result['category_auto']: stats['auto_cat'] += 1
        stats['imported'] += 1

    import_rows.sort(key=lambda x: x['date'])

    for ir in import_rows:
        r = last_row + 1
        last_row = r

        vals = [
            (1,  ir['date'],       'MM/DD/YYYY',                    BLK),
            (2,  ir['account'],    '@',                             DGRAY),
            (3,  ir['banktype'],   '@',                             DGRAY),
            (4,  ir['desc'],       '@',                             DGRAY),
            (5,  ir['payee'],      '@',                             BLK),
            (6,  ir['amount'],     '$#,##0.00;($#,##0.00);"-"',    BLK if ir['amount']>=0 else RED_W),
            (7,  ir['debit'],      '$#,##0.00;($#,##0.00);"-"',    BLK),
            (8,  ir['credit'],     '$#,##0.00;($#,##0.00);"-"',    BLK),
            (9,  ir['category'],   '@',                             BLK if ir['category'] else BLUE_IN),
            (10, ir['taxline'],    '@',                             DGRAY),
            (11, ir['is1099'],     '@',                             BLK),
            (12, ir['contractor'], '@',                             BLK),
            (13, ir['project'],    '@',                             BLK),
            (14, ir['venture'],    '@',                             BLK),
            (15, ir['memo'],       '@',                             BLK),
            (16, ir['reviewed'],   '@',                             BLK),
            (17, f'="Q"&INT((MONTH(A{r})+2)/3)', '@',              DGRAY),
            (18, f'=MONTH(A{r})',  '0',                             DGRAY),
        ]

        for col, val, fmt, color in vals:
            cell = ws.cell(r, col, value=val)
            cell.font = Font(name="Arial", size=10, color=color)
            cell.number_format = fmt
            cell.border = tb()
            cell.alignment = Alignment(vertical="center", wrap_text=(col==4))
            if ir['flag'] and col in [5,9,14]:
                cell.fill = hf(ORANGE)
            elif col == 9 and ir['category_auto']:
                cell.fill = hf("E2EFDA")
            elif col == 9 and not ir['category']:
                cell.fill = hf(ORANGE)

        ws.row_dimensions[r].height = 16

    wb.save(output_path)
    return stats, import_rows

# ── CLI ───────────────────────────────────────────────────────────────────────
def build_output_path(workbook_path):
    base, ext = os.path.splitext(workbook_path)
    return f"{base}_imported{ext}"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Aubyn Architecture — TD Bank CSV Importer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 Aubyn_TD_Importer.py TD-BANK-2025.csv --workbook Aubyn_Architecture_2025_Bookkeeping_v1.xlsx
  python3 Aubyn_TD_Importer.py TD-BANK-2025.csv --workbook Aubyn_Architecture_2025_Bookkeeping_v1.xlsx --year 2025
        """
    )
    parser.add_argument("csv", metavar="CSV_FILE", help="TD Bank CSV export")
    parser.add_argument("--workbook","-w", required=True, metavar="XLSX_FILE")
    parser.add_argument("--output","-o", default=None, metavar="OUTPUT_FILE")
    parser.add_argument("--year","-y", type=int, default=None, metavar="YYYY")
    parser.add_argument("--account", default=ACCOUNT_NAME)
    return parser.parse_args()

if __name__ == "__main__":
    args    = parse_args()
    out     = args.output or build_output_path(args.workbook)

    if not os.path.isfile(args.csv):
        print(f"ERROR: CSV not found: {args.csv}", file=sys.stderr); sys.exit(1)
    if not os.path.isfile(args.workbook):
        print(f"ERROR: Workbook not found: {args.workbook}", file=sys.stderr); sys.exit(1)

    print(f"TD Bank CSV:  {args.csv}")
    print(f"Workbook:     {args.workbook}")
    print(f"Output:       {out}")
    print(f"Year filter:  {args.year or 'ALL'}")
    print()

    stats, rows = import_csv(args.csv, args.workbook, out, args.year)

    print(f"Results:")
    print(f"  Total CSV rows:       {stats['imported'] + stats['skipped_dup']}")
    print(f"  Imported:             {stats['imported']}")
    print(f"  Skipped (dupes):      {stats['skipped_dup']}")
    print(f"  Auto-categorized:     {stats['auto_cat']}")
    print(f"  Flagged for review:   {stats['flagged']}")
    print()

    flagged = [r for r in rows if r['flag']]
    if flagged:
        print(f"── NEEDS MANUAL REVIEW ({len(flagged)} rows) ──────────────────")
        for r in flagged:
            cat = f"CAT: {r['category']!r}" if r['category'] else "NO CATEGORY"
            print(f"  {r['date']}  {r['amount']:>10.2f}  {r['desc'][:55]:<55}  {cat}")

    print()
    print("── CATEGORY BREAKDOWN ──────────────────────────────────")
    cat_counts = Counter(r['category'] for r in rows if r['category'])
    for cat, count in sorted(cat_counts.items()):
        total = sum(abs(r['amount']) for r in rows if r['category']==cat)
        print(f"  {count:>3}x  {cat:<48}  ${total:>10,.2f}")

    print()
    print("── VENTURE BREAKDOWN ───────────────────────────────────")
    vent_counts = Counter(r['venture'] for r in rows if r['venture'])
    for vent, count in sorted(vent_counts.items()):
        print(f"  {count:>3}x  {vent}")

    print(f"\nOutput: {out}")
