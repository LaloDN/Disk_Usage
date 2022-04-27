import os
import argparse
import shutil

def main():
    parser = argparse.ArgumentParser(description='Script para renombrar archivos con extension .csv y moverlos a otra carpeta')
    parser.add_argument('--directorio_obj',type=str,help='Ruta absoluta del directorio con los archivos csv que vamos a manipular')
    parser.add_argument('--directorio_des',type=str,help='Ruta absoluta del directorio a donde se van a mover los nuevos archivos .csv')
    args = parser.parse_args()

    for file in os.listdir(args.directorio_obj):
        if file.endswith('.csv_d') or file.endswith('.csv_t'):
            file_name=file.split('.')[0]
            new_name=os.path.join(args.directorio_obj,file_name+'.csv')
            os.rename(os.path.join(args.directorio_obj,file),new_name)
            try:
                shutil.move(new_name,args.directorio_des)
            except Exception as e:
                print('Error: '+str(e))
        if file.endswith('.csv'):
            try:
                shutil.move(os.path.join(args.directorio_obj,file),args.directorio_des)
            except Exception as e:
                print('Error '+str(e))
        
    
if __name__=='__main__':
    main()