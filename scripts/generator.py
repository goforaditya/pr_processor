import os
import random
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

OUTPUT_DIR = "C:/Users/adity/.gemini/antigravity/scratch/pr_processor/sample_prs"

def create_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def generate_simple_pr(filename, vendor_name, items, total, pr_id):
    """Generates a simple, clean PR with a standard table."""
    c = canvas.Canvas(os.path.join(OUTPUT_DIR, filename), pagesize=LETTER)
    width, height = LETTER

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, f"Purchase Request #{pr_id}")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Vendor: {vendor_name}")
    c.drawString(50, height - 100, f"Date: 2024-05-10")

    # Table Header
    y = height - 150
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item Description")
    c.drawString(300, y, "Quantity")
    c.drawString(400, y, "Unit Price")
    c.drawString(500, y, "Total")
    
    # Items
    y -= 20
    c.setFont("Helvetica", 12)
    for item in items:
        c.drawString(50, y, item['name'])
        c.drawString(300, y, str(item['qty']))
        c.drawString(400, y, f"${item['price']:.2f}")
        c.drawString(500, y, f"${item['qty'] * item['price']:.2f}")
        y -= 20
    
    # Grand Total
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, y, "Grand Total:")
    c.drawString(500, y, f"${total:.2f}")

    c.save()

def generate_complex_pr(filename, vendor_name, items, total, pr_id):
    """Generates a PR using Platypus for a more 'official' look with grid lines."""
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, filename), pagesize=LETTER)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"PURCHASE REQUEST: {pr_id}", styles['Title']))
    elements.append(Paragraph(f"<b>Vendor:</b> {vendor_name}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    data = [['Item Name', 'Qty', 'Unit Cost', 'Line Total']]
    for item in items:
        data.append([
            item['name'],
            item['qty'],
            f"${item['price']:.2f}",
            f"${item['qty'] * item['price']:.2f}"
        ])
    data.append(['', '', 'Total', f"${total:.2f}"])
    
    t = Table(data, colWidths=[250, 50, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t)
    
    doc.build(elements)

def main():
    create_directory()
    
    # Data for comparison
    items_a = [
        {"name": "UltraWidget 3000", "qty": 10, "price": 100.00},
        {"name": "Power Cord 5m", "qty": 5, "price": 15.50},
        {"name": "Warranty 1yr", "qty": 10, "price": 20.00}
    ]
    total_a = sum(i['qty'] * i['price'] for i in items_a)
    
    # Vendor B is cheaper on Widgets, more expensive on Cords
    items_b = [
        {"name": "UltraWidget 3000", "qty": 10, "price": 95.00},
        {"name": "Power Cord 5m", "qty": 5, "price": 18.00},
        {"name": "Warranty 1yr", "qty": 10, "price": 20.00}
    ]
    total_b = sum(i['qty'] * i['price'] for i in items_b)

    # Vendor C has different layout and format
    items_c = [
         {"name": "Office Chair", "qty": 2, "price": 250.00},
         {"name": "Desk Lamp", "qty": 10, "price": 15.00}
    ]
    total_c = sum(i['qty'] * i['price'] for i in items_c)

    print("Generating PR samples...")
    generate_simple_pr("pr_vendor_a.pdf", "Vendor A Corp", items_a, total_a, "PR-1001")
    generate_simple_pr("pr_vendor_b.pdf", "Vendor B Inc", items_b, total_b, "PR-1002")
    generate_complex_pr("pr_vendor_c.pdf", "Vendor C Supplies", items_c, total_c, "PR-2024-X")
    print(f"Generated 3 PDFs in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
