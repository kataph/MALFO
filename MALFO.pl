Occurrent(X) :- State(X) .
Occurrent(X) :- Process(X) .
Occurrent(X) :- Event(X) .

:- State(X), Process(X) .
:- State(X), Event(X) .
:- Process(X), Event(X) .

Occurrent(X):- causeOf(X,Y) .
Occurrent(Y):- causeOf(X,Y) .

:- causeOf(X,X) .

:- causeOf(X,Y), causeOf(Y,X).

causeOf(X,Y) :- achieves(X,Y) .
causeOf(X,Y) :- prevents(X,Y) .
causeOf(X,Y) :- allows(X,Y) .
causeOf(X,Y) :- disallows(X,Y) .
achieves(X,Y) v prevents(X,Y) v allows(X,Y) v disallows(X,Y) :- causeOf(X,Y) .

posCauseOf(X,Y) :- achieves(X,Y) .
posCauseOf(X,Y) :- allows(X,Y) .
posCauseOf(X,Y) :- facilPreconditionFor(X,Y) .
achieves(X,Y) v facilPreconditionFor(X,Y) v allows(X,Y) :- posCauseOf(X,Y) .

Event(X) v Process(X) v State(X) :- achieves(X,Y) .
Process(Y) v State(Y) :- achieves(X,Y) .
:- achieves(X,Y), State(X), Process(Y) .

AUX1(X,Y,z1(X,Y)) :- prevents(X,Y) .
State(Z) :- AUX1(X,Y,Z) .
incompatibleWith(Z,Y) :- AUX1(X,Y,Z) .
achieves(X,Z) :- AUX1(X,Y,Z) .
prevents(X,Y) :- State(Z), incompatibleWith(Z,Y), achieves(X,Z) .

Event(X) v Process(X) v State(X) :- prevents(X,Y) .
Process(Y) v State(Y) :- prevents(X,Y) .
:- prevents(X,Y), State(X), Process(Y) .


State(Z) :- facilPreconditionFor(Z,Y) . 
Event(Y) v Process(Y) v State(Y) :- facilPreconditionFor(Z,Y) . 

State(Z) :- prevPreconditionFor(Z,Y) . 
Event(Y) v Process(Y) v State(Y) :- prevPreconditionFor(Z,Y) . 

facilPreconditionFor(Z,Y) :- incompatibleWith(Z,W), prevPreconditionFor(W,Y).
prevPreconditionFor(Z,Y) :- incompatibleWith(Z,W), facilPreconditionFor(W,Y).

AUX2(X,Y,z2(X,Y)) :- allows(X,Y) .
AUX21(X,Y,Z) v AUX22(X,Y,Z) :- AUX2(X,Y,Z) .
facilPreconditionFor(Z,Y) :- AUX21(X,Y,Z) .
AUX211(X,Z) :- AUX21(X,Y,Z) .
achieves(X,Z) v maintains(X,Z) :- AUX211(X,Z) .
prevPreconditionFor(Z,Y) :- AUX22(X,Y,Z) .
prevents(X,Z) :- AUX22(X,Y,Z) .
:- AUX22(X,Y,Z), State(W), achieves(X,W), prevPreconditionFor(W,Y) .
allows(X,Y) :- achieves(X,Z), facilPreconditionFor(Z,Y) .
allows(X,Y) :- maintains(X,Z), facilPreconditionFor(Z,Y) .
allows(X,Y) :- prevents(X,Z), prevPreconditionFor(Z,Y), Occurrent(W), not AUX3(X,Y,W) .
AUX3(X,Y,W) :- State(W), achieves(X,W), prevPreconditionFor(W,Y) .

Event(X) v Process(X) :- allows(X,Y).
Event(Y) v Process(Y) v State(Y) :- allows(X,Y).

AUX4(X,Y,z4(X,Y)) :- disallows(X,Y) .
AUX41(X,Y,Z) v AUX42(X,Y,Z) :- AUX4(X,Y,Z) .
prevPreconditionFor(Z,Y) :- AUX41(X,Y,Z) .
AUX411(X,Z) :- AUX41(X,Y,Z) .
achieves(X,Z) v maintains(X,Z) :- AUX411(X,Z) .
prevents(X,Z) :- AUX42(X,Y,Z) .
facilPreconditionFor(Z,Y) :- AUX42(X,Y,Z) .
disallows(X,Y) :- achieves(X,Z), prevPreconditionFor(Z,Y) .
disallows(X,Y) :- maintains(X,Z), prevPreconditionFor(Z,Y) .
disallows(X,Y) :- prevents(X,Z), facilPreconditionFor(Z,Y) .

Event(X) v Process(X) :- disallows(X,Y) .
Event(Y) v Process(Y) v State(Y) :- disallows(X,Y).

Object(X) :- participatesIn(X,Y,T) .
Occurrent(Y) :- participatesIn(X,Y,T) .
Time(T) :- participatesIn(X,Y,T) .


Occurrent(Y) :- physicalConseqOf(X,Y) .
Occurrent(X) :- physicalConseqOf(X,Y) .

physicalConseqOf(X,Z) :- physicalConseqOf(X,Y), physicalConseqOf(Y,Z) .

