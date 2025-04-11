# TBM
With the rapid development of transportation infrastructure such as subways, highways, and other underground projects, China has become the world's largest market for shield tunneling equipment. The shield machine load plays a critical role in construction efficiency and operational safety. Therefore, we developed a shield tunneling load prediction system.

This software was developed using PySide2 and tested on the Windows 11 platform. It integrates pre-trained models based on Support Vector Regression (SVR) and Random Forest (RF) algorithms. By taking key operational parameters from each ring segment of slurry or earth pressure balance shield tunneling as input, the system predicts the corresponding shield loads—namely thrust force and torque—to assist in process control and decision-making during construction. The predicted results are visualized in chart form within the software.

The embedded pre-trained models were developed using real-world datasets: one from a slurry shield project (Chongqing Yangtze River Tunnel) and the other from an EPB shield project (Tianjin Metro Line 9). Using Mean Absolute Percentage Error (MAPE) as the evaluation metric, the models achieved the following results on test sets:

SVR model for slurry shield thrust: MAPE = 6.02%

SVR model for slurry shield torque: MAPE = 0.81%

RF model for EPB shield thrust: MAPE = 3.28%

RF model for EPB shield torque: MAPE = 4.75%

These four models were selected from a broader set of machine learning models based on having the lowest MAPE, representing the most accurate performance in predicting shield loads.
![image](https://github.com/user-attachments/assets/7371271f-ae82-4881-b740-345233321d0b)
![image](https://github.com/user-attachments/assets/c46937c7-fed5-4c57-a861-b708cab8fd64)
