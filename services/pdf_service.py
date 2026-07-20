import os
import subprocess


SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"


def office_to_pdf(input_path: str):

    output_dir = os.path.dirname(input_path)

    subprocess.run(
        [
            SOFFICE_PATH,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            output_dir,
            input_path
        ],
        check=True
    )

    pdf_name = os.path.splitext(
        os.path.basename(input_path)
    )[0] + ".pdf"

    return os.path.join(output_dir, pdf_name)