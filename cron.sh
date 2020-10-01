# Monday and Wednesday 2am signup RLC
0 2 * * 1,3 nohup /home/lathonez/python main.py rlc > /tmp/cares.log 2>&1


# Thursday and Friday 2am signup Coalition
0 2 * * 6,7 nohup /home/lathonez/python main.py coalition > /tmp/cares.log 2>&1