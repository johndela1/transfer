for f in `seq 5`; do ./load.py | wc -l & done 
wait
