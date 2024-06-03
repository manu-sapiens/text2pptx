import aspose.slides as slides

def convert_pptx_to_pdf(input_file: str, output_file: str):
    """
    Convert a PPTX file to a PDF file.

    :param input_file: Path to the input PPTX file.
    :param output_file: Path where the output PDF file will be saved.
    """
    with slides.Presentation(input_file) as presentation:
        presentation.save(output_file, slides.export.SaveFormat.PDF)

# Example usage
# convert_pptx_to_pdf("presentation.pptx", "presentation.pdf")
