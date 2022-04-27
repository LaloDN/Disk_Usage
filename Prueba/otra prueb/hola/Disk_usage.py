import argparse
import shutil
import json
import requests
import math

def slackMessage(message: str) -> None:
    """Función para enviar un mensaje con los errores de la ejecución a un canal de slack mediante webhooks-"""
    data={
        "text": message
    }
    requests.post('https://hooks.slack.com/services/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',json.dumps(data))


def disk_usage(disk: str,p_warning: float, p_max:float, backup_folder: str)->int:
    total,used,free=shutil.disk_usage(disk)
    percentage=free/total*100
    if percentage>=p_max:
        message='[SE HA INICADO UN PROCESO DE MOVER ARCHIVOS] Disco: ',disk,' Carpeta de destino: ',backup_folder
        slackMessage(message)
    elif percentage>=p_warning:
        message='Advertencia: el disco ',disk, 'está al ' ,str(round(percentage,2)),'% de su uso'
        slackMessage(message)

def main():
    parse=argparse.ArgumentParser(description='Script para monitorear el almacenamiento de un disco')
    parse.add_argument('--p_warning',type=float,help='Porcentaje en uso de un disco que se necesita para enviar la notifiación a slack')
    parse.add_argument('--n_warning',type=int,help='Número de archivos en un disco que se requieren para que se envie la notificación a slack')
    parse.add_argument('--p_max',type=float,help='Porcentaje en uso de un disco que se necesita para empezar a mover los archivos a otra carpeta de respaldo')
    parse.add_argument('--disk',type=str,help='Disco que se va a monitorear')
    parse.add_argument('--folder',type=str,help='Carpeta configurable para monitorear')
    parse.add_argument('--backup',type=str,help='Ruta absoluta del directorio en donde se va a hacer el respaldo')
    args=parse.parse_args()
    

if __name__ == '__main__':
    main()