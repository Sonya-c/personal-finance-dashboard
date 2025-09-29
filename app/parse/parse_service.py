from typing import Callable, Dict, Any, List
import io
import pdfplumber
from app.types import Account

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

def parse_davivienda(tables: List[PdfPlumberTable]):
    """Parse a davivienda statement pdf

    Args:
        tables (List[PdfPlumberTable]): List of pdf tables 

    Returns:
        _type_: _description_
    """
    return tables 


parses: Dict[Account, Callable[[List[PdfPlumberTable]], Any] | None] = {
    Account.DAVIVIENDA: parse_davivienda,
    Account.LULO: None,
    Account.NEQUI: None,
}

def parse(account: Account, file: bytes):
    """Given an account and a file in bytes, parse the pdf

    Args:
        account (Account): Account 
        file (bytes): File in bytes

    Raises:
        KeyError: _description_

    Returns:
        _type_: _description_
    """
    parser = parses[account]
    if parser is None: raise KeyError()
    
    pdf = extract_tables_from_pdf(file)
    return parser(pdf)
