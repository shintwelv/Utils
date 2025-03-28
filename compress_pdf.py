import subprocess
import os

def compress_pdf(input_path, output_path, quality='screen'):
    """
    압축 품질 옵션:
    - screen: 저해상도 (가장 작음)
    - ebook: 중간 해상도
    - printer: 고해상도
    - prepress: 매우 고해상도
    """
    try:
        subprocess.run([
            "gs",  # 윈도우에서는 "gswin64c" 일 수도 있음
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{quality}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path
        ], check=True)
        print(f"압축 완료: {output_path}")
    except Exception as e:
        print(f"오류 발생: {e}")

# 사용 예시
compress_pdf("/Users/shinil/Downloads/HowrahScholarship_ko.pdf", "/Users/shinil/Downloads/HowrahScholarship_ko_comp.pdf", quality="ebook")