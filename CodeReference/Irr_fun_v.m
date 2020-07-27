function Irr_fun_v()
% N a very large number;
sup = 1000;
V = 5;
IrrLevel_option = 1
IrrType_option = 1
global dt
%%%%%% RoadType_option = 1 high speed railway German spectra
%%%%%% RoadType_option = 2 high speed railway USA spectra

if IrrType_option == 1
    nl=2*pi/80; % unit rad/m, 0.5m
    nh=2*pi/0.5; % unit rad/m, 80m
    N=2048;
    % roughness coefficients
    switch IrrLevel_option
        case 0 % no roughness
            Av=0;
            wr=0.0206;
            wc=0.8246;
        case 1 % very good roughness
            % some coefficient
            Av=4.032e-7;
            wr=0.0206;
            wc=0.8246;
        case 2 % good roughness
            % some coefficient
            Av=10.80e-7; %(sqrt(10.80e-7)/25*sup)^2;
            wr=0.0206;
            wc=0.8246;
    end

elseif IrrType_option == 2
    nl=2*pi/300; % unit rad/m, 1.5m
    nh=2*pi/1.5; % unit rad/m, 300m
    N=2048;
    % roughness coefficients
    switch IrrLevel_option
        case 0 % no roughness
            Av=0;
            wc=0.8245;
        case 1 % level 1
            % some coefficient
            Av=1.2107e-4;
            wc=0.8245;
        case 2 % level 1 very poor
            Av=1.0181e-4;
            wc=0.8245;
        case 3 % level 1
            Av=0.6816e-4;
            wc=0.8245;
        case 4 % level 1
            Av=0.5376e-4;
            wc=0.8245;
        case 5 % level 1
            Av=0.2095e-4;
            wc=0.8245;
        case 6 % level 6 very good
            Av=0.0339e-4;
            wc=0.8245;
    end
end

deta_f = (nh-nl)/N; % unit rad/m

nk=nl+(nh-nl)/(2*N):(nh-nl)/N:nh-(nh-nl)/(2*N); % unit rad/m


faik=2*pi*rand(1,N); % random angle
ak2=zeros(1,N);    % the amplitude

for i=1:N
    wn=nk(i);
    if IrrType_option == 1
        Sn=(Av*wc^2/(wn^2+wr^2)/(wn^2+wc^2)); % unit m^2(rad/m)
    elseif IrrType_option == 2
        Sn=(0.25*Av*wc^2/(wn^2)/(wn^2+wc^2)); % unit m^2(rad/m)
    end
    ak2(i)=sqrt(2*deta_f*Sn);  % unit m
end
step = 1/(nh/2/pi)/V/2
x = sup/V
t=0:1/(nh/2/pi)/V/2:sup/V;   %time increment 0:1/(nh/2/pi)/V/2:25/V;
% t=0:dt:sup/V;   %time increment
Lt=length(t);

qkdd=zeros(N,Lt);
for i=1:N
    qkdd(i,:)=-(nk(i))^2*ak2(i)*cos(nk(i)*V*t+faik(i));
end
qtdd=zeros(1,Lt);
qtdd(:)=sum(qkdd)';

qkd=zeros(N,Lt);
for i=1:N
    qkd(i,:)=-(nk(i))*ak2(i)*sin(nk(i)*V*t+faik(i));
end
qtd=zeros(1,Lt);
qtd(:)=sum(qkd)';

qk=zeros(N,Lt);
for i=1:N
    qk(i,:)=ak2(i)*cos(nk(i)*V*t+faik(i));
end
qt=zeros(1,Lt);
qt(:)=sum(qk)';


h = abs(diff([t(2)*V, t(1)*V])); % the time increment
% first derivative
yapp1 = gradient(qt, h); %matlab silumation

% second derivative
yapp2 = 2*2*del2(qt, h); %matlab silumation

Irr_vec=[t*V;-qt;-qtd;-qtdd]; %[t*V*sup/25;qt;qtd*25/sup;qtdd];
 figure(4001);
 plot(t*V,qtdd),
 grid on
 title('road roughness£¨x£©')
 xlabel('time t/s')
 ylabel('m/s^2')
 hold on
 plot(t*V,yapp2),
 
 figure(4004);
 plot(t*V,qtd),
 grid on
 title('road roughness£¨x£©')
 xlabel('time t/s')
 ylabel('m/s^2')
 hold on
 plot(t*V,yapp1),
 
 figure(4002);
 plot(t*V,qt),
 grid on
 title('road roughness£¨x£©')
 xlabel('time t/s')
 ylabel('m')
 hold on

% fft
acc1=qtdd;
delta_t=t(2)-t(1);
Fs_1=1/(delta_t);
L_1=length(acc1);
NFFT_1 = 2^nextpow2(L_1);
Y_1 = fft(acc1,NFFT_1)/L_1;
Y=2*abs(Y_1(1:NFFT_1/2+1));
f_1 = Fs_1/2*linspace(0,1,NFFT_1/2+1);

 figure(4040)
 plot(f_1,Y);
 xlabel('Frequency (Hz)')
 ylabel('Amplitude (m)')
 hold on

end

