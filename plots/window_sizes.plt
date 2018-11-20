reset

#set title "small vs. big batch size"
set ylabel "F-measure"
set xlabel "window size (seconds)"

#set xtics nomirror
#set xtics 128
#set ytics 128
#set term png

#set term png truecolor enhanced font "Times,15"
#set term pngcairo dashed
set terminal pngcairo


set style data linespoints
#set sample 500
set yrange [20:100]

#set logscale x 2
#set logscale y 2
set grid
set termoption dashed

set output "experiments/results/window_sizes_datos1_fmeasure.png"

plot 	"experiments/results/window_sizes_CL2_CO1_model1_datos1.dat" using 1:2 dt 2 pt 4 lc rgb "black" title "CONVNETQUAKE" ,   \
"experiments/results/window_sizes_CL2_CO1_model2_datos1.dat" using 1:2 pt 5 lc rgb "black" title "UPC-UCV"

set output "experiments/results/window_sizes_datos2_fmeasure.png"

plot 	"experiments/results/window_sizes_CL2_CO1_model1_datos2.dat" using 1:2 dt 2 pt 4 lc rgb "black" title "CONVNETQUAKE" ,   \
"experiments/results/window_sizes_CL2_CO1_model2_datos2.dat" using 1:2 pt 5 lc rgb "black" title "UPC-UCV"

set output "experiments/results/window_sizes_datos3_fmeasure.png"

plot 	"experiments/results/window_sizes_CL2_CO1_model1_datos3.dat" using 1:2 dt 2 pt 4 lc rgb "black" title "CONVNETQUAKE" ,   \
"experiments/results/window_sizes_CL2_CO1_model2_datos3.dat" using 1:2 pt 5 lc rgb "black" title "UPC-UCV"

set output "experiments/results/window_sizes_datos1_datos2_datos3_fmeasure.png"

plot 	"experiments/results/window_sizes_CL2_CO1_model1_datos1_datos2_datos3.dat" using 1:2 dt 2 pt 4 lc rgb "black" title "CONVNETQUAKE" ,   \
"experiments/results/window_sizes_CL2_CO1_model2_datos1_datos2_datos3.dat" using 1:2 pt 5 lc rgb "black" title "UPC-UCV"