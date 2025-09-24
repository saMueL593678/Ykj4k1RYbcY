# 代码生成时间: 2025-09-24 12:37:40
# document_converter.py
# A Falcon-based application that converts document formats.

from falcon import Falcon, Request, Response
import os
import logging
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
import uno
from com.sun.star.uno import XComponentContext
from com.sun.star.frame import XComponentLoader, loadComponentFromURL
from com.sun.star.awt import Rectangle
from com.sun.star.util import XCloseable

# Set up logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define constants for the paths to OpenOffice and the input/output directories.
OPENOFFICE_PATH = r"C:\Program Files (x86)\OpenOffice 4\program\soffice.exe"
INPUT_DIR = r"input"
OUTPUT_DIR = r"output"


class DocumentConverter:
    """Class responsible for document conversion functionality."""
    def __init__(self):
        self.ctx = None
        self.desktop = None

    def initialize(self):
        # Initialize OpenOffice connection.
        self.ctx = uno.getComponentContext()
        self.desktop = loadComponentFromURL(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext",
            "localhost",
            self.ctx,
            [ "-single -accept=socket,host=localhost,port=2002;urp; -norestore -nodefault -nolockcheck -calc -headless -wait" ]
        )

    def convert_to_pdf(self, source_file_path):
        """Converts a document to PDF format."""
        if not os.path.exists(source_file_path):
            logger.error(f"File not found: {source_file_path}")
            raise FileNotFoundError(
                f"The source file {source_file_path} does not exist."
            )

        # Load the document.
        doc = self.desktop.loadComponentFromURL(
            source_file_path,
            "_blank", 0, {}
        )

        # Get the XWriterDocument interface.
        writer_doc = uno.cast(uno.getTypeByName(
            "com.sun.star.text.XTextDocument"), doc)

        # Save the document as a PDF.
        writer_doc.storeAsURL(
            os.path.join(OUTPUT_DIR, os.path.basename(source_file_path) + ".pdf\)
        )

        # Close the document.
        writer_doc.getController().getViewData().getDispatcher().
            executeDispatch(
                writer_doc.getFrame(),
                ".uno:CloseDoc", 0, 0, uno.Any(), []
            )

    def convert_to_docx(self, source_file_path):
        """Converts a document to DOCX format."""
        if not os.path.exists(source_file_path):
            logger.error(f"File not found: {source_file_path}")
            raise FileNotFoundError(
                f"The source file {source_file_path} does not exist."
            )

        # Create a new DOCX document.
        doc = Document()

        # Add a paragraph to the document.
        p = doc.add_paragraph("Converted from non-DOCX format.\)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Save the document.
        doc.save(os.path.join(OUTPUT_DIR, os.path.basename(source_file_path) + ".docx\))

class ConverterResource:
    """Falcon resource for document conversion."""
    def __init__(self):
        self.converter = DocumentConverter()
        self.converter.initialize()

    def on_get(self, req: Request, resp: Response):
        """Handles GET requests to convert documents."""
        source_file_path = req.params.get("file\)

        if not source_file_path:
            resp.status = falcon.HTTP_400
            resp.body = "Missing 'file' parameter."
            return

        try:
            if req.params.get("format\) == "pdf":
                self.converter.convert_to_pdf(source_file_path)
            elif req.params.get("format\) == "docx":
                self.converter.convert_to_docx(source_file_path)
            else:
                raise ValueError("Unsupported format.\)

            resp.status = falcon.HTTP_200
            resp.body = "Conversion successful."
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = str(e)

# Create the Falcon API application.
app = Falcon()

# Add the converter resource.
converter_resource = ConverterResource()
app.add_route("/convert", converter_resource)

# Run the application.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)