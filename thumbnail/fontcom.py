from PIL import ImageFont, ImageDraw, Image



def fontcom(position,width):
    defont = './font/'

    font_path1 = defont + 'RiiPopkkR.otf'
    font_path2 = defont + 'Kaiso-Next-B.otf'
    font_path3 = defont + 'AoyagiSosekiFont2.otf'
    font_path4 = defont + 'font_1_kokugl_1.15_rls.ttf'
    font_path5 = defont + 'KS-Kohichi-FeltPen.ttf'
    font_path6 = defont + 'ラノベPOP.otf'
    font_path7 = defont + 'keifont.ttf'
    font_path = font_path7
    font_size = int(width * (1/11))

    fil = './comm/'
    com1 = "shikou.png"
    com2 = "yurucom.png"
    com3 = "husen.png"
    com4 = "hukidashi1.png"
    com5 = "kyouchou.png"
    com6 = "kakukaku.png"
    com7 = "yokonaga.png"
    com = Image.open(fil + com6)

    return font_path,font_size,com
