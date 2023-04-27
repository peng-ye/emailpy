# Examples
## email scanning results (with scripts)
python emailpy.py --scan_results ./scan_results.txt --map_file ./user_email_map.txt


## email stats for CPU usage
### Case 1
\# every 30min, email the stat of the avg CPU usage for the past 60s with 1s interval (wait for 30min)

python email_cpu_usage_stat.py -e ye@hk -i 1 -t 60 -p src/avg_cpu_usage_once.sh -s 1800

### Case 2
\# email the stat of the avg CPU usage for each hour with 5min interval, if the stat is lower than 80%, with greetings :)

python email_cpu_usage_stat.py -e ye@hk,jie@hk -i 300 -t 12 -p src/avg_cpu_usage_once.sh -th 80 -hd "Hi there. "