% function [Irr_vec] = Irr_fun (sup,V,seed,IrrDirection_option)
% % N a very large number;
% global IrrLevel_option;
% global IrrType_option;
% global dt tn_sub;
% %%%%%% RoadType_option = 1 high speed railway German spectra
% %%%%%% RoadType_option = 2 high speed railway USA spectra
% 
% if IrrType_option == 1
%     nl=2*pi/80; % unit rad/m, 0.5m
%     nh=2*pi/0.5; % unit rad/m, 80m
%     N=512;
%     
%     % roughness coefficients
%     
%     switch IrrLevel_option
%         case 0 % no roughness
%             % some coefficient
%             Av=0;           % m^2/rad/m
%             wr=0.0206;      % /rad/m
%             wc=0.8246;      % /rad/m
%         case 1 % very good roughness
%             % some coefficient
%             Av=4.032e-7;    % m^2/rad/m
%             wr=0.0206;      % /rad/m
%             wc=0.8246;      % /rad/m
%         case 2 % good roughness
%             % some coefficient
%             Av=10.80e-7;    % m^2/rad/m
%             wr=0.0206;      % /rad/m
%             wc=0.8246;      % /rad/m
%     end
%     
%     
% elseif IrrType_option == 2
%     nl=2*pi/300; % unit rad/m, 1.5m
%     nh=2*pi/1.5; % unit rad/m, 300m
%     N=512;
%     
%     % roughness coefficients
%     switch IrrLevel_option
%         case 0 % no roughness
%             Av=0;
%             wc=0.8245;
%         case 1 % level 1
%             % some coefficient
%             Av=1.2107e-4;
%             wc=0.8245;
%         case 2 % level 1 very poor
%             Av=1.0181e-4;
%             wc=0.8245;
%         case 3 % level 1
%             Av=0.6816e-4;
%             wc=0.8245;
%         case 4 % level 1
%             Av=0.5376e-4;
%             wc=0.8245;
%         case 5 % level 1
%             Av=0.2095e-4;
%             wc=0.8245;
%         case 6 % level 6 very good
%             Av=0.0339e-4;
%             wc=0.8245;
%     end
% end
% 
% deta_f=(nh-nl)/N; % unit rad/m
% 
% % t=0:dt/tn_sub/2:sup/V;   %time increment
% t=0:1/(nh*V/2/pi)/2:sup/V;   %time increment
% % the time step should be twice of the highest frequecy
% 
% Lt=length(t);
% 
% rand('state',seed);
% faik=unifrnd(0,2*pi,1,N);       % random angle
% Sn=zeros(1,N);                  % the specturm
% A=zeros(1,N);                   % the amplitude
% Ad=zeros(1,N);                   % the amplitude
% Add=zeros(1,N);                   % the amplitude
% qt=zeros(1,Lt);                 % the sample
% qtd=zeros(1,Lt);                 % the sample
% qtdd=zeros(1,Lt);                 % the sample
% 
% nk=nl+(nh-nl)/(2*N):(nh-nl)/N:nh-(nh-nl)/(2*N);  % central frequency
% 
% for l=1:Lt
%     for i=1:N
%         Sn(i)=(Av*wc^2/(nk(i)^2+wr^2)/(nk(i)^2+wc^2)); % unit m^2(rad/m)
%         A(i)=sqrt(2*Sn(i)*deta_f)*cos(nk(i)*t(l)*V+faik(i));
%         Ad(i)=-(nk(i))*sqrt(2*Sn(i)*deta_f)*sin(nk(i)*t(l)*V+faik(i));
%         Add(i)=-(nk(i))^2*sqrt(2*Sn(i)*deta_f)*cos(nk(i)*t(l)*V+faik(i));
%     end
%     qt(l)=sum(A);
%     qtd(l)=sum(Ad);
%     qtdd(l)=sum(Add);
% end
% 
% 
% h = abs(diff([t(2)*V, t(1)*V])); % the time increment
% 
% % first derivative
% yapp1 = gradient(qt, h); %matlab silumation
% 
% % second derivative
% yapp2 = 2*2*del2(qt, h); %matlab silumation
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% 
% Irr_vec=[t*V;qt;qtd;qtdd];
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % figure(4003);
% % hold on
% % plot(t,qtdd),
% % plot(t,yapp2),
% % grid on
% % title('road roughness£¨x£©')
% % xlabel('time t/s')
% % ylabel('m/s^2')
% % 
% % 
% % figure(4002);
% % hold on
% % plot(t,qtd),
% % plot(t,yapp1),
% % grid on
% % title('road roughness£¨x£©')
% % xlabel('time t/s')
% % ylabel('m/s')
% % hold on
% % 
% % 
% % figure(4001);
% % plot(t,qt),
% % grid on
% % title('road roughness£¨x£©')
% % xlabel('time t/s')
% % ylabel('m')
% % hold on
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% 
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% acc1=qt;
% delta=t(2)-t(1);
% Fs_1=1/(delta);
% L_1=length(acc1);
% NFFT_1 = 2^nextpow2(L_1); % Next power of 2 from length of y
% Y_1 = fft(acc1,NFFT_1)/L_1;
% Y=2*abs(Y_1(1:NFFT_1/2+1));
% f_1 = Fs_1/2*linspace(0,1,NFFT_1/2+1);
% % Plot single-sided amplitude spectrum.
% 
% % figure(4004)
% % loglog(f_1,Y);
% % hold on;
% % loglog(nk*2*pi*2,sqrt(2*deta_f*Sn),'r');
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% 
% 
% 
% 
% end