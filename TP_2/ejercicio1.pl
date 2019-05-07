%------------Rama izquierda------------

joints_dazzling_and_rusting(X1,Type):-X1==true,writeln('Coordination is required'),!;X1==false,thickness_less_treshold_limit(Type).
thickness_less_treshold_limit(Valvetype):-valve_thickness(Valvetype,Thickness),
                                         Thickness<50,writeln('Report to technical Inspection'),!
                                         ;valve_thickness(Valvetype,Thickness),Thickness>=50,writeln('The condition of the equipment is suitable').

%------------Rama derecha------------

gas_leakage_at_joint(X3):-X3==true,writeln('Check for leakage_fixed_with_wrench'),!
                          ;X3==false,writeln('The safety valve joint is free for gass leakage').

leakage_fixed_with_wrench(X4):-X4==true,writeln('Report to technical inspection unit'),!
                              ;X4==false,writeln('Send a report to the repair department to fix the fault').

%------------Rama central------------
safety_valve_with_gas_evacuation(X5)
does_pilot_work_properly(X2):-X2==true,writeln('Set the safety valve according to the instructions'),!
                              ;X2==false,writeln('Pilot full service and reinstallation').

%------------Base de conocimientos------------

valve_thickness(v1,20).
valve_thickness(v2,40).
valve_thickness(v3,100).
