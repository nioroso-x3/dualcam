#/bin/bash
#temporary script to set the rpi pwm 
echo "2" | sudo tee -a "/sys/class/pwm/pwmchip2/export"
echo "0" | sudo tee -a "/sys/class/pwm/pwmchip2/pwm2/enable"
sleep 0.2
echo "200000000" | sudo tee -a "/sys/class/pwm/pwmchip2/pwm2/period"
sleep 0.2
echo "180000000" | sudo tee -a "/sys/class/pwm/pwmchip2/pwm2/duty_cycle"
echo "1" | sudo tee -a "/sys/class/pwm/pwmchip2/pwm2/enable"
