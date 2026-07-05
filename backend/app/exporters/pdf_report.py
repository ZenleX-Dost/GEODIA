from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_structure_sheet_pdf(ouvrage_id: int, ouvrage_data: dict) -> BytesIO:
    """
    Generate a PDF structure sheet for a specific structure.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    title = Paragraph(f"Fiche de Structure : {ouvrage_data.get('nom', 'Inconnu')}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Basic Info
    data = [
        ["Code", ouvrage_data.get('code', 'N/A')],
        ["Famille", ouvrage_data.get('famille', 'N/A')],
        ["Classe", ouvrage_data.get('classe', 'N/A')],
        ["Coordonnées", f"{ouvrage_data.get('lat', '')}, {ouvrage_data.get('lon', '')}"]
    ]
    
    t = Table(data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 24))
    
    # Indices Summary
    elements.append(Paragraph("Résumé des Indices", styles['Heading2']))
    indices_data = [
        ["Indice de Capacité Fonctionnelle (ICF)", str(ouvrage_data.get('icf', 'N/A'))],
        ["Indice de Vétusté Physique (IVP)", str(ouvrage_data.get('ivp', 'N/A'))],
        ["Indice de Priorité de Défaut (IPD)", str(ouvrage_data.get('ipd', 'N/A'))],
        ["Indice d'Évaluation des Dommages (IED)", str(ouvrage_data.get('ied', 'N/A'))]
    ]
    t2 = Table(indices_data, colWidths=[300, 150])
    t2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke)
    ]))
    elements.append(t2)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_inspection_report_pdf(inspection_id: int, inspection_data: dict, observations: list) -> BytesIO:
    """
    Generate a PDF inspection report.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    elements = []
    elements.append(Paragraph(f"Rapport d'Inspection #{inspection_id}", styles['Heading1']))
    elements.append(Spacer(1, 12))
    
    # Inspection metadata
    elements.append(Paragraph(f"Date: {inspection_data.get('date', 'N/A')}", styles['Normal']))
    elements.append(Paragraph(f"Inspecteur: {inspection_data.get('inspecteur', 'N/A')}", styles['Normal']))
    elements.append(Paragraph(f"État Global: {inspection_data.get('etat', 'N/A')}", styles['Normal']))
    elements.append(Spacer(1, 24))
    
    # Observations
    elements.append(Paragraph("Observations et Pathologies", styles['Heading2']))
    
    if observations:
        obs_data = [["Zone", "Pathologie", "Gravité", "Étendue"]]
        for obs in observations:
            obs_data.append([
                obs.get("zone", ""),
                obs.get("pathologie_code", ""),
                str(obs.get("gravite", "")),
                f"{obs.get('etendue_pct', 0)}%"
            ])
            
        t = Table(obs_data, colWidths=[100, 150, 100, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#163323')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("Aucune observation enregistrée.", styles['Normal']))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer
