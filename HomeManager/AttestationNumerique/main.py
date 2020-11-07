from PyPDF2 import PdfFileWriter, PdfFileReader
import qrcode
import datetime
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from datetime import date
import argparse

from django.conf import settings
import os.path

script_dir = os.path.dirname(os.path.abspath(__file__))
 

def image_croix():
    image = Image.new('RGB', (30, 30), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    image_font = ImageFont.truetype("Arial.ttf", 35)
    image_draw.text((3, -4), f'X', (0, 0, 0), font=image_font)
    return np.array(image)


def GenererUneAttestation(moi):

  img = Image.open(os.path.join(script_dir, 'input-page1.png')).convert('RGB')
  img_array = np.array(img)
  cross = image_croix()
  moi.motif = "sport"
  if "travail" in moi.motif:
      img_array[527:557, 155:185] = cross
  if "courses" in moi.motif:
      img_array[620:650, 155:185] = cross
  if "sante" in moi.motif:
      img_array[738:768, 155:185] = cross
  if "famille" in moi.motif:
      img_array[822:852, 155:185] = cross
  if "sport" in moi.motif:
      img_array[987:1017, 155:185] = cross

  # QR CODE
  qr_text = f"Cree le: {datetime.datetime.now().strftime('%d/%m/%Y a %H:%M')};" \
            f" Nom: {moi.nom};" \
            f" Prenom: {moi.prenom};" \
            f" Naissance: {moi.dateNaissance} a {moi.villeNaissance};" \
            f" Adresse: {moi.adressePostal};" \
            f" Sortie: {moi.dateSortie} a {moi.heureSortie};" \
            f" Motifs: {moi.motif}"

  # qr_text="hyduzqhdzoiqd zqoihdpodqz"
  qr = qrcode.make(qr_text, border=0)
  qr = qr.resize((200, 200))
  qr = np.array(qr).astype(np.uint8) * 255
  qr = qr.repeat(3).reshape(qr.shape[0], qr.shape[1], -1)

  img_array[1328:1528, 890:1090] = np.array(qr)
  img = Image.fromarray(img_array)

  # Fill args
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("Arial.ttf", 22)
  font_small = ImageFont.truetype("Arial.ttf", 14)
  draw.text((260, 285), f'{moi.prenom} {moi.nom}', (0, 0, 0), font=font)
  draw.text((255, 332), f'{moi.dateNaissance}', (0, 0, 0), font=font)
  draw.text((620, 332), f"{moi.villeNaissance}", (0, 0, 0), font=font)
  draw.text((285, 377), f"{moi.adressePostal}", (0, 0, 0), font=font)

  draw.text((228, 1370), f"{moi.villeActuel}", (0, 0, 0), font=font)
  draw.text((190, 1418), datetime.datetime.now().strftime("%d/%m/%Y"), (0, 0, 0), font=font)
  draw.text((530, 1418), datetime.datetime.now().strftime("%H:%M"), (0, 0, 0), font=font)

  #draw.text((948, 1443), datetime.datetime.now().strftime("%d/%m/%Y à %H:%M"), (0, 0, 0), font=font_small)

  plt.imsave(os.path.join(script_dir, "output-1.pdf"), np.array(img), format="pdf")

  # ---------------------------
  #  Second Page (Big QR code)
  # ---------------------------
  img = np.array(Image.open(os.path.join(script_dir, 'input-page2.png')))
  img[:] = 255
  qr = Image.fromarray(qr)
  qr = qr.resize((qr.size[0] * 3, qr.size[1] * 3))
  qr = np.array(qr)
  img[113:113 + qr.shape[0], 113:113 + qr.shape[1]] = qr
  plt.imsave(os.path.join(script_dir, "output-2.pdf"), img, format="pdf")

  # --------------------
  # Merge PDFs
  # --------------------
  pdf1 = PdfFileReader(os.path.join(script_dir, 'output-1.pdf'))
  pdf2 = PdfFileReader(os.path.join(script_dir, 'output-2.pdf'))
  writer = PdfFileWriter()
  writer.addPage(pdf1.getPage(0))
  writer.addPage(pdf2.getPage(0))
  writer.write(open(os.path.join(script_dir, "output.pdf"), "wb"))

  return os.path.join(script_dir, "output.pdf")
