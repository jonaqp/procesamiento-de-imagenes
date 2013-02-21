morris=morris.dat
boyer=boyer.dat

##para ver si existen los archivos
##si es asi los borra
##agradecimiento a pedrito por 
##esta parte de archivos
 
if [ -e $morris ]; then
	rm morris.dat
fi
if [ -e $boyer ]; then
	rm boyer.dat
fi
 
 
touch morris.dat
touch boyer.dat
##no delcaramos mas varaibles ya que no ase falta
## la varaible dentro del for toma los valores despues de in
## en cada regreso
 
for PATRONES in 0 1 2 3 4 5 6 7 8 ##los valores de las potencia de dos
do
	for TEXTO in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 ##frecuencia de cero
	do
		for PECERO in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 ##posibilidades de exito cero y uno
		do
			for CONTADOR in 1 2 3 4 5 ##Repetición del experimento
			do
		        touch mugre.dat
				res=`python canal.py $TEXTO $PATRONES $PECERO $PECERO $REPE` ##porcentaje de exito con python
		        echo $res >> mugre.dat
			done
			res=`awk -f cosa.awk mugre.dat` ##promedio del experimiento de arriba
			echo valor de res $res
			rm mugre.dat
			echo $PATRONES $TEXTO $PECERO $res >> canal.dat ##pasamos datos al archivo final
			echo $res >> desviacion.dat
		done
	done
	echo '' >> canal.dat ##si no ponemos esto a gnuplot no le gusta para poder graficarlo con colores
	echo $PATRONES
done
python desviacion.py ##para la desviacion de los datos finales de porcentaje de exito
gnuplot grafica.plot ##crear la imagen de la grafica