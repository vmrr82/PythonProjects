import qrcode
import qrcode.constants

# Ruta de la imagen


def qrcreator():
    url = "https://www.adayo-pbo.es/apoyo-las-familias/#"
         
            # Crear el objeto QRCode
    qr = qrcode.QRCode(version=1, 
                       box_size=10, 
                       border=5,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)  # Añadir los datos al QR
    qr.make(fit=True)  # Asegurarse de que el tamaño se ajusta

            # Crear la imagen QR y guardarla
    img = qr.make_image(fill_color='#6495ED', back_color='white')
    img.save('logo.png')  # Guardar como archivo PNG

qrcreator()
