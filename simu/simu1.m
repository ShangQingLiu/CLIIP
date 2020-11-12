clc;clear
%%SEIR  Transmission  dynamics  model  of  2019  nCoV coronavirus  with  considering  the  weak  infectious  ability  and changes in latency duration%%%%%%
%%Shi Pengpeng,Cao Shengli,Feng Peihua,Completed on Jan 5th, first released on Jan 7th%%
%%This latest modified version was released on Feb. 10th, 2020%%
%% Model parameters
c=3.6;beta=6.93e-11;delta_I=0.13; 
delta_q=0.13;gama_I=0.003; gama_H=0.009; q=9e-7; alpha=0.0001;theta=0.6;
lam=1/14; T=40; t=0.1; NN=T/t;
%% Initial values
%%S=13.95e8; E=4007; I=776; Sq=8420;Eq=3000; H=I+Eq; R=34; De=25;
S=1.3331e4; E=889; I=100; Sq=358; Eq=64; H=164; R=4; 
AA=[S E I Sq Eq H R];
for ii=1:NN
	%% Modified SEIR Transmission dynamics model   
	sigma=(1/7-1/3)./(1+exp((ii*t-4)./ii*t/0.2))+1/3;
	dS = -(beta*c+c*q*(1-beta))*S*(I+theta*E)+lam*Sq;
	dE = beta*c*(1-q)*S*(I+theta*E)-sigma*E;
	dI = sigma*E-(delta_I+alpha+gama_I)*I;
	dSq =(1-beta)*c*q*S*(I+theta*E)-lam*Sq;
	dEq = beta*c*q*S*(I+theta*E)-delta_q*Eq;
	dH = delta_I*I+delta_q*Eq-(alpha+gama_H)*H;
	dR = gama_I*I+gama_H*H;dDe = alpha*(I+H);
	%% Euler integration algorithm
	 S =S+dS*t;
	E = E+dE*t;
	I = I+dI*t;
	Sq = Sq+dSq*t;
	Eq = Eq+dEq*t;
	H = H+dH*t;
	R = R+dR*t;
	AA=[AA; S E I Sq Eq H R];
	end
%% Theoretical estimation
Infected(:,1)= round(AA(1:1/t:size(AA,1),3));
Cured(:,1)=round(AA(1:1/t:size(AA,1),7));
plot(0:T,[Infected Cured])
%% raw data
hold on
data_Infected=[776 776	1218 1880 2630 4369 5762 7440 9336 11319	13779	16402	19413	22980 26343	29034	31826	33788 36043	37693]';
data_Cured=[34 34   38  49  51  60  103 126 171 243 328 475 632 892 1153 1540 2050 2651 3283 3998]';
%%plot([1:length(data_Infected)]'-1,[data_Infected data_Cured],'*')