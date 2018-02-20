% %clear all
% %clc
%  
%  
% %Data = 'DataSheet.mat'
% %Data = xlsread('DataSheet.mat');
%  
% Y1 = DataSheet(1:116,3);
% Y2 = DataSheet(1:116,5);
% %Y3 = DataSheet(1:116,1);
% X = [1:116];
%  
% [ AX HL HR ] = plotyy(X,Y1,X,Y2);
% %[ AX HL HR HRR] = plotyy(X,Y1,X,Y2,X,Y3); 
% %plot(X,Y1,X,Y2);
%  
% set(get(AX(1),'Ylabel'),'String','Torque')
% set(get(AX(2),'Ylabel'),'String','HandsOFF Counter')
% %set(get(AX(3),'Ylabel'),'String','HandsOFF FLAG')
%  
%  
%  
% set(HL,'LineStyle','*')
% set(HR,'LineStyle','-')
% %set(HRR,'LineStyle','-')
%  
%  
%  
% %title('Display Data')
% xlabel('Domain Axis')
% grid on

%Y1 = DataSheet(1:3223,8);
%Y2 = DataSheet(1:3223,8);
%Y3 = DataSheet(1:133,9);
%Y4 = DataSheet(1:133,10);
% Y5 = DataSheet(1:611,11);
% X = [0.01:0.01:19.4];
%X = DataSheet(1:3223,7);

% figure(1);
% %subplot(4,1,1);
% plot(X,Y1);
% axis([-510 510 -6 6])
% % title('Steering Angle[deg]')
% xlabel('Steering Angle[deg]','fontsize',12,'fontweight','b')
% ylabel('Torque[Nm]','fontsize',12,'fontweight','b')
% % j = legend('Vehicle Speed[kph]',2);
% % set(j,'Interpreter','none')
% grid on
% 
% Y2 = DataSheet(1:1117,12);
% X2 = DataSheet(1:1117,11);
% figure(2);
% plot(X2,Y2,'r');
% axis([-2.7 2.7 -3.5 3.5])
% xlabel('Lateral Acceleration[m/sec^2]','fontsize',12,'fontweight','b')
% ylabel('Torque[Nm]','fontsize',12,'fontweight','b')
% grid on
% 
% Y3 = DataSheet(1:1117,14);
% X3 = DataSheet(1:1117,13);
% figure(3);
% plot(X2,Y2,'b',X3,Y3,'b');
% axis([-3.5 3.5 -3.5 3.5])
% xlabel('Lateral Acceleration[m/sec^2]','fontsize',12,'fontweight','b')
% ylabel('Torque[Nm]','fontsize',12,'fontweight','b')
% grid on

t1 = SteerWhlAg(1:174269,1);
y1 = SteerWhlAg(1:174269,2);
t2 = SteerWhlAgSpd(1:174269,1);
y2 = SteerWhlAgSpd(1:174269,2);
t3 = DegOfDe(1:87362,1);
y3 = DegOfDe(1:87362,2);
t4 = SideA(1:87362,1);
y4 = SideA(1:87362,2);
t5 = VehSpd(1:87360,1);
y5 = VehSpd(1:87360,2);

% X4 = DataSheet(1:1234,20);
% Y4 = DataSheet(1:1234,15);
% Y5 = DataSheet(1:1234,16);
% Y6 = DataSheet(1:1234,17);
% Y7 = DataSheet(1:1234,18);
% Y8 = DataSheet(1:1234,19);
% 
% X5 = DataSheet(1:1167,21);
% Y9 = DataSheet(1:1167,22);
% Y10 = DataSheet(1:1167,23);
% Y11 = DataSheet(1:1167,24);
% Y12 = DataSheet(1:1167,25);
% Y13 = DataSheet(1:1167,26);

figure(2);
subplot(5,1,1); plot(t1,y1);
% axis([0 1748 -540 440])
axis([0 1748 -200 200])
title('Steering Wheel Angle[deg]','fontsize',12,'fontweight','b')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% k = legend('Motor Current[A]',2);
% set(k,'Interpreter','none')
grid on

subplot(5,1,2); plot(t2,y2,'r');
axis([0 1748 -495 510])
title('Steering Wheel Angle Speed[deg/s]','fontsize',12,'fontweight','b')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% h = legend('Vehicle Load Ratio',2);
% set(h,'Interpreter','none')
grid on

subplot(5,1,3); plot(t3,y3,'g');
axis([0 1748 0 40])
title('Degree Of Deviation[им/s]','fontsize',12,'fontweight','b')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% g = legend('+B State',2);
% set(g,'Interpreter','none')
grid on

subplot(5,1,4); plot(t4,y4,'m');
axis([0 1748 -0.55 0.55])
title('Side Acceleration[g]','fontsize',12,'fontweight','b')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% i = legend('Steering Angle[deg]',2);
% set(i,'Interpreter','none')
grid on

subplot(5,1,5); plot(t5,y5,'c');
axis([0 1748 0 144])
title('Vehicle Speed[kph]','fontsize',12,'fontweight','b')
xlabel('Time(sec)','fontsize',12,'fontweight','b')
% i = legend('Steering Angle[deg]',2);
% set(i,'Interpreter','none')
grid on

% figure(5);
% subplot(5,1,1); plot(X5,Y9);
% axis([0 4.664 2 3.5])
% % title('Hands OFF Detection Flag')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% % k = legend('Motor Current[A]',2);
% % set(k,'Interpreter','none')
% grid on
% subplot(5,1,2); plot(X5,Y10,'r');
% axis([0 4.664 0 3])
% % title('Hands OFF Detection Flag')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% % h = legend('Vehicle Load Ratio',2);
% % set(h,'Interpreter','none')
% grid on
% 
% subplot(5,1,3); plot(X5,Y11,'g');
% axis([0 4.664 0 35])
% % title('Steering Wheel Torque[Nm]')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% % g = legend('+B State',2);
% % set(g,'Interpreter','none')
% grid on
% 
% subplot(5,1,4); plot(X5,Y12,'m');
% axis([0 4.664 0 35])
% % title('Hands OFF Counter')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% % i = legend('Steering Angle[deg]',2);
% % set(i,'Interpreter','none')
% grid on
% 
% subplot(5,1,5); plot(X5,Y13,'c');
% axis([0 4.664 0 55])
% % title('Hands OFF Counter')
% xlabel('Time(sec)','fontsize',12,'fontweight','b')
% % i = legend('Steering Angle[deg]',2);
% % set(i,'Interpreter','none')
% grid on



% % subplot(5,1,1); plot(X,Y1);
% % axis([0 6.28 -13 26])
% % % title('Yaw Rate[им/s]')
% % % xlabel('Time(sec)')
% % grid on
% % 
% % subplot(5,1,2); plot(X,Y2,'r');
% % axis([0 6.28 -8 2])
% % % title('Torque[Nm]')
% % % xlabel('Time(sec)')
% % grid on
% % 
% % subplot(5,1,3); plot(X,Y3,'g');
% % axis([0 6.28 -300 100])
% % % title('Steering Angle[deg]')
% % % xlabel('Time(sec)')
% % grid on
% % 
% % subplot(5,1,4); plot(X,Y4,'m');
% % axis([0 6.28 -50 550])
% % % title('Over Steer / Under Steer')
% % % xlabel('Time(sec)')
% % grid on
% % 
% % subplot(5,1,5); plot(X,Y5,'k');
% % axis([0 6.28 -0.2 1.2])
% % % title('OSC Flag')
% % xlabel('Time(sec)')
% % grid on
