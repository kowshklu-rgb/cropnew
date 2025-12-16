"""
PDF Report Generator for Precision Agriculture Platform
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def create_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1B5E20'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SubTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#388E3C'),
        spaceAfter=10,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2E7D32'),
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='SmallText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#888888'),
        alignment=TA_CENTER
    ))
    
    return styles


def generate_crop_recommendation_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    styles = create_styles()
    story = []
    
    story.append(Paragraph("🌾 Precision Agriculture Platform", styles['MainTitle']))
    story.append(Paragraph("Crop Recommendation Report", styles['SubTitle']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['SmallText']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4CAF50')))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("📊 Input Parameters", styles['SectionHeader']))
    
    input_data = [
        ['Parameter', 'Value', 'Unit'],
        ['Nitrogen (N)', str(data.get('nitrogen', 'N/A')), 'kg/ha'],
        ['Phosphorus (P)', str(data.get('phosphorus', 'N/A')), 'kg/ha'],
        ['Potassium (K)', str(data.get('potassium', 'N/A')), 'kg/ha'],
        ['Temperature', str(data.get('temperature', 'N/A')), '°C'],
        ['Humidity', str(data.get('humidity', 'N/A')), '%'],
        ['pH Level', str(data.get('ph', 'N/A')), ''],
        ['Soil Type', str(data.get('soil_type', 'N/A')), ''],
        ['Season', str(data.get('season', 'N/A')), ''],
        ['Previous Crop', str(data.get('previous_crop', 'N/A')), ''],
    ]
    
    table = Table(input_data, colWidths=[4*cm, 5*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#81C784')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("🎯 Recommendation Results", styles['SectionHeader']))
    
    recommended = data.get('recommended_crop', 'N/A')
    story.append(Paragraph(f"<b>Primary Recommendation:</b> {recommended}", styles['BodyText']))
    story.append(Spacer(1, 10))
    
    if 'top_3_crops' in data:
        story.append(Paragraph("Top 3 Recommended Crops:", styles['BodyText']))
        top_crops_data = [['Rank', 'Crop', 'Confidence']]
        for i, (crop, prob) in enumerate(data['top_3_crops'], 1):
            top_crops_data.append([f'#{i}', crop, f'{prob*100:.1f}%'])
        
        top_table = Table(top_crops_data, colWidths=[2*cm, 6*cm, 4*cm])
        top_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#66BB6A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#C8E6C9')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#DCEDC8')),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#F1F8E9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#A5D6A7')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(top_table)
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#C8E6C9')))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Generated by Precision Agriculture Platform - Smart Farming with ML", styles['Footer']))
    story.append(Paragraph("© 2024 All Rights Reserved", styles['Footer']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_fertilizer_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    styles = create_styles()
    story = []
    
    story.append(Paragraph("🧪 Fertilizer Recommendation Report", styles['MainTitle']))
    story.append(Paragraph(f"Crop: {data.get('crop', 'N/A')}", styles['SubTitle']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['SmallText']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4CAF50')))
    story.append(Spacer(1, 20))
    
    fert_type = data.get('fertilizer_type', 'Organic')
    story.append(Paragraph(f"📋 {fert_type} Fertilizer Schedule", styles['SectionHeader']))
    
    if 'schedule' in data:
        schedule_data = [['Growth Stage', 'Fertilizer', 'Application Rate', 'Method']]
        for stage, info in data['schedule'].items():
            schedule_data.append([
                stage,
                info.get('name', 'N/A'),
                info.get('rate', 'N/A'),
                info.get('method', 'N/A')
            ])
        
        table = Table(schedule_data, colWidths=[3*cm, 4*cm, 4*cm, 5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#81C784')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(table)
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#C8E6C9')))
    story.append(Paragraph("Generated by Precision Agriculture Platform", styles['Footer']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_multi_crop_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    styles = create_styles()
    story = []
    
    story.append(Paragraph("🌻 Multi-Cropping Plan Report", styles['MainTitle']))
    story.append(Paragraph(f"Main Crop: {data.get('main_crop', 'N/A')}", styles['SubTitle']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['SmallText']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4CAF50')))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("🌿 Companion Crops", styles['SectionHeader']))
    companions = data.get('companions', [])
    for comp in companions:
        story.append(Paragraph(f"• {comp}", styles['BodyText']))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("📏 Spacing Requirements", styles['SectionHeader']))
    spacing_data = [
        ['Crop Type', 'Spacing'],
        ['Main Crop', data.get('spacing_main', 'N/A')],
        ['Companion Crops', data.get('spacing_companion', 'N/A')],
    ]
    table = Table(spacing_data, colWidths=[5*cm, 8*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#66BB6A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#A5D6A7')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("✨ Benefits", styles['SectionHeader']))
    story.append(Paragraph(data.get('benefits', 'N/A'), styles['BodyText']))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("🚿 Irrigation Schedule", styles['SectionHeader']))
    story.append(Paragraph(data.get('irrigation', 'N/A'), styles['BodyText']))
    
    if 'yield_boost' in data:
        story.append(Spacer(1, 15))
        story.append(Paragraph("📈 Expected Yield Boost", styles['SectionHeader']))
        story.append(Paragraph(f"Expected yield increase: {data.get('yield_boost', 'N/A')}", styles['BodyText']))
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#C8E6C9')))
    story.append(Paragraph("Generated by Precision Agriculture Platform", styles['Footer']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_yield_prediction_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    styles = create_styles()
    story = []
    
    story.append(Paragraph("📊 Yield Prediction Report", styles['MainTitle']))
    story.append(Paragraph(f"Crop: {data.get('crop', 'N/A')}", styles['SubTitle']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['SmallText']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4CAF50')))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("🎯 Predicted Yield", styles['SectionHeader']))
    predicted = data.get('predicted_yield', 0)
    story.append(Paragraph(f"<b>{predicted} quintals per hectare</b>", styles['BodyText']))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("📋 Input Conditions", styles['SectionHeader']))
    input_data = [
        ['Parameter', 'Value'],
        ['Nitrogen', f"{data.get('nitrogen', 'N/A')} kg/ha"],
        ['Phosphorus', f"{data.get('phosphorus', 'N/A')} kg/ha"],
        ['Potassium', f"{data.get('potassium', 'N/A')} kg/ha"],
        ['Temperature', f"{data.get('temperature', 'N/A')}°C"],
        ['Humidity', f"{data.get('humidity', 'N/A')}%"],
        ['pH Level', f"{data.get('ph', 'N/A')}"],
        ['Soil Type', data.get('soil_type', 'N/A')],
        ['Season', data.get('season', 'N/A')],
    ]
    
    table = Table(input_data, colWidths=[5*cm, 6*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#81C784')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#C8E6C9')))
    story.append(Paragraph("Generated by Precision Agriculture Platform", styles['Footer']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_farm_overview_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    styles = create_styles()
    story = []
    
    story.append(Paragraph("📈 Farm Overview Report", styles['MainTitle']))
    story.append(Paragraph("Comprehensive Farm Analytics", styles['SubTitle']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles['SmallText']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4CAF50')))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("📊 Key Metrics", styles['SectionHeader']))
    
    metrics_data = [
        ['Metric', 'Value'],
        ['Total Crops Supported', data.get('total_crops', '300+')],
        ['Soil Types Analyzed', data.get('soil_types', '12')],
        ['ML Model Accuracy', data.get('accuracy', '99.77%')],
        ['Growing Seasons', data.get('seasons', '4')],
    ]
    
    table = Table(metrics_data, colWidths=[6*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#81C784')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(table)
    
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#C8E6C9')))
    story.append(Paragraph("Generated by Precision Agriculture Platform", styles['Footer']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
