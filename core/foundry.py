import os
from pathlib import Path
from typing import Any, Dict
from docxtpl import DocxTemplate
from fillpdf import fillpdfs

class AxonFoundry:
    """
    Document generation engine for Axon.
    Handles rendering DOCX and PDF templates with dynamic context.
    """

    def __init__(self, base_dir: str = "."):
        """
        Initializes the AxonFoundry with relative or absolute base paths.
        
        Args:
            base_dir: The project's root directory. Defaults to current directory.
        """
        self.root = Path(base_dir).resolve()
        self.docx_dir = self.root / "templates" / "docx"
        self.pdf_dir = self.root / "templates" / "pdf"
        self.output_dir = self.root / "outputs"

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_docx(self, template_filename: str, context: Dict[str, Any], output_filename: str) -> str:
        """
        Renders a DOCX template with the provided context and saves it to the outputs folder.

        Args:
            template_filename: Name of the .docx file in templates/docx/
            context: Key-value pairs to populate the Jinja2 tags in the template.
            output_filename: The name for the generated file.

        Returns:
            The absolute string path to the generated file.
        """
        template_path = self.docx_dir / template_filename
        
        if not template_path.exists():
            raise FileNotFoundError(f"DOCX template not found at {template_path}")

        doc = DocxTemplate(str(template_path))
        doc.render(context)
        
        output_path = self.output_dir / output_filename
        doc.save(str(output_path))
        
        return str(output_path.resolve())

    def generate_pdf(self, template_filename: str, context: Dict[str, Any], output_filename: str) -> str:
        """
        Placeholder for filling PDF forms using fillpdf.
        
        Args:
            template_filename: Name of the .pdf file in templates/pdf/
            context: Data to fill into the PDF form fields.
            output_filename: The name for the generated file.
            
        Returns:
            The absolute string path to the generated file.
        """
        template_path = self.pdf_dir / template_filename
        
        if not template_path.exists():
            raise FileNotFoundError(f"PDF template not found at {template_path}")

        output_path = self.output_dir / output_filename
        
        # fillpdf.fillpdfs.write_fillable_pdf fills a form and produces a new PDF
        # Note: If the form is not flattened, it remains editable.
        fillpdfs.write_fillable_pdf(str(template_path), str(output_path), context)
        
        return str(output_path.resolve())
