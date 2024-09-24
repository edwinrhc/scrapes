from pprint import pprint
import re


title = '''Innovative Sysco Imperial 2-ply bath tissue refills ensure 99% roll usage before changeouts are needed, which can virtually eliminate waste and minimize the frequency of changeouts. These refills are compatible with our popular and efficient Complete®360 bath tissue dispensers.

• Contains 12 Coreless Toilet Paper Rolls, Totaling 20,400 Sheets per Case
• Toilet Paper Ply: 2-Ply
• Roll Type: Perforated
• Roll Dimensions: 3.25" W x 4.05" L
• Sheets per Roll: 1,700
• Suggested Usage Areas: Restroom
• Storage Handling: 73°F - 100°F
• Handling Instructions: Avoid excessive heat or cold
• Case Dimensions: 12.25" L x 18.37" W x 6.50" H 
• Compatible Dispensers: SUPC 4527970 & SUPC 4806190
• High-capacity, easy-tear rolls (3.25" x 4.05") help to control usage and reduce waste
• Efficient 2-ply coreless rolls allow 99% bath tissue usage, virtually eliminating stub-roll waste
• 12 rolls per case can create storage efficiencies to free up space in BOH
• Poly-wrapped cases help reduce overall storage footprint, protect the product, and reduce waste since there is no wrapper or corrugate 
• Compatible with Complete®360 2-Roll (4806190) and 4-Roll (4527970) Coreless Toilet Paper Dispensers
• COMPLETE®360 is our coordinated line of towel, tissue, and napkin dispensers with high-quality refills and disposables for restroom, FOH, and BOH settings. The sleek and reliable C360 portfolio is well known for helping operators prioritize hygiene, staff productivity, and guest experience.'''

pattern = r'(?:sheets\sper\sroll\s?:?\s?([\d,]+)|rolls\sof\s([\d,]+)\ssheets)'

def get_match_from_text(text, pattern):
    
    text = text.lower()
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_num_from_text(raw_text):
    
    num = ''
    if raw_text:
        num_regex = r'\d+(\.\d+)?'
        clean_txt = re.search(num_regex, raw_text)
        if clean_txt:
            num = clean_txt.group(0)
    
    return num


print(extract_num_from_text(get_match_from_text(title, pattern).replace(',', '')))