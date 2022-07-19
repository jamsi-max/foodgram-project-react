import io

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def get_shopping_list_pdf(basket_ingredients):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('Montserrat', 'Montserrat.ttf'))

        # header
        p.setFillColorRGB(.255, .230, .238)
        p.rect(0, 800, 652, 50, fill=1)

        p.setFont('Montserrat', 14)
        p.setFillColorRGB(1, 1, 1)
        # header end

        # footer
        p.setFillColorRGB(.255, .230, .238)
        p.rect(0, 0, 652, 50, fill=1)

        p.setFont('Montserrat', 14)
        p.setFillColorRGB(1, 1, 1)
        p.drawString(40, 20, 'Продуктовый помощник')
        p.drawString(300, 20, 'Разработан: https://t.me/Jony2024')
        # footer end

        # ingridients list
        p.setFont('Montserrat', 22)
        p.setFillColorRGB(1, 1, 1)
        p.drawString(100, 815, 'Список покупок:')
        p.setFont('Montserrat', 14)
        step = 750
        p.setFillColorRGB(0, 0, 0)
        for ingredient in basket_ingredients:
            p.drawString(
                125,
                step,
                f'- {ingredient["ingredient__name"]} - \
{ingredient["amount"]} {ingredient["ingredient__measurement_unit"]};')
            step -= 25
            p.line(125, step + 15, 500, step + 15)
        # end ingridients list

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping-list.pdf'
        )