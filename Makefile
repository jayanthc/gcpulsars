all:
	gcc -Wall -std=c99 -pedantic galcenbayes.c -lm -o galcenbayes
	gcc -Wall -std=c99 -pedantic galcenbayes_fixedf.c -lm -o galcenbayes_fixedf

