import markdown2
from schemas import TravelItinerary

# Try to import PDF libraries
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: PDF export not available. Install reportlab to enable PDF export.")

def format_itinerary_to_markdown(itinerary: TravelItinerary) -> str:
    """
    Converts a TravelItinerary Pydantic model into a formatted Markdown string.
    """
    md = f"# {itinerary.title}\n\n"
    
    # Trip Summary
    md += f"**Destination:** {itinerary.request.destination}  \n"
    md += f"**Duration:** {itinerary.request.duration_days} Days  \n"
    md += f"**Travelers:** {itinerary.request.travelers}  \n"
    md += f"**Budget:** {itinerary.request.budget}  \n"
    md += f"**Interests:** {', '.join(itinerary.request.interests)}\n\n"
    
    md += "## Trip Overview\n"
    md += f"{itinerary.summary}\n\n"
    
    md += "## Total Estimated Cost\n"
    md += f"{itinerary.total_estimated_cost or 'Not specified'}\n\n"
    
    md += "## Daily Itinerary\n"
    
    for day in itinerary.days:
        date_str = f" ({day.date})" if day.date else ""
        md += f"### Day {day.day_number}{date_str}\n"
        
        md += f"**🌅 Morning:**\n{day.morning_activity}\n\n"
        md += f"**☀️ Afternoon:**\n{day.afternoon_activity}\n\n"
        md += f"**🌙 Evening:**\n{day.evening_activity}\n\n"
        
        if day.accommodation:
            md += f"**🏨 Accommodation:** {day.accommodation}\n\n"
            
        md += "---\n\n"
        
    return md

def export_to_pdf(markdown_content: str, output_path: str):
    """
    Converts markdown content to a PDF file using reportlab.
    """
    if not PDF_AVAILABLE:
        print("Error: PDF export requires reportlab. Install with: pip install reportlab")
        return False
    
    try:
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='green',
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Parse markdown and convert to PDF elements
        lines = markdown_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.2*inch))
                continue
            
            # Handle headers
            if line.startswith('# '):
                story.append(Paragraph(line[2:], title_style))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], styles['Heading2']))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['Heading3']))
            elif line.startswith('**') and line.endswith('**'):
                story.append(Paragraph(line, styles['Heading4']))
            elif line.startswith('---'):
                story.append(Spacer(1, 0.3*inch))
            else:
                story.append(Paragraph(line, styles['BodyText']))
        
        # Build PDF
        doc.build(story)
        return True
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False
