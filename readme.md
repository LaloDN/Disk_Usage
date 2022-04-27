# Manual del script

## Módulos
+ argparse: Se utiliza para configurar los argumentos como el disco que se va a analizar o el porcentaje que se requiere para las alertas.
+ shutil: Se utiliza para mover los archivos de lugar.
+ json, request: Son utilizados para enviar la petición al bot de slack.
+ os: Es utilizado para operaciones con archivos y para ejecutar comandos de bash desde python.
## Main 
### Argparse

Dentro del main lo primero que se encuentra es la definición de los argumentos que se utiliza el script cuando se ejecuta

+ p_warning: Es un número flotante el cuál se va a comparar con el porcentaje en uso de un disco, si el porcentaje es mayor a este número se enviará una alerta a slack.
+ p_max: Es otro número flotante que también se va a comparar con el porcentaje en uso de un disco, pero si el porcentaje del disco es mayor al procentaje que nosotros introduzcamos, se va a iniciar un proceso para mover los archivos dentro del disco a una carpeta que le pasamos en los argumentos (nota: se recomienda que este valor sea mayor que el de p_warning para avisar con antelación de una posible limpieza de disco)
+ disk: El nombre del disco que queremos analizar.
+ backup: Contiene la ruta absoluta de la carpeta a la que queremos que se muevan los archivos del disco cuando el script detecte que se esta quedando sin espacio
+ n_warning: Es un número entero el cuál se va a comparar con el número de archivos de una carpeta para ver si se envía una alerta a slack.
+ folder: Es la ruta absoluta de una carpeta configurable para revisar la cantidad de archivos que hay dentro de ella.

Después de definir los argumentos del argparse viene una pequeña comprobación para ver si los argumentos están correctos (que los valores de los porcentajes esten dentro del rango de 1 a 100 y que el número de archivos a comparar con la carpeta sea mayor a 0).

Por último se hace la llamda a las funciones disk_usage y count_folder, pero antes de hacer la llamda a la función count_folder revisa si existe la carpeta que vamos a analizar en el sistema, si no existe imprime un mensaje de error y sale del programa. Después de esto el script termina su ejecución.

## slackMessage()

> Descripción: Envia un mensaje personalizado a un canal de slack con la ayuda de un bot.
> Párametros: recibe message, una cadena con el mensaje que se va a enviar al canal de slack.

Esta función recibe el mensaje que se quiere enviar por parámetro, dentro de la función crea un JSON con una única propiedad llamada text y como valor tendrá el mensaje que recibe por parámetro.
Por último hace un request de tipo post, para esta petición se le pasa la llave para utilizar el bot de slack y el JSON convertido a cadena con la función dumps.

## count_folder()

> Descripción: Cuenta el número de archivos que hay dentro de un directorio y envía un mensaje a slack.
> Parámetros: recibe folder, una cadena con el path hacía la carpeta que queremos monitorear y n_files, el número de archivos que necesita sobrepasar la carpeta para que envíe una alerta.

Lo primero que se hace es utilizar una funcione one liner para obtener el número total de archivos (sin contar los directorios) dentro de la carpeta que le especifiquemos de manera recursiva y guardarlo dentro de una variable.
Esta variable se va a comparar contra n_files, si el número de archivos dentro de la carpeta resulta ser mayor, entonces se va a enviar la alerta a slack con la función slackMessage, con la cantidad de archivos dentro de la carpeta.

## disk_usage()

> Descripción Revisa el porcentaje en uso de un disco y envia alertas o mueve los archivos a una carpeta de respaldo según sea el caso.

> Parámetros: recibe disk, una cadena con el nombre del disco montado en el sistema que se va a analizar, p_warning que es el porcentaje en uso del disco que se requiere para enviar una alerta a slack, p_max es el porcentaje en uso del disco que se necesita para empezar a mover TODOS los archivos dentro del disco a una carpeta de respaldo y backup_folder, la ruta con la carpeta en donde se hará el respaldo.

### Obtención del porcentaje
Para empezar a trabajar primero se necesita saber el porcentaje en uso del disco, para eso utilizamos el método os.popen para ejecutar un comando en bash en donde le pasamos el nombre del disco a revisar, se limpia el resultado de la ejecución del comando para extraer el porcentaje en uso y se guarda en una variable.
Nota: si no encuentra el disco lanzará un mensaje error y terminará con la ejecución del programa

### Mensaje de alerta
Después de obtener el procentaje en uso del disco que nos interesa, preguntamos con un if si el porcentaje es mayor o igual que el necesario para mandar una alerta a slack con el uso del disco, si esto se cumple, se manda a llamar a la función slackMessage para enviar la alerta con el bot.


### Proceso de mover archivos hacía el respaldo
Con otro if preguntamos si el procentaje en uso es mayor o igual al porcentaje que se necesita para que se empiecen a trasladar los archivos a otra carpeta. Si es así, lo primero que se hace es preguntar por seguridad si es que la carpeta donde se va a hacer el respaldo existe, si no existe, la crea y manda una notificación a slack con la función slackMessage diciendo que se creó la carpeta.

Lo siguiente es acceder a los archivos del disco, no se puede utilizar el comando os.listdir por que no es un directorio tal cual, por lo que aquí se vuelve a utilizar otro comando de bash para obtener la ruta en donde esta montado el disco (findmnt), se limpia el resultado que traiga la consulta de este comando para extraer la ruta absoluta del disco.

Una vez obtenida la ruta del disco, por seguridad se pregunta si se quiere continuar con el respaldo, se lee la entrada del usuario con un input y se va a continuar con el proceso solo si introduce una 'y' o 'Y', de lo contrario se terminará la función. Si se decide proceder, se envía un mensaje a slack de que se va a iniciar con un proceso de respaldo, con un for se trasladan los archivos y una vez que termina el proceso, se envía otro mensaje a slack informando que terminó el respaldo.

