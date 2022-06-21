import argparse
import shutil
import json
import requests
import os

def slackMessage(message: str) -> None:
    """Función para enviar un mensaje a un canal de slack mediante webhooks-"""
    data={
        "text": message
    }
    requests.post('YOUR_SLACK_HOOK',json.dumps(data))

def disk_usage(disk: str,p_warning: float, p_max:float, backup_folder: str)->None:
    """Función para revisar el porcentaje de un disco en uso y mandar alertas """
    try:    
        result=os.popen("df -h | grep "+disk).readlines()[0]
        percentage=float(result.split()[-2][:-1])
    except:
        print('Error: no se ha encontrado el disco',disk)
        quit()
        
    if percentage>=p_warning:
        message='Advertencia: el disco '+disk+' está al '+str(round(percentage,2))+'% de su uso'
        slackMessage(message)
    
    if percentage>=p_max:
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
            message='Advertencia: la ruta '+backup_folder+' no existia dentro del sistema, se ha creado con éxito.'
            slackMessage(message)
           
        #Ruta de montado del disco 
        result=os.popen("findmnt -S "+disk).readlines()[1]
        disk_path=result.split()[0]
        
        confirmation=input('¿Está seguro de que quiere mover los archivos del disco '+disk+' hacía la carpeta '+backup_folder+'?\n(y,n)')
        if confirmation=='y' or confirmation=='Y':
            message='[SE HA INICADO UN PROCESO DE MOVER ARCHIVOS] Disco: '+disk+' Carpeta de destino: '+backup_folder
            slackMessage(message)
            for file in os.listdir(disk_path):
                    shutil.move(os.path.join(disk_path,file),backup_folder)
            slackMessage('¡Se ha completado una operación de traslado de archivos con éxito!')
            
def count_folder(folder: str, n_files: int)->None:
    """Función para contar el número de arcivos de un directorio y enviar un mensaje de alerta"""
    folder_files=sum([len(files) for r, d, files in os.walk(folder)])
    if folder_files>n_files:
        message='Advertencia: la carpeta '+folder+' ha sobrepasado los '+str(n_files)+' archivos ('+str(folder_files)+' archivos en total)'
        slackMessage(message)

def main():
    
    parse=argparse.ArgumentParser(description='Script para monitorear el almacenamiento de un disco')
    parse.add_argument('--p_warning',type=float,help='Porcentaje en uso de un disco que se necesita para enviar la notifiación a slack')
    parse.add_argument('--p_max',type=float,help='Porcentaje en uso de un disco que se necesita para empezar a mover los archivos a otra carpeta de respaldo')
    parse.add_argument('--disk',type=str,help='Disco que se va a monitorear')
    parse.add_argument('--backup',type=str,help='Ruta absoluta del directorio en donde se va a hacer el respaldo')
    parse.add_argument('--n_warning',type=int,help='Número de archivos en un disco que se requieren para que se envie la notificación a slack')
    parse.add_argument('--folder',type=str,help='Carpeta configurable para monitorear')
    args=parse.parse_args()
    
    if args.p_warning not in (1,100) or args.p_max not in (1,100) or args.n_warning<=0:
        print('Error: alguno de los parámetros de porcentaje (1-100) o de número de archivos (mayor que 0) son inválidos')
        quit()
    
    disk_usage(args.disk,args.p_warning,args.p_max,args.backup)
    if not os.path.exists(args.folder):
        print('Error: la carpeta',args.folder,'no existe dentro del sistema')
        quit()
    count_folder(args.folder,args.n_warning)
    
if __name__ == '__main__':
    main()
