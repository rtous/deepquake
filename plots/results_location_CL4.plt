# set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 500, 350 
# set output 'histograms.7.png'
set border 3 front linetype -1 linewidth 1.000
set boxwidth 0.95 absolute
set style fill   solid 1.00 noborder
set grid nopolar
set grid noxtics nomxtics ytics nomytics noztics nomztics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set grid layerdefault   linetype 0 linewidth 1.000,  linetype 0 linewidth 1.000
set key bmargin center horizontal Left reverse noenhanced autotitles columnhead nobox
set style histogram clustered gap 1 title  offset character 2, 0.25, 0
set datafile missing '-'
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -45  offset character 0, 0, 0 autojustify
set xtics  norangelimit font ",8"
# set xtics   ()
set ytics border in scale 0,0 mirror norotate  offset character 0, 0, 0 autojustify
set ztics border in scale 0,0 nomirror norotate  offset character 0, 0, 0 autojustify
# set cbtics border in scale 0,0 mirror norotate  offset character 0, 0, 0 autojustify
# set rtics axis in scale 0,0 nomirror norotate  offset character 0, 0, 0 autojustify
#set title "F-measure results of the different models over the different datasets" 
#set xlabel "#workers" 
set xlabel  offset character 0, -2, 0 font "" textcolor lt -1 norotate
set ylabel "Accuracy" 
set yrange [0.3:1]
# i = 23
set term png
set output "output/results_location_CL4.png"
plot newhistogram "", 'output/results_location_CL4.dat' using 2:xtic(1) t col lc rgb 'light-gray' fs pattern 3, '' u 3 t col lc rgb 'dark-gray' fs pattern 3, '' u 4 t col lc rgb 'black' fs pattern 1, '' u 5 t col lc rgb 'black' fs pattern 2



