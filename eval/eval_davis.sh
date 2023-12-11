python ./test.py

python ./eval/convert_davis.py \
--out_folder './results/davis_results/' \
--in_folder './results/davis2/' \
--dataset '/home/qinzheyun/Data/DAVIS/'

python ./eval/evaluation_method.py \
--task semi-supervised   --results_path './results/davis_results/' --set val \
--davis_path '/home/qinzheyun/Data/DAVIS/'