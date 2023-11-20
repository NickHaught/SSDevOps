import pypdfium2 as pdfium
from PIL import Image

pdf = pdfium.PdfDocument("images/Hebron_1960.pdf")
#n_pages = len(pdf)
# Access the first page (index 0)
page = pdf.get_page(0)

# Render the page to a bitmap
bitmap = pdfium.PdfPage.render(page, scale = 4)

# Convert the bitmap to a PIL image
pil_image = Image.frombytes("RGB", (bitmap.width, bitmap.height), bitmap.buffer)

# Save the PIL image as a JPEG
pil_image.save("output.jpg")

# Close the PDF document
pdf.close()
# for page_number in range(n_pages):
#     page = pdf.get_page(page_number)
#     pil_image = page.render_topil(
#         scale=1,
#         rotation=0,
#         crop=(0, 0, 0, 0),
#         colour=(255, 255, 255, 255),
#         annotations=True,
#         greyscale=False,
#         optimise_mode=pdfium.OptimiseMode.NONE,
#     )
#     pil_image.save(f"image_{page_number+1}.png")