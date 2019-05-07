%------------Rama izquierda------------
%joints_dazzling_and_rusting(true/false,valvetype for thickness analisys)
joints_dazzling_and_rusting(X1,Type):-X1==true,writeln('Coordination is required'),!;X1==false,thickness_less_treshold_limit(Type).

thickness_less_treshold_limit(Valvetype):-safety_valve_thickness(Valvetype,Thickness),
                                         Thickness<50,writeln('Report to technical Inspection'),!
                                         ;safety_valve_thickness(Valvetype,Thickness),Thickness>=50,writeln('The condition of the equipment is suitable').

%------------Rama derecha------------

gas_leakage_at_joint(X3):-X3==true,writeln('Check for leakage_fixed_with_wrench'),!
                          ;X3==false,writeln('The safety valve joint is free for gass leakage').

leakage_fixed_with_wrench(X4):-X4==true,writeln('Report to technical inspection unit'),!
                              ;X4==false,writeln('Send a report to the repair department to fix the fault').

%------------Rama central------------

safety_valve_with_gas_evacuation(X5):-X5==true,writeln('Check line_gas_pressure_appropriate'),!
                                      ;X5==false,writeln('Check relief_valve_work_correctly').

%relief_valve_work_correctly(valvetype,regulating pressure,increase percentage of regulating pressure)
relief_valve_work_correctly(Valvetype,Rp,IPRG):-relief_valve_pressure(Valvetype,MaxRp), (Rp*IPRG/100+Rp)<MaxRp,
                                                writeln('Safety funtion is appropriate'),!;writeln('Check valve_status_close_position').

line_gas_pressure_appropriate(X6):-X6==true,writeln('Check pressure_sensor_pipes_blocked'),!
                                  ;X6==false,writeln('Adjust the regulator according to the instructions').

valve_status_close_position(X8):-X8==true,writeln('Place the safety valve in open position'),!
                                ;X8==false,writeln('Check control_valve_sensors_blocked').

pressure_sensor_pipes_blocked(X9):-X9==true,writeln('Clean up and fix the faults of the sensing pipes'),!
                                  ;X9==false,writeln('Check safety_spring_effective').

control_valve_sensors_blocked(X10):-X10==true,writeln('Cleaning and troubleshooting of the sensing pipes'),!
                                    ;X10==false,writeln('Check performance_efficiency_sv_spring').

safety_spring_effective(X11):-X11==true,writeln('Check preventable_leakage_sit_orifice'),!
                              ;X11==false,writeln('Replace the safety spring in the service').

performance_efficiency_sv_spring(X12):-X12==true,writeln('Check proper_leakage_prevention_sit_orifice'),!
                                      ;X12==false,writeln('Putting spring and safety in the service').

proper_leakage_prevention_sit_orifice(X13):-X13==true,writeln('Check does_pilot_work_properly'),!
                                      ;X13==false,writeln('Replace sit and orifice and put the safety valve into circuit').

does_pilot_work_properly(X2):-X2==true,writeln('Set the safety valve according to the instructions'),!
                              ;X2==false,writeln('Pilot full service and reinstallation').

preventable_leakage_sit_orifice(X14):-X14==true,writeln('Set the safety valve according to the instructions'),!
                                    ;X14==false,writeln('Replace sit and orifice and put the safety valve into circuit').

%------------Base de conocimientos------------

%safety_valve_thickness(valvetype,thickness).
safety_valve_thickness(sv1,20).
safety_valve_thickness(sv2,40).
safety_valve_thickness(sv3,100).

%relief_valve_pressure(valvetype,max regulating pressure).
relief_valve_pressure(rv1,50).
relief_valve_pressure(rv2,150).
relief_valve_pressure(rv3,250).
