En pi�ce jointe tu trouveras le code Python3 (c�est un fichier texte que tu peux lire avec notepad ou Word ou tout autre �diteur de textes) et la photo du branchement du MPU6050.
 
En gros, fil rouge sur VCC du MPU6050 va sur pin 1 (3.3V) du Raspberry Pi.  Fil noir sur GND du MPU6050 va sur pin 6 (GND) du RPi.  Fil vert sur SDA du MPU6050 va sur pin 3 (SDA) du RPi.  Fil blanc sur SCL du MPU6050 va sur pin 5 (SCL) du RPi.  Pour ma part, j�ai branch� mon fil gris sur INT du MPU6050.  Ce fil est pour une am�lioration future. Pr�sentement, il n�est pas branch� au Raspberry Pi.
