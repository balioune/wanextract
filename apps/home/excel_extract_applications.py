import json
from django.db.models import Q
from django.http import HttpResponse
from apps.home.models import *
import xlwt
from xlwt import *

# Excel Conf
COL_WIDTH = 150 * 50

front_style = xlwt.XFStyle()
al = xlwt.Alignment()
al.horz = xlwt.Alignment().HORZ_CENTER
al.vert = xlwt.Alignment().VERT_CENTER
front_style.alignment = al
front_style.font.bold = True
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['white']
front_style.pattern = pattern

fnt = Font()
fnt.name = 'Arial'
fnt.bold = True

borders = Borders()
borders.left = 6
borders.right = 6
borders.top = 6
borders.bottom = 6

alignment = Alignment()
alignment.horz = Alignment.HORZ_CENTER
alignment.vert = Alignment.VERT_CENTER

style = XFStyle()
style.font = fnt
style.borders = borders
style.alignment = alignment


def extract_total_octets_per_site(datetime_from, datetime_to):
    response = HttpResponse(content_type='application/ms-excel')
    filename = "TotalOctectperSite.xls"
    response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename

    center_style = xlwt.easyxf("align: vert centre, horiz centre")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('OctetsPerSite', True)
    columns = ['PROVIDER', 'SITE NAME', 'RxOctets', 'TxOctets', 'TotalOctets',]

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], style)
        ws.col(col_num).width = COL_WIDTH

    ws.write_merge(1, 1, 0, 7, 'Extract Total Octets per Site from {} to {}'.format(str(datetime_from), str(datetime_to)), style)

    row_num = 2
    for site in []:
        ws.write(row_num, 0, str(site), center_style)
        ws.write(row_num, 1, '', center_style)
        row_num += 1

    wb.save(response)
    return response
