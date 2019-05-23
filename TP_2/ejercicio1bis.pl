/* Axiomas */

verificar(leaked_fixed_wrench_joints) :-
                estado(leaked_fixed_wrench_joints,desconocido),
                ((estado(gas_leakage_at_joint, ok), writeln('Verificar leaked_fixed_wrench_joints'));
                verificar(gas_leakage_at_joint)).

verificar(gas_leakage_at_joint) :-
                estado(gas_leakage_at_joint,desconocido),
                writeln('Verificar gas_leakage_at_joint').

%----------------------------------

verificar(thickness_treshold_limit) :-
                estado(thickness_treshold_limit,desconocido),
                ((estado(valve_dazzling_and_rusting, ok), writeln('Verificar thickness_treshold_limit'));
                verificar(valve_dazzling_and_rusting)).

verificar(valve_dazzling_and_rusting) :-
                estado(valve_dazzling_and_rusting,desconocido),
                writeln('Verificar valve_dazzling_and_rusting').

%-----------------------------------

verificar(preventable_leakage_between_sit_n_orifice) :-
                estado(preventable_leakage_between_sit_n_orifice,desconocido),
                ((estado(safety_spring_effective, ok), writeln('Verificar preventable leakage between sit n orifice'));
                verificar(safety_spring_effective)).

verificar(safety_spring_effective) :-
                estado(safety_spring_effective,desconocido),
                ((estado(control_preasure_sensor_pipes_blocked, ok), writeln('Verificar safety spring effective'));
                verificar(control_preasure_sensor_pipes_blocked)).

verificar(control_preasure_sensor_pipes_blocked) :-
                estado(control_preasure_sensor_pipes_blocked,desconocido),
                ((estado(line_gas_pressure_appropriate, ok), writeln('Verificar control preasure sensor pipes blocked'));
                verificar(line_gas_pressure_appropriate)).

verificar(line_gas_pressure_appropriate) :-
                estado(line_gas_pressure_appropriate,desconocido),
                ((estado(safety_valve_has_continuous_evacuation, ok), writeln('Verificar line gas pressure appropriate'));
                verificar(safety_valve_has_continuous_evacuation)).

%-----------------------------------

verificar(pilot_works_properly) :-
                estado(pilot_works_properly, desconocido),
                ((estado(leakage_prevention_between_sit_and_orifice, ok), writeln('Verificar Pilot'));
                verificar(leakage_prevention_between_sit_and_orifice)).

verificar(leakage_prevention_between_sit_and_orifice) :-
                estado(leakage_prevention_between_sit_and_orifice, desconocido),
                ((estado(safety_valve_spring, ok), writeln('Verificar leakage prevention between sit and orifice'));
                verificar(safety_valve_spring)).

verificar(safety_valve_spring) :-
                estado(safety_valve_spring, desconocido),
                ((estado(control_valve_sensors_blocked, no), writeln('Verificar safety valve spring'));
                verificar(control_valve_sensors_blocked)).

verificar(control_valve_sensors_blocked) :-
                estado(control_valve_sensors_blocked, desconocido),
                ((estado(valve_status_closed, no), writeln('Verificar control valve sensors blocked'));
                verificar(valve_status_closed)).

verificar(valve_status_closed) :-
                estado(valve_status_closed, desconocido),
                ((estado(relief_valve_ok_with_10_percent_more_pressure, no), writeln('Verificar valve status "Close"'));
                verificar(relief_valve_ok_with_10_percent_more_pressure)).

verificar(relief_valve_ok_with_10_percent_more_pressure) :-
                estado(relief_valve_ok_with_10_percent_more_pressure, desconocido),
                ((estado(safety_valve_has_continuous_evacuation, no), writeln('Verificar relief valve works correctly with +10% over regular pressure'));
                verificar(safety_valve_has_continuous_evacuation)).
verificar(safety_valve_has_continuous_evacuation) :-
                estado(safety_valve_has_continuous_evacuation, desconocido),
                writeln('Verificar safety valve has continuous evacuation').


/* Ground Facts (se pueden modificar dinamicamente con assert y retract)*/
estado(pilot_works_properly, desconocido).
estado(leakage_prevention_between_sit_and_orifice, desconocido).
estado(safety_valve_spring, desconocido).
estado(control_valve_sensors_blocked, desconocido).
estado(valve_status_closed, desconocido).
estado(relief_valve_ok_with_10_percent_more_pressure, desconocido).
estado(safety_valve_has_continuous_evacuation, desconocido).
estado(preventable_leakage_between_sit_n_orifice,desconocido).
estado(safety_spring_effective,desconocido).
estado(control_preasure_sensor_pipes_blocked,desconocido).
estado(line_gas_pressure_appropriate,desconocido).
estado(thickness_treshold_limit,desconocido).
estado(valve_dazzling_and_rusting,desconocido).
estado(gas_leakage_at_joint,desconocido).
estado(leaked_fixed_wrench_joints,desconocido).
