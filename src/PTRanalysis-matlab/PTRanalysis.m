%% Pulse Tube Refrigerator Analysis
% First developed by: Alisha Schor, alisha.schor@gmail.com Used from DSpace
% Further Developed by Jacob Miske for 2.013 PTR 2019-2020
% Define geometric parameters
% All units SI (kg-m-s)

% This codebase needs to be built out further, perhaps translated to Python
% TODO: input based calculations

% Method:
% 1. Find best 'k' by scanning for max cooling power given system
% 2. Set k to best
% 3. Vary a different system parameter for that k
% 4. Look for gains in cooling power

%% Constants
%Inches to meters multiplier
TOSI=0.0254;

%% Dimensions
% Swept Volume (cylinder)
dswept = 1.364*TOSI;
lswept = 0.1;
f      = 60; %Hz
Aswept = pi*dswept^2/4;
w      = 2*pi*f;
% Aftercooler (first HEX)
do = 0.811*TOSI;
lo = 0.7*TOSI;
Ao = pi*do^2/4;
Vo = Ao*lo;
% Regenerator
dr = 1.364*TOSI;
lr = 6*TOSI;
Ar = pi*dr^2/4;
Vr = Ar*lr;
% Cold HEX
dc = 0.811*TOSI;
lc = 0.7*TOSI;
Ac = pi*dc^2/4;
Vc = Ac*lc;
% Pulse Tube
dpt = 0.81*TOSI;
lpt = 6*TOSI;
Apt = pi*dpt^2/4;
Vpt = Apt*lpt;
% Warm HEX
dh = 0.811*TOSI;
lh = 0.7*TOSI;
Ah = pi*dh^2/4;
Vh = Ah*lh;
% Choose temperatures
Tc = 120; %K
Th = 300; %K
Tr = (Th-Tc)/log(Th/Tc);
% NOTE: Either properties of air or properties
% of nitrogen must be commented prior to running
% this file, only one set of working fluid 
% params is used


%% Material Properties

% TODO: have users input Air, N, CH4,or He and re-evalaute model for each 

% Properties of air
% R=287;            % J/kg-K
% rhoo=1.229;       % kg/m-3
% gamma=1.4;
% Patm=1.1Oe5;      % Pa
% mu=1.5e-5;        % Pa-s
% cp=1003;          % J/kg-K
% kair=0.02544;     % W/m-K
% nu=1.475e-5;      % m^2/s

% Properties of nitrogen
% R=290;              % J/kg-K
% rhoo=1.116;         % kg/m^3
% gamma=1.4;          % Non-dimensional
% Patm=1.01e5;        % Pa
% mu=1.8042e-5;       % Pa-s
% cp=1041.4;          % J/kg-K
% kair=0.02607;       % W/m-K
% nu=1.6231-5;        % m^2/s

% Properties of Helium
R     = 2077;       % J/kg-K
rhoo  = 0.2501;     % kg/m^3 at -80C
gamma = 1.4;        % Non-dimensional
Patm  = 1.01e5;     % Pa
mu    = 1.96e-5;    % Pa-s
cp    = 5188;       % J/kg-K
kair  = 0.149;      % W/m-K
nu    = 1.87-5;     % m^2/s

% Properties of copper
ccu     = 385;      %J/kg-K
kcu     = 385;      %W/m-K
rhocu   = 8960;     %kg/m^3

% Chosen properties for init pressure and k (orifice flow rate)
Po  = Patm;
Va  = Aswept*lswept;
k   = 2:0.25:15;
k   = 10.^(-k);


%% Time vector
t=0:0.005:2;
for j=1:length(k)
    % Honestly, this is the most important part of the tool and I don't
    % know how it works
    a(j) = R*Th/Po*(Vh/(R*Th)+(k(j)*rhoo/(i*w)));
    
    b(j) = a(j)+Vpt/(gamma*Po)+Vh/(rhoo*R*Th)-1/rhoo*(Vh/(R*Th)+...
    (k(j)*rhoo/(i*w))+k(j)/(i*w));
    
    c(j) = R*Th/Po*(Vo/(R*Th)+Vr/(R*Th)+Vc/(R* Tc)+b(j)*Po/(R*Tc)-...
    b(j)*rhoo+a(j)*rhoo+rhoo*Vpt/(gamma*Po)+Vh/(R*Th)-a(j)*...
    Po/(R*Th)+k(j)*rhoo/(i*w));
end

phase   = angle(c)*180/pi;
MagC    = abs(c);


%% Calculate work and cooling power by choosing either
% pressure or volume amplitude.
% Pa=Va./MagC or Va=Pa.*MagC
Pa      = Va./MagC;
Work    = 0.5.*Pa.*Va.*sin(angle(c))*f;
DV3     = Pa.*abs(b);
Qc      = abs(-.5.*Pa.*DV3.*sin(angle(b))*f+i*w/(R*Tc)*(Pa*Vc+DV3*Po));

MaxWork     = max(-Work);
MaxCooling  = max(Qc);
for g=1:length(Work)
    if Qc(g)== MaxCooling
        OptimumK     = k(g);
        OptimumPhase = angle(c(g))*180/pi;
        MassFlow     = OptimumK*rhoo*Pa(g);
        VolFlow      = OptimumK*Pa(g);
        break
    end
end


%% Plot outputs
figure(1)
subplot(2,1,1)
semilogx(k,phase);xlabel('k');ylabel('Phase (deg)');
grid on
title("P-T Phase Shift and Cooling Power")
xlim([1e-10, 1e-6])
hold on
subplot(2,1,2)
semilogx(k,-Work,'k-.');
hold on
semilogx(k,Qc,'b');
legend('Work','Qc')
xlabel('k');
ylabel('Cooling Power (W)');
grid on
% xlim([1e-11, 1e-5])
saveas(gcf, "phase_and_cooling.png")

%% Phase Shift Plot
figure(2)
semilogx(k,phase);xlabel('k');ylabel('Phase (deg)');
grid on
title("P-T Phase Shift")
% xlim([1e-10, 1e-6])
improvePlot
saveas(gcf, "phase.png")

%% Cooling Power Plot
figure(3)
semilogx(k,-Work,'k-.');
hold on
semilogx(k,Qc,'b');
legend('Work','Qc')
xlabel('k');
ylabel('Cooling Power (W)');
grid on
% xlim([1e-11, 1e-5])
title("Cooling Power Ratio f(k)")
improvePlot
saveas(gcf, "cool_power.png")

%% Valve sizing and Cv
% Based on Swagelok & Parker references
Q  = OptimumK*Pa(g)*2118.88;     %CFM
P1 = (Po+Pa(g)/2)*0.0001450377;  %PSIA
P2 = Po*0.0001450377;            %PSIA
% SG=I; % air
SG = 0.967; %nitrogen T=(Th-273.15)*9/5+32+460; % "Absolute Temperature"
T  = 180;
Cv = Q/16.05*sqrt(SG*T/ (P1^2-P2^2));


% Required nozzle size based on mass flow rate
Pup  = 60;             %upstream pressure in psi
Pup  = Pup*6894.757;   %upstream pressure in Pa
Anoz = MassFlow/(gamma^.5)*(2/(gamma+1))^(-(gamma+1)/(2*gamma-1))*sqrt(R*Th)/(Pup);
Dnoz = sqrt (4/pi*Anoz);


