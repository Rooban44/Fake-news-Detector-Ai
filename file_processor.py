"""
File Processing Module
Handles text extraction from images, PDFs, and text files
"""
import os
import io
from PIL import Image
import pytesseract
import PyPDF2


class FileProcessor:
    """Process uploaded files and extract text"""
    
    def __init__(self):
        # Set tesseract path for Windows (adjust if needed)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def process_file(self, file_data, filename):
        """
        Process uploaded file and extract text
        
        Args:
            file_data: File binary data
            filename: Name of the file
            
        Returns:
            dict: Extracted text and metadata
        """
        file_ext = os.path.splitext(filename)[1].lower()
        
        try:
            if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                return self._extract_from_image(file_data, filename)
            elif file_ext == '.pdf':
                return self._extract_from_pdf(file_data, filename)
            elif file_ext == '.txt':
                return self._extract_from_text(file_data, filename)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {file_ext}. Supported: .jpg, .png, .pdf, .txt'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing file: {str(e)}'
            }
    
    def _extract_from_image(self, file_data, filename):
        """Extract text from image using OCR"""
        try:
            # Try to use pytesseract if available
            try:
                image = Image.open(io.BytesIO(file_data))
                text = pytesseract.image_to_string(image)
                
                if not text.strip():
                    return {
                        'success': False,
                        'error': 'No text found in image. Please ensure the image contains readable text.'
                    }
                
                return {
                    'success': True,
                    'text': text,
                    'source': filename,
                    'type': 'image'
                }
            except Exception as ocr_error:
                # Tesseract not installed - provide helpful error
                return {
                    'success': False,
                    'error': 'OCR not available. To enable image text extraction, install Tesseract OCR.',
                    'help': 'For now, please copy and paste the text manually or upload a PDF/text file.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error reading image: {str(e)}'
            }
    
    def _extract_from_pdf(self, file_data, filename):
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
            
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            
            if not text.strip():
                return {
                    'success': False,
                    'error': 'No text found in PDF. The PDF might be scanned or image-based.'
                }
            
            return {
                'success': True,
                'text': text,
                'source': filename,
                'type': 'pdf',
                'pages': len(pdf_reader.pages)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error reading PDF: {str(e)}'
            }
    
    def _extract_from_text(self, file_data, filename):
        """Extract text from text file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    text = file_data.decode(encoding)
                    return {
                        'success': True,
                        'text': text,
                        'source': filename,
                        'type': 'text'
                    }
                except UnicodeDecodeError:
                    continue
            
            return {
                'success': False,
                'error': 'Unable to decode text file. Please ensure it uses UTF-8 encoding.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error reading text file: {str(e)}'
            }