achieves(X,Z) :- achieves(X,Y), physicalConseqOf(Y,Z) .
allows(X,Z) :- allows(X,Y), physicalConseqOf(Y,Z) .
prevents(X,Z) :- prevents(X,Y), physicalConseqOf(Y,Z) .
disallows(X,Z) :- disallows(X,Y), physicalConseqOf(Y,Z) .
achieves(Y,X) :- achieves(Z,X), physicalConseqOf(Y,Z) .
allows(Y,X) :- allows(Z,X), physicalConseqOf(Y,Z) .
prevents(Y,X) :- prevents(Z,X), physicalConseqOf(Y,Z) .
disallows(Y,X) :- disallows(Z,X), physicalConseqOf(Y,Z) .


Occurrent(X) :- FunctionCompatible(X) .
:-AUX5(O,X,T,F,B), FunctionCompatible(X) .
AUX5(O,X,T,F,B) :- participatesIn(O,X,T), functionOf_sys(F,O), CF(B,F,T), incompatibleWith(X,B) .
participatesIn(O,X,T) :- AUX5(O,X,T,F,B) .
functionOf_sys(F,O) :- AUX5(O,X,T,F,B) .
CF(B,F,T):- AUX5(O,X,T,F,B) .
incompatibleWith(X,B) :- AUX5(O,X,T,F,B) .
FunctionCompatible(X) :- Occurrent(X), Object(O), Function(F), Time(T), Behavior(B), not AUX5(O,X,T,F,B) .

posCauseOf_cross(X,Y) :- posCauseOf(X,Y) .
posCauseOf_cross(X,Z) :- posCauseOf(X,Y), posCauseOf_cross(Y,Z) .


FailureMechanism(X) :- Process(X), FunctionCompatible(X), Failure(Y), posCauseOf_cross(X,Y) .
FailureMechanism(X) :- Event(X), FunctionCompatible(X), Failure(Y), posCauseOf_cross(X,Y) .
Process(X) v Event(X) :- FailureMechanism(X) .
FunctionCompatible(X) :- FailureMechanism(X) .
AUX6(X,y6(X)) :- FailureMechanism(X) .
Failure(Y) :- AUX6(X,Y) .
posCauseOf_cross(X,Y) :- AUX6(X,Y) .

FailureCondition(X) :- State(X), FunctionCompatible(X), Failure(Y), posCauseOf_cross(X,Y) .
FailureCondition(X) :- State(X), FunctionCompatible(X), Failure(Y), prevPreconditionFor(X,Z), disallows(Z,Y) .
State(X) :- FailureCondition(X) .
FunctionCompatible(X) :- FailureCondition(X) .
AUX7(X,y7(X)) :- FailureCondition(X) .
Failure(Y) :- AUX7(X,Y) .
AUX8(X,Y) :- AUX7(X,Y) .
posCauseOf_cross(X,Y) v AUX9(X,Y,z9(X,Y)) :- AUX8(X,Y) .
prevPreconditionFor(X,Z) :- AUX9(X,Y,Z) .
disallows(Z,Y) :- AUX9(X,Y,Z) .

AUXA(X,Y) :- Failure(Y), causeOf(X,Y) .
MereSymptom(X) :- FunctionCompatible(X), Fault(Z), causeOf(Z,X), Occurrent(Y), not AUXA(X,Y) .
FunctionCompatible(X) :- MereSymptom(X) .
:- MereSymptom(X), Failure(Y), causeOf(X,Y).
AUXB(X,zb(X)) :- MereSymptom(X) .
Fault(Z) :- AUXB(X,Z) .
causeOf(Z,X) :- AUXB(X,Z) .

:- Malfunction(X), FunctionCompatible(X).

Fault(X) :- State(X), internalTo(Z,X), achieves(Z,X), not FunctionCompatible(X) .
State(X) :- Fault(X) .
:- Fault(X), FunctionCompatible(X).
AUXC(X,zc(X)) :- Fault(X) .
internalTo(Z,X) :- AUXC(X,Z) .
achieves(Z,X) :- AUXC(X,Z) .

DownState(X) :- State(X), not FunctionCompatible(X), not -Fault(X) .
State(X) :- DownState(X) .
:- DownState(X), FunctionCompatible(X) .
:- DownState(X), Fault(X) .

Failure(X) :- Malfunction(X), Event(X), Fault(Y), achieves(X,Y) .
Malfunction(X) :- Failure(X) .
Event(X) :- Failure(X) .
AUXD(X,yd(X)) :- Failure(X) .
Fault(Y) :- AUXD(X,Y) .
achieves(X,Y) :- AUXD(X,Y) .

NonPerformanceEvent(X) :- Malfunction(X), Event(X), not Failure(X) .
Malfunction(X) :- NonPerformanceEvent(X) .
Event(X):- NonPerformanceEvent(X) .
:- NonPerformanceEvent(X), Failure(X) .

MalfunctionProcess(X) :- Malfunction(X), Process(X) .
Malfunction(X) :- MalfunctionProcess(X) .
Process(X) :- MalfunctionProcess(X) .
