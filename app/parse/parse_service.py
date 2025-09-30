from datetime import datetime, date
import re
from typing import Callable, Dict, List, Optional
import io
import pdfplumber
from app.common.types import Account, Movement

PdfPlumberTable = List[List[str | None]]

def extract_tables_from_pdf(file: bytes) -> List[PdfPlumberTable]:
    """Extrat trables from pdf file using pdf plumber

    Args:
        file (bytes): File in bytes

    Returns:
        List[PdfPlumberTable]: List Of PdfPlumber tables
    """
    pdf = pdfplumber.open(io.BytesIO(file))
    return [t for page in pdf.pages for t in page.extract_tables()]

def parse_davivienda(
        movement: List[str | None], 
        total_movements: int,
        year: Optional[int] = None
    ) -> Movement | None:
    """Parse a davivienda statement pdf

    Args:
        movement (List[str | None]): A raw movement 
        total_movements (int): Current total movements 
        year (int): Optional. Current year  

    Returns:
        Movement | None: Movement 
    """
    # If row is empty, then ignore it 
    if movement[0] is None or movement[0] == "" or len(movement[0]) != 2: return None

    # If it's a pokect movement, then ignore it  
    if re.match(".*Bolsillo.*", str(movement[4])): return None

    day = int(str(movement[0]))
    month = int(str(movement[1]))
    year = year if year else datetime.now().year

    # Normalize the descriptions (for some reason, some descriptions does not have spaces)
    description = re.sub(r'([a-z])([A-Z])', r'\1 \2',  str(movement[4])) 

    sign = str(movement[2])[-1]
    str_amount =  str(movement[2])[:-1]\
        .replace(",","")\
        .replace(" ", "")\
        .replace("$", "")

    amount = float(sign + str_amount)

    return Movement(
        id = f"DAVI{month}{total_movements:03}",
        ref = None,
        account = Account.DAVIVIENDA,
        date = date(year, month, day),
        amount = amount,
        description = description,
    )
            
ParserFunction = Callable[
    [List[str | None], int, Optional[int] | None], 
    Optional[Movement]
]

parses: Dict[Account, Optional[ParserFunction]] = {
    Account.DAVIVIENDA: parse_davivienda,
    Account.LULO: None,
    Account.NEQUI: None,
}

def parse(account: Account, file: bytes) -> List[Movement]:
    """Given an account and a file in bytes, parse the pdf

    Args:
        account (Account): Account 
        file (bytes): File in bytes

    Raises:
        KeyError: _description_

    Returns:
        List[Movement]: List of parsed movements
    """
    parser = parses[account]
    if parser is None: raise KeyError()
    
    movements: List[Movement] = []

    tables = extract_tables_from_pdf(file)
    for table in tables: 
        for row in table: 
            movement = parser(row, len(movements), None)
            if movement: movements.append(movement)
  
    return movements
